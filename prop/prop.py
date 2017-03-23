# Super simple prop design by Tim Molteno
# Copyright (c) 2016. Tim Molteno tim@molteno.net
#

import numpy as np
import math
import foil
import stl_tools
import motor_model

from blade_element import BladeElement
from design_parameters import DesignParameters
from scipy.interpolate import PchipInterpolator

import sys
sys.path.append('bem')
import optimize

class Prop:
    '''
      A prop is a collection of BladeElement objects. 
    '''
    
    def __init__(self, param, resolution):
        self.param = param
        self.radial_resolution = resolution  # How often to create a profile
        self.radial_steps = int(self.param.radius / self.radial_resolution)
        self.aspect_ratio = 10.0
        self.n_blades = 2

    def get_chord(self, r, rpm, alpha):
        twist = self.get_twist(r, rpm)
        angle = min(np.pi/2, twist + alpha)
        depth_max = self.get_max_depth(r)
        chord = min(self.get_max_chord(r, angle), depth_max / np.sin(angle))
        return chord

    def new_foil(self, r, rpm, alpha):
        twist = self.get_twist(r, rpm)
        thickness = self.get_foil_thickness(r)
        chord = self.get_chord(r, rpm, alpha)

        
        f = foil.Foil(chord=chord, thickness=thickness)
        f.set_trailing_edge(self.param.trailing_edge/(1000.0 * chord))
        
        v = self.get_blade_velocity(r, rpm)
        be = BladeElement(r, dr=self.radial_resolution, foil=f, twist=twist, alpha=alpha, velocity=v)
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
            
            k/r = end_c
            c = k / r
            
        '''
        if (False):
            circumference = 2.0*np.pi*r

            end_c = self.param.radius / self.aspect_ratio
            k = end_c * self.param.radius

            chord = k / r
            chord = min(chord, (circumference / (self.n_blades+1))/np.cos(twist))

        # New method using interpolation
        x = np.linspace(0.01, self.param.radius, 6)
        end_c = self.param.radius / self.aspect_ratio
        k = end_c * self.param.radius
        y = k / x
        
        lower_limit = (2.0*np.pi*x / (self.n_blades+2.0))/np.cos(twist)

        y = np.minimum(y,lower_limit)

        s = PchipInterpolator(x, y)

        return s(r) # min(chord, (circumference / (self.n_blades+1))/np.cos(twist))

    def get_scimitar_offset(self,r):
        ''' How much forward or aft of the centerline to place the foil
        '''

        hub_r = self.param.hub_radius
        max_r = self.param.radius * 0.8

        hub_c = 0.0
        max_c = self.param.radius * (self.param.scimitar_percent / 100.0)
        end_c = 0.0

        x = np.array([0,     hub_r,     max_r, self.param.radius] )
        y = np.array([hub_c, 1.1*hub_c, max_c, end_c] )

        s = PchipInterpolator(x, y)

        return s(r)

    def get_foil_thickness(self,r):
        ''' Allowed foil thickness as a function of radius (m) 
            Limited by mechanical strength, or weight issues
        '''
        thickness_root = self.param.hub_depth*0.8
        thickness_end = 0.7 / 1000
        # Solve s + kr^3 = end && s + kh^3 = start
        # Subtract kr^3 - k h^3 = (end - start) => k = (end - start) / (r^3 - h^3)
        # s = end - kr^3
        k = (thickness_end - thickness_root) / (self.param.radius**3 - self.param.hub_radius**3)
        s = thickness_end - k*self.param.radius**3
        thickness = s + k*r**3
        return thickness

    def get_max_depth(self,r):
        ''' Allowed depth of the prop as a function of radius (m)
            This is a property of the environment that the prop operates in.
            
            TODO Load this from the exclude zone of the prop description
        '''
        hub_r = self.param.hub_radius
        hub_depth = self.param.hub_depth
        max_depth = 12.0 / 1000
        max_r = self.param.radius / 3.0
        end_depth = 5.0 / 1000

        x = np.array([0, hub_r, max_r, 0.9*self.param.radius, self.param.radius] )
        y = np.array([hub_depth, 1.1*hub_depth, max_depth, 1.2*end_depth, end_depth] )

        s = PchipInterpolator(x, y)

        depth = s(r)
        return depth

    def get_helical_length(self, r, rpm):
        circumference = np.pi * 2 * r
        forward_travel_per_rev = self.get_forward_windspeed(r) / (rpm/60.0)

        helical_length = np.sqrt(circumference*circumference + forward_travel_per_rev*forward_travel_per_rev)
        return helical_length

    def get_twist(self, r, rpm):
        '''This is the angle that the prop makes to the air moving past at the design wind speed
        '''
        circumference = np.pi * 2 * r
        forward_travel_per_rev = self.get_forward_windspeed(r) / (rpm/60.0)
        twist = math.atan(forward_travel_per_rev / circumference)
        return twist

    def get_blade_velocity(self, r, rpm):
        '''The speed of the blade through the air
           The direction of travel is given by the twist angle
        '''
        v = self.get_helical_length(r, rpm) * (rpm/60.0)
        return v
      
    def get_forward_windspeed(self, r):
        ''' Get the airspeed as a function of radius.
            For hovering props, this will vary considerably and this function should contain
            a model that describes this.
        '''
        v = self.param.forward_airspeed
        
        hub_v = 3.0*v    # These should be determined by the thrust and area
        max_v = 2.0*v
        end_v = 1.2*v

        max_r = self.param.radius / 2.0

        x = np.array([0, max_r, self.param.radius, 2*self.param.radius] )
        y = np.array([hub_v, max_v, end_v, v] )

        s = PchipInterpolator(x, y)

        return s(r)

    def get_torque(self, rpm):
        torque = 0.0
        thrust = 0.0
        for be in self.blade_elements:
            v = self.get_blade_velocity(be.r, rpm)
            drag, lift = be.get_forces(v)
            
            torque += drag
            thrust += lift

        return torque+0.001, lift



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

    def design(self, optimum_rpm):
        forward_travel_per_rev = self.param.forward_airspeed / (optimum_rpm/60.0)
        print("Revs per second %f" % (optimum_rpm/60.0))
        print("Forward travel per rev %f" % forward_travel_per_rev)
        self.blade_elements = []
        radial_points = np.linspace(self.param.hub_radius, self.param.radius, self.radial_steps)
        for r in radial_points:
            nominal_alpha = np.radians(0)
            be = self.new_foil(r, optimum_rpm, nominal_alpha)
            print be
            self.blade_elements.append(be)

        optimum_aoa = []
        for be in self.blade_elements:
            v = self.get_blade_velocity(be.r, optimum_rpm)
            # Assume a slow velocity forward, and an angle of attack of 8 degrees
            twist = self.get_twist(be.r, optimum_rpm)
          
            alpha = np.radians(np.linspace(-20, 30, 100))
            
            cl = be.fs.get_cl(v, alpha)
            cd = be.fs.get_cd(v, alpha)
            
            optim_target = ((cl + 1.0) / (cd + 0.01))
            
            j = np.argmax(optim_target)
            opt_alpha = alpha[j]
            print np.degrees(opt_alpha)
            optimum_aoa.append(opt_alpha)

        # Now smooth the optimum angles of attack
        optimum_aoa = np.array(optimum_aoa)
        coeff = np.polyfit(radial_points, optimum_aoa, 4)
        angle_of_attack = np.poly1d(coeff)
        
        for be in self.blade_elements:
            a = angle_of_attack(be.r)
            be.set_alpha(a)
            print be
            
        torque, lift = self.get_torque(optimum_rpm)
        
        print("Torque: %f, Lift %f" % (torque, lift))

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
        torque, lift = self.get_torque(optimum_rpm)
        return torque

    def design_bem(self, optimum_torque, optimum_rpm, thrust):
        self.blade_elements = []
        u_0 = self.param.forward_airspeed

        dv_goal = optimize.dv_from_thrust(thrust, R=self.param.radius, u_0=u_0)
        
        radial_points = np.linspace(self.param.radius, self.param.hub_radius, self.radial_steps)
        #radial_points = np.linspace(self.param.hub_radius, self.param.radius, self.radial_steps)
        total_thrust = 0.0
        total_torque = 0.0
        omega = (optimum_rpm /  60.0) * 2.0 * np.pi
        dr = abs(radial_points[0]-radial_points[1])
        
        twist_angles = []
        for r in radial_points:
            dv_modified = dv_goal*(np.exp(-(self.param.radius/(20.0*r))**2))
            be = self.new_foil(r, optimum_rpm, 0.0)
            x, fun = optimize.design_for_dv(foil_simulator=be.fs, dv_goal=dv_modified, \
                rpm = optimum_rpm, B = 1, r = r, u_0 = u_0)
            theta, dv, a_prime = x
            if (fun > 0.01):
                try:
                    theta = self.blade_elements[-1].get_twist()
                except Exception:
                    #theta = np.radians(10.0)
                    ##dv, a_prime = optimize.bem2(foil_simulator=be.fs, theta = theta, \
                            ##rpm = optimum_rpm, B = 1, r = r, u_0 = u_0)
                    th_old = min(np.degrees(theta), 20)
                    print("Rescan around {}".format(th_old))
                    opt = 99.0
                    for th_deg in np.arange(th_old-15, th_old+15, 0.5):
                        dv_test, a_prime_test = optimize.bem2(foil_simulator=be.fs, theta = np.radians(th_deg), \
                            rpm = optimum_rpm, B = 1, r = r, u_0 = u_0)
                        print (th_deg, dv_test, a_prime_test)
                        if (abs(dv_test - dv_goal) < opt):
                            opt = abs(dv_test - dv_goal)
                            dv = dv_test
                            a_prime = a_prime_test
                            theta = np.radians(th_deg)
                        
            be.set_twist(theta)
            twist_angles.append(theta)
            
            dT =  optimize.dT(dv, r, dr, u_0)
            dM = optimize.dM(dv, a_prime, r, dr, omega, u_0)
            total_thrust += dT
            total_torque += dM
            
            print("theta={}, dv={}, a_prime={}, thrust={}, torque={}, eff={} ".format(np.degrees(theta), dv, a_prime, dT, dM, dT/dM))
            print be

            self.blade_elements.append(be)
        self.blade_elements.reverse()
        twist_angles.reverse()
        # Now smooth the twist angles
        # Now smooth the optimum angles of attack
        twist_angles = np.array(twist_angles)
        print twist_angles
        coeff = np.polyfit(radial_points[::-1], twist_angles, 4)
        twist_angle_poly = np.poly1d(coeff)
        
        for be in self.blade_elements:
            a = twist_angle_poly(be.r)
            be.set_twist(a)
            print be
            
        torque, lift = self.get_torque(optimum_rpm)
        print("Total Thrust: {}, Torque: {}".format(total_thrust, total_torque))
        return total_torque
        
    def torque_modify(self, optimum_torque, optimum_rpm, dt):

        forward_travel_per_rev = self.param.forward_airspeed / (optimum_rpm/60.0)
        radial_points = np.linspace(self.param.hub_radius, self.param.radius, self.radial_steps)
        
        # if dt < 0, we must reduce drag
        p.aspect_ratio *= 1.0 - dt/3

        for be in self.blade_elements:
            aoa = be.get_alpha()
            print "Current Angle of Attack %f" % np.degrees(aoa)
            v = self.get_blade_velocity(be.r, optimum_rpm)
            twist = self.get_twist(be.r, optimum_rpm)
            angle = min(np.pi/2, twist + aoa)
            print "Angle %f" % np.degrees(angle)
            depth_max = self.get_max_depth(be.r)
            chord = min(self.get_max_chord(be.r, angle), abs(depth_max / np.sin(angle)))
            be.foil.chord = chord
            be.set_alpha(aoa)
            print be

        torque, lift = self.get_torque(optimum_rpm)
        return torque, lift

class NACAProp(Prop):
    ''' Prop that uses NACA Airfoils
    '''

    def new_foil(self, r, rpm, alpha):
        twist = self.get_twist(r, rpm)
        thickness = self.get_foil_thickness(r)
        chord = self.get_chord(r, rpm, alpha)

        if (r < 0.01):
            f = foil.NACA4(chord=chord, thickness=thickness / chord, m=0.00, p=0.4)
        else:
            f = foil.NACA4(chord=chord, thickness=thickness / chord, m=0.06, p=0.4)
        f.set_trailing_edge(self.param.trailing_edge/(1000.0 * chord))
        
        v = self.get_blade_velocity(r, rpm)
        be = BladeElement(r, dr=self.radial_resolution, foil=f, twist=twist, alpha=alpha, velocity=v)
        return be
    
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Design a prop blade.')
    parser.add_argument('--param', default='prop_design.json', help="Propeller design parameters.")
    parser.add_argument('--n', type=int, default=20, help="The number of points in the top and bottom of the foil")
    parser.add_argument('--mesh', action='store_true', help="Generate a GMSH mesh")
    parser.add_argument('--bem', action='store_true', help="Use bem design")
    parser.add_argument('--auto', action='store_true', help="Use auto design torque")
    parser.add_argument('--naca', action='store_true', help="Use NACA airfoils (slow)")
    parser.add_argument('--resolution', type=float, default=6.0, help="The spacing between foil (mm).")
    parser.add_argument('--thrust', type=float, default=6.0, help="The thrust (Newtons).")
    parser.add_argument('--stl-file', default='prop.stl', help="The STL filename to generate.")
    args = parser.parse_args()
    
    
    param = DesignParameters(args.param)
    if args.naca:
        p = NACAProp(param, args.resolution / 1000)
    else:
        p = Prop(param, args.resolution / 1000)

    m = motor_model.Motor(Kv = param.motor_Kv, I0 = param.motor_no_load_current, Rm = param.motor_winding_resistance)
    optimum_torque, optimum_rpm = m.get_Qmax(param.motor_volts)
    power = m.get_Pmax(param.motor_volts)
    print("Optimum Motor Torque %f at %f RPM, power=%f" % (optimum_torque, optimum_rpm, power))
    v = p.get_air_velocity_at_prop(optimum_torque, optimum_rpm)
    print("Airspeed at propellers (hovering): %f" % (v))
    param.forward_airspeed = v


    if (args.bem):
        #p.n_blades = 2
        thrust = args.thrust
        goal_torque = optimum_torque/2
        single_blade_torque = goal_torque + 0.001
        
        #while single_blade_torque > goal_torque:
        #thrust *= 0.95 * goal_torque/single_blade_torque
        single_blade_torque = p.design_bem(optimum_torque, optimum_rpm, thrust=thrust)
        

    if (args.auto):
      p.n_blades = 2
      aoa = np.radians(6.0)
      single_blade_torque = p.design_torque(optimum_torque, optimum_rpm, aoa)
      p.n_blades = np.round(optimum_torque/single_blade_torque)
      if (p.n_blades < 2):
        p.n_blades = 2
      print "Number of Blades: %d" % p.n_blades
      torque = single_blade_torque*p.n_blades
      dt = (optimum_torque - torque) / optimum_torque
      print "Torque=%f, optimum=%f, dt=%f" % (torque, optimum_torque, dt )
      while (abs(dt)  > 0.03):
        #p.aspect_ratio *= 1.0 - dt/3
        print "Chord Fraction %f" % p.aspect_ratio
        print "AOA %f" % np.degrees(aoa)
        torque,lift = p.torque_modify(optimum_torque, optimum_rpm, dt)

        dt = (optimum_torque - torque*p.n_blades) / optimum_torque
        print "Torque=%f, lift=%f, optimum=%f, dt=%f" % (torque*p.n_blades, lift*p.n_blades, optimum_torque, dt )
      
    #else:
      #p.n_blades = 2
      #p.design(optimum_rpm)

    if (args.mesh):
      p.gen_mesh('gmsh.vtu', args.n)
      
    blade_stl_filename = param.name + "_blade.stl"
    p.gen_stl(blade_stl_filename, args.n)
    
    scad_filename = param.name + ".scad"
    p.gen_scad(scad_filename)
