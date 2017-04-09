# Super simple prop design by Tim Molteno
# Copyright (c) 2016-2017. Tim Molteno tim@molteno.net
#

import numpy as np
import math
import foil
import stl_tools
import motor_model

from blade_element import BladeElement
from design_parameters import DesignParameters
from scipy.interpolate import PchipInterpolator

import os
import logging
logger = logging.getLogger(__name__)

import optimize

class Prop:
    '''
      A prop is a collection of BladeElement objects. 
    '''
    
    def __init__(self, param, resolution):
        self.param = param
        self.radial_resolution = resolution  # How often to create a profile
        self.radial_steps = int(self.param.radius / self.radial_resolution)
        self.n_blades = 2
        self.max_depth_interpolator = None
        self.scimitar_interpolator = None
        self.max_chord_poly = None
        

    def get_chord(self, r, rpm, twist):
        '''
            depth = chord * sin(twist)
        '''
        angle = min(np.pi/2, twist)
        depth_limited_chord = np.abs(self.get_max_depth(r) / (np.sin(angle) + 1e-6))
        return min(self.get_max_chord(r, angle), depth_limited_chord)

    def new_foil(self, r, rpm, twist):
        thickness = self.get_foil_thickness(r)
        chord = self.get_chord(r, rpm, twist)

        f = foil.Foil(chord=chord, thickness=thickness)
        f.set_trailing_edge(self.param.trailing_edge)
        be = BladeElement(r, dr=self.radial_resolution, foil=f, twist=twist, \
            rpm=rpm, u_0 = self.param.forward_airspeed)
        return be


    def get_air_velocity_at_prop(self, torque, rpm, rho=1.225):
        r = self.param.radius
        tau=torque
        rps = rpm / 60.0
        v = np.sqrt((r**2*rho)**(1/3)*(rps*tau)**(2/3)/(r**2*rho))
        return v/2.0 # Half of the 

    def get_air_density(self):
        return 1.225 # kg m^{-3}
    
    def get_max_chord(self,r, twist):
        ''' Allowed chord as a function of radius (m) 
            Limited by mechanical strength, or weight issues
            
            k/r = tip_chord
            c = k / r
        '''
        if (self.max_chord_poly is None):
            x = np.linspace(0.001, self.param.radius, 36)
            k = self.param.tip_chord * self.param.radius
            y = k / x
            
            upper_limit = (2.0*np.pi*x / (self.n_blades+2.0))/np.cos(twist)

            y = np.minimum(y,upper_limit)

            coeff = np.polyfit(x, y, 11)
            self.max_chord_poly = np.poly1d(coeff)
            
            #import matplotlib.pyplot as plt
            #rpts = np.linspace(0, self.param.radius, 40)
            #plt.plot(rpts, self.max_chord_poly(rpts), label='max_chord')
            #plt.plot(x, y, 'x', label='points')
            #plt.legend()
            #plt.grid(True)
            #plt.xlabel('r')
            #plt.ylabel('Chord')
            #plt.show()


        return self.max_chord_poly(r)

    def get_scimitar_offset(self,r):
        ''' How much forward or aft of the centerline to place the foil
        '''
        if (self.scimitar_interpolator is None):
            hub_r = self.param.hub_radius
            max_r = self.param.radius * 0.8

            hub_c = 0.0
            max_c = self.param.radius * (self.param.scimitar_percent / 100.0)
            end_c = 0.0
            x = np.array([0,     hub_r,     max_r, self.param.radius] )
            y = np.array([hub_c, 1.1*hub_c, max_c, end_c] )

            self.scimitar_interpolator = PchipInterpolator(x, y)

            #import matplotlib.pyplot as plt
            #rpts = np.linspace(0, self.param.radius, 40)
            #plt.plot(rpts, self.scimitar_interpolator(rpts), label='scimitar')
            #plt.plot(x, y, 'x', label='points')
            #plt.legend()
            #plt.grid(True)
            #plt.xlabel('Angle of Attack')
            #plt.show()
        return self.scimitar_interpolator(r)

    def get_foil_thickness(self,r):
        ''' Allowed foil thickness as a function of radius (m) 
            Limited by mechanical strength, or weight issues
        '''
        thickness_root = self.param.hub_depth*0.8
        thickness_end = 0.9 / 1000
        # Solve s + kr^3 = end && s + kh^3 = start
        # Subtract kr^3 - k h^3 = (end - start) => k = (end - start) / (r^3 - h^3)
        # s = end - kr^3
        p = 0.87
        k = (thickness_end - thickness_root) / (self.param.radius**-p - self.param.hub_radius**-p)
        s = thickness_end - k*self.param.radius**-p
        thickness = s + k*r**-p
        
        #import matplotlib.pyplot as plt
        #rpts = np.linspace(self.param.hub_radius, self.param.radius, 40)
        #plt.plot(rpts, s + k*rpts**-p, label='thickness')
        #plt.legend()
        #plt.grid(True)
        #plt.xlabel('r')
        #plt.show()

        return thickness

    def get_max_depth(self,r):
        ''' Allowed depth of the prop as a function of radius (m)
            This is a property of the environment that the prop operates in.
            
            TODO Load this from the exclude zone of the prop description
        '''
        if (self.max_depth_interpolator is None):
            hub_r = self.param.hub_radius
            hub_depth = self.param.hub_depth
            max_depth = 12.0 / 1000
            max_r = self.param.radius / 3.0
            end_depth = 5.0 / 1000

            x = np.array([0, hub_r, max_r, 0.9*self.param.radius, self.param.radius] )
            y = np.array([hub_depth, 1.1*hub_depth, max_depth, 1.2*end_depth, end_depth] )
            self.max_depth_interpolator = PchipInterpolator(x, y)

            #import matplotlib.pyplot as plt
            #rpts = np.linspace(0, self.param.radius, 40)
            #plt.plot(rpts, self.max_depth_interpolator(rpts), label='max depth')
            #plt.plot(x, y, 'x', label='points')
            #plt.legend()
            #plt.grid(True)
            #plt.xlabel('r')
            #plt.show()


        return self.max_depth_interpolator(r)


    def get_forces(self, rpm):
        torque = 0.0
        thrust = 0.0
        for be in self.blade_elements:
            be.rpm = rpm
            dv_goal = be.dv
            dv, a_prime, err = be.bem(self.n_blades)

            if (err < 0.01):
                dT = be.dT()
                dM = be.dM()
                thrust += dT
                torque += dM
                logger.info("r={}, theta={}, dv={}, a_prime={}, thrust={}, torque={}, eff={} ".format( \
                    be.r, np.degrees(be.get_twist()), \
                    dv, a_prime, dT, dM, dT/dM))

            else:
                logger.warning("r={}: BEM did not converge {} {} {}".format(be.r, be.dv, dv_goal, a_prime, err))
                if (err > 0.5):
                    be.dv = 1.0
                    be.a_prime = 0.0

        return torque, thrust



    def gen_mesh(self, filename, n):
        import pygmsh as pg
        geom = pg.Geometry()

        loops = []
        for be in self.blade_elements:
            car = 0.5/1000
            line_l, line_u = be.get_foil_points(n, self.get_scimitar_offset(be.r))
            loop_points = np.concatenate((line_l, line_u[::-1]), axis=0)
            g_pts = []
            for p in loop_points[0:-2]:
              g_pts.append(geom.add_point(p,car))
              
            l_foil = geom.add_bspline(g_pts)
            
            loops.append(l_foil)

        #print geom.get_code()
        geom.add_ruled_surface([loops[0], loops[1]])
        
        #l in range(len(loops) - 1):
            #geom.add_surface(loops[l], loops[l+1])
        #poly = geom.add_polygon([
            #[0.0,   0.5, 0.0],
            #[-0.1,  0.1, 0.0],
            #[-0.5,  0.0, 0.0],
            #[-0.1, -0.1, 0.0],
            #[0.0,  -0.5, 0.0],
            #[0.1,  -0.1, 0.0],
            #[0.5,   0.0, 0.0],
            #[0.1,   0.1, 0.0]
            #],
            #lcar=0.05
            #)
        #axis = [0, 0, 1]

        #geom.extrude(
            #'Surface{%s}' % poly,
            #translation_axis=axis,
            #rotation_axis=axis,
            #point_on_axis=[0, 0, 0],
            #angle=2.0 / 6.0 * np.pi
            #)

        points, cells = pg.generate_mesh(geom)

        import meshio
        meshio.write(filename, points, cells)
            
    def gen_stl(self, filename, n):
        stl = stl_tools.STL()
        
        scale = 1000.0 # Convert to mm.
        top_lines = []
        bottom_lines = []
        
        bottom_edge = []
        top_edge = []
        for be in self.blade_elements:
            line_l, line_u = be.get_foil_points(n,  self.get_scimitar_offset(be.r))
            
            top_lines.append(line_u*scale)
            top_edge.append(line_u[-1,:]*scale)
            
            
            bottom_lines.append(line_l*scale)
            bottom_edge.append(line_l[-1,:]*scale)

        stl.add_line(bottom_lines[0])
        ## Do the top surface
        for tl in top_lines:
            stl.add_line(tl)
            
        ## Do the bottom surface
        bottom_lines.reverse()
        for bl in bottom_lines:
            stl.add_line(bl)
        
        ## Join the trailing edges
        stl.new_block()
        stl.add_line(bottom_edge)
        stl.add_line(top_edge)
        
        stl.gen_stl(filename)

    def gen_scad(self, filename):
        ''' Create an OpenSCAD file for the propeller
        '''
        blade_stl_filename = self.param.name + '_blade.stl'
        f=open(filename,"w")
        f.write("center_hole = 5;\n \
hub_diameter = %f;\n \
hub_height = %f;\n \
n_blades = %d;\n \
blade_name = \"%s\";\n"  % (self.param.hub_radius*2000, self.param.hub_depth*1000.0, self.n_blades, blade_stl_filename))
        
        template_file = open('pyprop_template.scad', 'r')
        template = template_file.read()
        template_file.close()
        
        f.write(template)
        f.close()

    def gen_removable_blade_scad(self, filename):
        ''' Create an OpenSCAD file for the propeller
        '''
        blade_stl_filename = self.param.name + '_blade.stl'
        f=open(filename,"w")
        f.write("center_hole = 5;\n \
hub_diameter = %f;\n \
hub_height = %f;\n \
n_blades = %d;\n \
blade_name = \"%s\";\n"  % (self.param.hub_radius*2000, self.param.hub_depth*1000.0, self.n_blades, blade_stl_filename))
        
        template_file = open('blade_template.scad', 'r')
        template = template_file.read()
        template_file.close()
        
        f.write(template)
        f.close()


    def design_torque(self, optimum_torque, optimum_rpm, aoa):
        self.blade_elements = []
        # Calculate the chord distribution, from geometry and clearence
        forward_travel_per_rev = self.param.forward_airspeed / (optimum_rpm / 60.0)
        radial_points = np.linspace(self.param.hub_radius, self.param.radius, self.radial_steps)
        for r in radial_points:
            be = self.new_foil(r, optimum_rpm, aoa)
            be.set_alpha(be.get_zero_cl_angle())
            print be

            self.blade_elements.append(be)
        # 
        # Calculate the thickness distribution
        
        # Get foil polars
        # Assign angle of attack to be optimium
        torque, thrust = self.get_forces(optimum_rpm)
        return torque

    def tip_loss(self, r, phi):
        e = (self.n_blades*(self.param.radius - r*0.95))/(2.0*r*np.sin(phi))
        F = 2.0 * np.arccos(np.exp(-e)) / np.pi
        
        hub_loss = np.cos(phi)
        return F*hub_loss 
        
    def design_bem(self, optimum_torque, optimum_rpm, thrust):
        self.blade_elements = []
        u_0 = self.param.forward_airspeed

        dv_goal = optimize.dv_from_thrust(thrust, R=self.param.radius, u_0=u_0)
        radial_points = np.linspace(self.param.radius, self.param.hub_radius, self.radial_steps)

        total_thrust = 0.0
        total_torque = 0.0
        omega = (optimum_rpm /  60.0) * 2.0 * np.pi
        dr = abs(radial_points[0]-radial_points[1])
        
        twist_angles = []
        theta = 0.0  # start guess
        dv = dv_goal  # start guess
        a_prime = 0.001  # start guess
        prev_twist = 0.0

        #import matplotlib.pyplot as plt
        #phi_all = np.arctan((u_0 + dv_goal)/(omega*radial_points))
        #plt.plot(radial_points, self.tip_loss(radial_points, 0.1), label='tip loss')
        #plt.plot(radial_points, phi_all, label='phi')
        #plt.plot(radial_points, np.cos(phi_all), label='cos(phi)')
        #plt.legend()
        #plt.grid(True)
        #plt.xlabel('radius')
        #plt.show()
        #return None
        for r in radial_points:
            u = u_0 + dv_goal
            v = omega*r
            phi = np.arctan(u/v)
            
            dv_modified = dv_goal*self.tip_loss(r, phi)
            be = self.new_foil(r, optimum_rpm, prev_twist)
            x, fun = optimize.design_for_dv(foil_simulator=be.fs, dv_goal=dv_modified, \
                rpm = optimum_rpm, B = self.n_blades, r = r, dr=dr, u_0 = u_0)
            theta, dv, a_prime = x
            if (fun > 0.03):
                logger.info("Rescan around {}".format(np.degrees(phi)))
                opt = 9999.9
                for th_deg in np.arange(np.degrees(phi)-5, np.degrees(phi)+15, 0.5):
                    dv_test, a_prime_test, err = optimize.bem_iterate(foil_simulator=be.fs, \
                        dv_goal=dv_modified, theta = np.radians(th_deg), \
                        rpm = optimum_rpm, B = self.n_blades, r = r, dr=dr, u_0 = u_0)
                    logger.info("err={:5.4f}, th={:4.2f}, dv={:4.2f}, a'={:5.4f}".format(err, th_deg, dv_test, a_prime_test))
                    delta = abs(dv_test - dv_modified)
                    if (err < 0.01) and (delta < opt):
                        opt = delta
                        dv = dv_test
                        a_prime = a_prime_test
                        theta = np.radians(th_deg)
                        logger.info("Best Delta {} at {} deg".format(delta, th_deg))

                
                #x, fun = optimize.design_for_dv(foil_simulator=be.fs, \
                    #th_guess=theta, dv_guess=dv, a_prime_guess=a_prime, dv_goal=dv_modified, \
                    #rpm = optimum_rpm, B = self.n_blades, r = r, dr=dr, u_0 = u_0)
                #if (fun < 0.01):
                    #theta, dv, a_prime = x

            be.set_twist(theta)
            be.set_bem(dv, a_prime)
            twist_angles.append(theta)
            
            dT = be.dT()
            dM = be.dM()
            total_thrust += dT
            total_torque += dM
            
            print("r={} theta={}, dv={}, a_prime={}, thrust={}, torque={}, eff={} ".format(r, np.degrees(theta), dv, a_prime, dT, dM, dT/dM))
            print be

            self.blade_elements.append(be)
            prev_twist = theta
            
        self.blade_elements.reverse()
        twist_angles.reverse()
        # Now smooth the twist angles
        # Now smooth the optimum angles of attack
        twist_angles = np.array(twist_angles)
        coeff = np.polyfit(radial_points[::-1], twist_angles, 3)
        twist_angle_poly = np.poly1d(coeff)
        
        import matplotlib.pyplot as plt
        plt.plot(radial_points[::-1], twist_angles, label='twist angles')
        plt.plot(radial_points[::-1], twist_angle_poly(radial_points[::-1]), label='Smoothed twist angles')
        plt.legend()
        plt.grid(True)
        plt.xlabel('Angle of Attack')
        plt.show()
        print("Smoothed Blade Form")
        
        for be in self.blade_elements:
            a = twist_angle_poly(be.r)
            be.set_twist(a)
            print be

            
        torque, thrust = self.get_forces(optimum_rpm)
        return torque, thrust
        

class NACAProp(Prop):
    ''' Prop that uses NACA Airfoils
    '''

    def new_foil(self, r, rpm, twist):
        thickness = self.get_foil_thickness(r)
        chord = self.get_chord(r, rpm, twist)
        if (chord < 0.0):
            raise Exception("Chord {} < 0, twist={} deg".format(chord, np.degrees(twist)))
        if (r < 0.01):
            f = foil.NACA4(chord=chord, thickness=thickness / chord, m=0.00, p=0.4)
        else:
            f = foil.NACA4(chord=chord, thickness=thickness / chord, m=0.06, p=0.4)
        f.set_trailing_edge(self.param.trailing_edge/1000.0)
        
        #v = self.get_blade_velocity(r, rpm)
        be = BladeElement(r, dr=self.radial_resolution, foil=f, twist=twist, \
            rpm=rpm, u_0 = self.param.forward_airspeed)
        return be
    

class ARADProp(Prop):
    ''' Prop that uses ARAD Airfoils
    '''

    def new_foil(self, r, rpm, twist):
        import foil_ARA
        thickness = self.get_foil_thickness(r)
        chord = self.get_chord(r, rpm, twist)
        if (chord < 0.0):
            raise Exception("Chord {} < 0, twist={} deg".format(chord, np.degrees(twist)))
        f = foil_ARA.ARADFoil(chord=chord, thickness=thickness / chord)
        f.set_trailing_edge(self.param.trailing_edge/1000.0)
        
        #v = self.get_blade_velocity(r, rpm)
        be = BladeElement(r, dr=self.radial_resolution, foil=f, twist=twist, \
            rpm=rpm, u_0 = self.param.forward_airspeed)
        return be
    
import logging.config
import yaml

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Design a prop blade.')
    parser.add_argument('--param', default='prop_design.json', help="Propeller design parameters.")
    parser.add_argument('--n', type=int, default=20, help="The number of points in the top and bottom of the foil")
    parser.add_argument('--mesh', action='store_true', help="Generate a GMSH mesh")
    parser.add_argument('--bem', action='store_true', help="Use bem design")
    parser.add_argument('--auto', action='store_true', help="Use auto design torque")
    parser.add_argument('--arad', action='store_true', help="Use ARA-D airfoils (slow)")
    parser.add_argument('--naca', action='store_true', help="Use NACA airfoils (slow)")
    parser.add_argument('--resolution', type=int, default=40, help="The number of blade elements.")
    parser.add_argument('--stl-file', default='prop.stl', help="The STL filename to generate.")
    args = parser.parse_args()
    
    # Set up Logging
    path = 'logging.yaml'
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)

    # Decode Design Parameters
    param = DesignParameters(args.param)
    resolution_m = (param.radius - param.hub_radius) / args.resolution
    if args.arad:
        p = ARADProp(param, resolution_m)
    elif args.naca:
        p = NACAProp(param, resolution_m)
    else:
        p = Prop(param, resolution_m)

    m = motor_model.Motor(Kv = param.motor_Kv, I0 = param.motor_no_load_current, Rm = param.motor_winding_resistance)
    optimum_torque, optimum_rpm = m.get_Qmax(param.motor_volts)
    power = m.get_Pmax(param.motor_volts)
    
    print("\nPROPLY: Automatic propeller Design\n\n")
    print("Optimum Motor Torque {:5.3f} Nm at {:5.1f} RPM, power={:5.1f} Watts".format(optimum_torque, optimum_rpm, power))
    print("Spanwise resolution (mm) {:4.2f}".format(resolution_m*1000))
    print(param)
    dv = optimize.dv_from_thrust(param.thrust, param.radius, param.forward_airspeed,)
    print("Airspeed at propellers (hovering): {:4.2f} m/s".format(param.forward_airspeed + dv))
    print("\n\n")

    if (args.bem):
        p.n_blades = param.blades
        thrust = param.thrust
        goal_torque = optimum_torque*1.5
        Q, T = p.design_bem(optimum_torque, optimum_rpm, thrust=thrust)
        print("Total Thrust: {:5.2f}, Torque: {:5.3f}".format(T, Q))
        if (args.auto):
            while Q > goal_torque:
                thrust *= 0.95 * goal_torque/Q
                Q, T = p.design_bem(optimum_torque, optimum_rpm, thrust=thrust)
                print("Total Thrust: {:5.2f} (N), Torque: {:5.2f} (Nm)".format(T, Q))

        # Print Thrust and Torque as a function of RPM.
        #print("RPM, \t\t THRUST, \t TORQUE")
        #rpm_list = np.linspace(optimum_rpm/3, 2*optimum_rpm, 30)
        #for rpm in rpm_list:
            #torque, thrust = p.get_forces(rpm)
            #print("{:5.3f}, \t {:5.3f}, \t{:5.3f}".format(rpm, thrust, torque))


    if (args.mesh):
      p.gen_mesh('gmsh.vtu', args.n)
      
    blade_stl_filename = param.name + "_blade.stl"
    p.gen_stl(blade_stl_filename, args.n)
    
    scad_filename = param.name + ".scad"
    p.gen_scad(scad_filename)
    
    p.gen_removable_blade_scad(param.name + "_removable.scad")

    
