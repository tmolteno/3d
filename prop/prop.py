# Super simple prop design by Tim Molteno
# tim@molteno.net
#

# Basic idea is to generate an STL file from a description

import numpy as np
import math
import foil
import stl_tools
import motor_model

from design_parameters import DesignParameters
from scipy.interpolate import PchipInterpolator

#from foil_simulator import XfoilSimulatedFoil as FoilSimulator
from foil_simulator import PlateSimulatedFoil as FoilSimulator

class Prop:
    
    def __init__(self, param, resolution):
        self.param = param
        self.radial_resolution = resolution  # How often to create a profile
        self.radial_steps = int(self.param.radius / self.radial_resolution)
        
        
    def get_max_chord(self,r):
        ''' Allowed chord as a function of radius (m) 
            Limited by mechanical strength, or weight issues
            
            k/r = end_c
            c = k / r
            
        '''
        end_c = self.param.radius / 6
        k = end_c * self.param.radius

        chord = k / r
        
        return chord

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
        thickness_root = 5.0 / 1000
        thickness_end = 2.0 / 1000
        thickness = thickness_end + (1.0 - r / self.param.radius)*(thickness_root - thickness_end)
        return thickness

    def get_max_depth(self,r):
        ''' Allowed depth of the prop as a function of radius (m)
            This is a property of the environment that the prop operates in.
        '''
        hub_r = self.param.hub_radius
        hub_depth = 6.0 / 1000
        max_depth = 15.0 / 1000
        max_r = self.param.radius / 3.0
        end_depth = 6.0 / 1000

        x = np.array([0, hub_r, max_r, 0.9*self.param.radius, self.param.radius] )
        y = np.array([hub_depth, 1.1*hub_depth, max_depth, 1.2*end_depth, end_depth] )

        s = PchipInterpolator(x, y)

        depth = s(r)
        return depth

    def get_helical_length(self, r):
        circumference = np.pi * 2 * r
        forward_travel_per_rev = self.get_forward_windspeed(r) / (self.param.rps())

        helical_length = np.sqrt(circumference*circumference + forward_travel_per_rev*forward_travel_per_rev)
        return helical_length

    def get_twist(self, r):
        circumference = np.pi * 2 * r
        forward_travel_per_rev = self.get_forward_windspeed(r) / (self.param.rps())
        twist = math.atan(forward_travel_per_rev / circumference)
        return twist

    def get_blade_velocity(self, r):
        v = self.get_helical_length(r) * self.param.rps()
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
      
    def design(self, trailing_thickness):
        self.foils = []
        for r in np.linspace(1e-6, self.param.radius, self.radial_steps):
            circumference = np.pi * 2 * r
            chord = self.get_max_chord(r)
            angle_of_attack = math.atan(self.pitch / circumference)
            f = foil.Foil(chord, angle_of_attack)
            fs = FoilSimulator(f)
            self.foils.append([r, f, fs])

        for r,f,fs in self.foils:
            v = self.get_blade_velocity(r)
            #print "r=%f, %s, v=%f, Re=%f" % (r, f, v, f.Reynolds(v))
    
    
    def get_torque(self):
        torque = 0.0
        for r,f,fs in self.foils:
            v = self.get_blade_velocity(r)
            twist = self.get_twist(r)
            cd = fs.get_cd(v, f.aoa-twist)
            drag = f.drag_per_unit_length(v, cd)
            dr = self.radial_resolution
            
            torque += dr*drag*r*np.cos(twist)
        return torque

    def get_foil_points(self, n, r, f):
        pl, pu = f.get_points(n)
        ''' points are in the y - z plane. The x value is set by the radius'''
        yl, zl = pl
        yu, zu = pu
        x = np.zeros(n) + r
        
        scimitar_angle = math.atan(self.get_scimitar_offset(r) / r)
        # Transform the profile to lie on a circle of radius r
        c = 2.0*np.pi*r   # Circumference
        theta_l = 2.0*np.pi*yl / c  + scimitar_angle # angular coordinate along circumference (fraction)
        xl = r*np.cos(theta_l)
        yl = r*np.sin(theta_l)

        theta_u = 2.0*np.pi*yu / c  + scimitar_angle # angular coordinate along circumference (fraction)
        xu = r*np.cos(theta_u)
        yu = r*np.sin(theta_u)
        
        upper_line = np.zeros([n,3])
        upper_line[:,0] = xu
        upper_line[:,1] = yu
        upper_line[:,2] = zu
        
        lower_line = np.zeros([n,3])
        lower_line[:,0] = xl
        lower_line[:,1] = yl
        lower_line[:,2] = zl
        
        return lower_line, upper_line

    def gen_mesh(self, filename, n):
        import pygmsh as pg
        geom = pg.Geometry()

        loops = []
        for r,f,fs in self.foils:
            car = 0.5/1000
            line_l, line_u = self.get_foil_points(n, r, f)
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
        for r,f,fs in self.foils:
            line_l, line_u = self.get_foil_points(n, r, f)
            
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


class NACAProp(Prop):
    ''' Prop that uses NACA Airfoils
    '''
    def design(self, trailing_thickness):
        forward_travel_per_rev = self.param.forward_airspeed / (self.param.rps())
        print("Revs per second %f" % self.param.rps())
        print("Forward travel per rev %f" % forward_travel_per_rev)
        self.foils = []
        radial_points = np.linspace(self.param.hub_radius, self.param.radius, self.radial_steps)
        for r in radial_points:
            twist = self.get_twist(r)

            depth_max = self.get_max_depth(r)
            chord = min(self.get_max_chord(r), depth_max / np.sin(twist + np.radians(30)))
            thickness = self.get_foil_thickness(r)
            
            f = foil.NACA4(chord=chord, thickness=thickness / chord, \
                m=0.15, p=0.4, angle_of_attack=twist)
            fs = FoilSimulator(f)
            
            f.set_trailing_edge(trailing_thickness/chord)

            self.foils.append([r, f, fs])

        optimum_aoa = []
        for r,f, fs in self.foils:
            v = self.get_blade_velocity(r)
            # Assume a slow velocity forward, and an angle of attack of 8 degrees
            twist = self.get_twist(r)
          
            if (f.Reynolds(v) < 20000.0):
              opt_alpha = np.radians(20.0)
              optimum_aoa.append(opt_alpha)
              f.aoa = twist + opt_alpha
              print "r=%f, twist=%f, %s, v=%f, Re=%f" % (r, np.degrees(twist), f, v, f.Reynolds(v))
            else:
              alpha = np.radians(np.linspace(0, 30, 100))
              
              cl = fs.get_cl(v, alpha)
              cd = fs.get_cd(v, alpha)
              
              optim_target = (cl / (cd + 0.01))
              
              j = np.argmax(optim_target)
              opt_alpha = alpha[j]
                            
              optimum_aoa.append(opt_alpha)
              print "r=%f, twist=%f, alfa=%f,  %s, v=%f, Re=%f, cl/cd=%f" % (r, np.degrees(twist), np.degrees(opt_alpha), f, v, f.Reynolds(v), optim_target[j])

        # Now smooth the optimum angles of attack
        optimum_aoa = np.array(optimum_aoa)
        coeff = np.polyfit(radial_points, optimum_aoa, 4)
        angle_of_attack = np.poly1d(coeff)
        
        for r,f,fs in self.foils:
            twist = self.get_twist(r)
            f.aoa = twist + angle_of_attack(r)
            print "r=%f, %s" % (r, f)
            
        torque = self.get_torque()
        print torque

    def design_torque(self, optimum_torque, optimum_rpm):
        self.foils = []
        self.param.motor_rpm = optimum_rpm
        # Calculate the chord distribution, from geometry and clearence
        forward_travel_per_rev = self.param.forward_airspeed / (self.param.rps())
        radial_points = np.linspace(self.param.hub_radius, self.param.radius, self.radial_steps)
        for r in radial_points:
            v = self.get_blade_velocity(r)
            twist = self.get_twist(r)

            depth_max = self.get_max_depth(r)
            chord = min(self.get_max_chord(r), depth_max / np.sin(twist + np.radians(30)))
            
            #f = foil.FlatPlate(chord=chord, angle_of_attack=twist + np.radians(15.0))
            f = foil.NACA4(chord=chord, thickness=self.get_foil_thickness(r) / chord, \
                m=0.1, p=0.4, angle_of_attack=twist + np.radians(15.0))
            f.set_trailing_edge(0.0005/chord)

            print "r=%f, twist=%f, %s, v=%f, Re=%f" % (r, np.degrees(twist), f, v, f.Reynolds(v))
            fs = FoilSimulator(f)
            self.foils.append([r, f, fs])
        # 
        # Calculate the thickness distribution
        
        # Get foil polars
        # Assign angle of attack to be optimium
        torque = self.get_torque()
        print torque
        print optimum_torque
        print optimum_torque / torque
        # Calculate lift, drag as a function of radius.
        # Get torque & lift
        # Modify chord distribution (and/or add blades if chord exceeds r/5)
        
        # Allocate the drag as a function of radius. The velocity is proportional to r, the 
        # drag is proportional to c_d r^2
        # Integrate the drag int_0^r cd r^2 = Torque
        # Modify the 
        return 3
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Design a prop blade.')
    parser.add_argument('--param', default='prop_design.json', help="Propeller design parameters.")
    parser.add_argument('--n', type=int, default=20, help="The number of points in the top and bottom of the foil")
    parser.add_argument('--mesh', action='store_true', help="Generate a GMSH mesh")
    parser.add_argument('--auto', action='store_true', help="Use auto design torque")
    parser.add_argument('--min-edge', type=float, default=0.5, help="The minimum thickness of the foil (mm).")
    parser.add_argument('--resolution', type=float, default=6.0, help="The spacing between foil (mm).")
    parser.add_argument('--stl-file', default='prop.stl', help="The STL filename to generate.")
    args = parser.parse_args()
    
    trailing_thickness = args.min_edge / 1000
    
    param = DesignParameters(args.param)
    p = NACAProp(param, args.resolution / 1000)

    if (args.auto):
      m = motor_model.Motor(Kv = 980.0, I0 = 0.5, Rm = 0.207)
      optimum_torque, optimum_rpm = m.get_Qmax(11.0)
      print("Optimum Torque %f at %f RPM" % (optimum_torque, optimum_rpm))
      p.design_torque(optimum_torque, optimum_rpm)
      
    else:
      p.design(trailing_thickness)

    if (args.mesh):
      p.gen_mesh('gmsh.vtu', args.n)
      
    p.gen_stl(args.stl_file, args.n)