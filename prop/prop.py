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



class Prop:
    '''
      A prop is a collection of BladeElement objects. 
    '''
    
    def __init__(self, param, resolution):
        self.param = param
        self.radial_resolution = resolution  # How often to create a profile
        self.radial_steps = int(self.param.radius / self.radial_resolution)
        self.chord_fraction = 7.0
        self.n_blades = 2
        
    
    def get_air_velocity_at_prop(self, torque, rpm, rho=1.225):
        r = self.param.radius
        tau=torque
        rps = rpm / 60.0
        return np.sqrt((r**2*rho)**(1/3)*(rps*tau)**(2/3)/(r**2*rho))


    
    def get_max_chord(self,r, twist):
        ''' Allowed chord as a function of radius (m) 
            Limited by mechanical strength, or weight issues
            
            k/r = end_c
            c = k / r
            
        '''
        circumference = 2.0*np.pi*r
        
        end_c = self.param.radius / self.chord_fraction
        k = end_c * self.param.radius

        chord = k / r
        
        return min(chord, (circumference / (self.n_blades+1))/np.cos(twist))

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
        thickness_root = self.param.hub_depth*0.9
        thickness_end = 1.0 / 1000
        # Solve s + kr^2 = end && s + kh^2 = start
        # Subtract kr^2 - k h^2 = (end - start) => k = (end - start) / (r^2 - h^2)
        # s = end - kr^2
        k = (thickness_end - thickness_root) / (self.param.radius**2 - self.param.hub_radius**2)
        s = thickness_end - k*self.param.radius**2
        thickness = s + k*r**2
        return thickness

    def get_max_depth(self,r):
        ''' Allowed depth of the prop as a function of radius (m)
            This is a property of the environment that the prop operates in.
        '''
        hub_r = self.param.hub_radius
        hub_depth = self.param.hub_depth
        max_depth = 15.0 / 1000
        max_r = self.param.radius / 3.0
        end_depth = 4.0 / 1000

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

        return 0.25*torque, lift



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
    
class NACAProp(Prop):
    ''' Prop that uses NACA Airfoils
    '''
    def design(self, optimum_rpm):
        forward_travel_per_rev = self.param.forward_airspeed / (optimum_rpm/60.0)
        print("Revs per second %f" % (optimum_rpm/60.0))
        print("Forward travel per rev %f" % forward_travel_per_rev)
        self.blade_elements = []
        radial_points = np.linspace(self.param.hub_radius, self.param.radius, self.radial_steps)
        for r in radial_points:
            twist = self.get_twist(r, optimum_rpm)
            nominal_alpha = np.radians(20)
            angle = min(np.pi/2, twist + nominal_alpha)
            depth_max = self.get_max_depth(r)
            chord = min(self.get_max_chord(r, angle), depth_max / np.sin(angle))
            thickness = self.get_foil_thickness(r)

            f = foil.NACA4(chord=chord, thickness=thickness / chord, m=0.15, p=0.4)
            f.set_trailing_edge(self.param.trailing_edge/(1000.0 * chord))
            
            v = self.get_blade_velocity(r, optimum_rpm)
            be = BladeElement(r, dr=self.radial_resolution, foil=f, twist=twist, alpha=nominal_alpha, velocity=v)
            print be
            self.blade_elements.append(be)

        optimum_aoa = []
        for be in self.blade_elements:
            v = self.get_blade_velocity(be.r, optimum_rpm)
            # Assume a slow velocity forward, and an angle of attack of 8 degrees
            twist = self.get_twist(be.r, optimum_rpm)
          
            alpha = np.radians(np.linspace(0, 30, 100))
            
            cl = be.fs.get_cl(v, alpha)
            cd = be.fs.get_cd(v, alpha)
            
            optim_target = (cl / (cd + 0.01))
            
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
            v = self.get_blade_velocity(r, optimum_rpm)
            twist = self.get_twist(r, optimum_rpm)
            angle = min(np.pi/2, twist + aoa)
            depth_max = self.get_max_depth(r)
            chord = min(self.get_max_chord(r, angle), depth_max / np.sin(angle))
            
            #f = foil.FlatPlate(chord=chord, angle_of_attack=twist + np.radians(15.0))
            f = foil.NACA4(chord=chord, thickness=self.get_foil_thickness(r) / chord, \
                m=0.06, p=0.3)
            f.set_trailing_edge(self.param.trailing_edge/(1000.0 * chord))

            be = BladeElement(r, dr=self.radial_resolution, foil=f, twist=twist, alpha=aoa, velocity=v)
            print be
            self.blade_elements.append(be)
        # 
        # Calculate the thickness distribution
        
        # Get foil polars
        # Assign angle of attack to be optimium
        torque, lift = self.get_torque(optimum_rpm)
        return torque
        
    def torque_modify(self, optimum_torque, optimum_rpm, aoa):

        forward_travel_per_rev = self.param.forward_airspeed / (optimum_rpm/60.0)
        radial_points = np.linspace(self.param.hub_radius, self.param.radius, self.radial_steps)
        for be in self.blade_elements:
            v = self.get_blade_velocity(be.r, optimum_rpm)
            twist = self.get_twist(be.r, optimum_rpm)
            angle = min(np.pi/2, twist + aoa)
            depth_max = self.get_max_depth(be.r)
            chord = min(self.get_max_chord(be.r, angle), depth_max / np.sin(angle))
            be.foil.chord = chord
            be.set_alpha(aoa)
            print be

        torque, lift = self.get_torque(optimum_rpm)
        return torque, lift
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Design a prop blade.')
    parser.add_argument('--param', default='prop_design.json', help="Propeller design parameters.")
    parser.add_argument('--n', type=int, default=20, help="The number of points in the top and bottom of the foil")
    parser.add_argument('--mesh', action='store_true', help="Generate a GMSH mesh")
    parser.add_argument('--auto', action='store_true', help="Use auto design torque")
    parser.add_argument('--resolution', type=float, default=6.0, help="The spacing between foil (mm).")
    parser.add_argument('--stl-file', default='prop.stl', help="The STL filename to generate.")
    args = parser.parse_args()
    
    
    param = DesignParameters(args.param)
    p = NACAProp(param, args.resolution / 1000)

    if (args.auto):
      m = motor_model.Motor(Kv = param.motor_Kv, I0 = param.motor_no_load_current, Rm = param.motor_winding_resistance)
      #m = motor_model.Motor(Kv = 1200.0, I0 = 0.5, Rm = 0.205)
      optimum_torque, optimum_rpm = m.get_Qmax(param.motor_volts)
      power = m.get_Pmax(param.motor_volts)
      print("Optimum Motor Torque %f at %f RPM, power=%f" % (optimum_torque, optimum_rpm, power))
      v = p.get_air_velocity_at_prop(optimum_torque, optimum_rpm)
      print("Airspeed at propellers (hovering): %f" % (v))
      param.forward_airspeed = v

      p.n_blades = 2
      aoa = np.radians(15.0)
      single_blade_torque = p.design_torque(optimum_torque, optimum_rpm, aoa)
      p.n_blades = np.round(optimum_torque/single_blade_torque)
      if (p.n_blades < 2):
        p.n_blades = 2
      print "Number of Blades: %d" % p.n_blades
      torque = single_blade_torque*p.n_blades
      dt = (optimum_torque - torque) / optimum_torque
      print "Torque=%f, optimum=%f, dt=%f" % (torque, optimum_torque, dt )
      while (abs(dt)  > 0.03):
        p.chord_fraction *= 1.0 - dt/3
        print "Chord Fraction %f" % p.chord_fraction
        torque,lift = p.torque_modify(optimum_torque, optimum_rpm, aoa)

        dt = (optimum_torque - torque*p.n_blades) / optimum_torque
        print "Torque=%f, lift=%f, optimum=%f, dt=%f" % (torque*p.n_blades, lift*p.n_blades, optimum_torque, dt )
      
    else:
      m = motor_model.Motor(Kv = param.motor_Kv, I0 = param.motor_no_load_current, Rm = param.motor_winding_resistance)
      optimum_torque, optimum_rpm = m.get_Qmax(param.motor_volts)
      p.n_blades = 2
      p.design(optimum_rpm)

    if (args.mesh):
      p.gen_mesh('gmsh.vtu', args.n)
      
    blade_stl_filename = param.name + "_blade.stl"
    p.gen_stl(blade_stl_filename, args.n)
    
    scad_filename = param.name + ".scad"
    p.gen_scad(scad_filename)