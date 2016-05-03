# Super simple prop design by Tim Molteno
# tim@molteno.net
#

# Basic idea is to generate an STL file from a description

import numpy as np
import math
import foil
import stl_tools

from design_parameters import DesignParameters

from scipy.interpolate import PchipInterpolator

class Prop:
    
    def __init__(self, param):
        self.param = param
        self.radial_resolution = 2.0 / 1000  # How often to create a profile
        self.radial_steps = int(self.param.radius / self.radial_resolution)
        
        
    def get_max_chord(self,r):
        ''' Allowed chord as a function of radius (m) 
            Limited by mechanical strength, or weight issues
        '''

        hub_r = self.param.hub_radius
        max_r = self.param.radius / 3

        hub_c = hub_r
        max_c = self.param.radius / 3
        end_c = self.param.radius / 8

        x = np.array([0, hub_r, max_r, 0.9*self.param.radius, self.param.radius] )
        y = np.array([hub_c, 1.1*hub_c, max_c, 1.2*end_c, end_c] )

        s = PchipInterpolator(x, y)

        chord = s(r)
        return chord

    def get_foil_thickness(self,r):
        ''' Allowed foil thickness as a function of radius (m) 
            Limited by mechanical strength, or weight issues
        '''
        thickness_root = 5.0 / 1000
        thickness_end = 1.0 / 1000
        thickness = thickness_end + (1.0 - r / self.param.radius)*(thickness_root - thickness_end)
        return thickness

    def get_max_depth(self,r):
        ''' Allowed depth of the prop as a function of radius (m)
            This is a property of the environment that the prop operates in.
        '''
        hub_r = self.param.hub_radius
        hub_depth = 6.0 / 1000
        max_depth = 15.0 / 1000
        max_r = self.param.radius / 2.0
        end_depth = 3.0 / 1000

        x = np.array([0, hub_r, max_r, 0.9*self.param.radius, self.param.radius] )
        y = np.array([hub_depth, 1.1*hub_depth, max_depth, 1.2*end_depth, end_depth] )

        s = PchipInterpolator(x, y)

        depth = s(r)
        return depth

    def get_blade_velocity(self, r):
        circumference = np.pi * 2 * r
        forward_travel_per_rev = self.param.forward_airspeed / (self.param.rps())

        helical_length = np.sqrt(circumference*circumference + forward_travel_per_rev*forward_travel_per_rev)
        v = helical_length * self.param.rps()
        return v
      
    def get_forward_windspeed(self, r):
        ''' Get the airspeed as a function of radius.
            For hovering props, this will vary considerably and this function should contain
            a model that describes this.
        '''
        return self.param.forward_airspeed
      
    def design(self, trailing_thickness):
        self.foils = []
        for r in np.linspace(1e-6, self.param.radius, self.radial_steps):
            circumference = np.pi * 2 * r
            chord = self.get_max_chord(r)
            angle_of_attack = math.atan(self.pitch / circumference)
            f = foil.Foil(chord, angle_of_attack)
            self.foils.append([r, f])

        for r,f in self.foils:
            v = self.get_blade_velocity(r)
            #print "r=%f, %s, v=%f, Re=%f" % (r, f, v, f.Reynolds(v))
            
    def gen_stl(self, filename, n):
        
        stl = stl_tools.STL()
        scale = 1000.0 # Convert to mm.
        
        top_lines = []
        bottom_lines = []
        
        bottom_edge = []
        top_edge = []
        for r, f in self.foils:
            pl, pu = f.get_points(n)
            ''' points are in the y - z plane. The x value is set by the radius'''
            yl, zl = pl
            yu, zu = pu
            x = np.zeros(n) + r
            
            # Transform the profile to lie on a circle of radius r
            c = 2.0*np.pi*r   # Circumference
            theta_l = 2.0*np.pi*yl / c  # angular coordinate along circumference (fraction)
            xl = r*np.cos(theta_l)
            yl = r*np.sin(theta_l)

            theta_u = 2.0*np.pi*yu / c  # angular coordinate along circumference (fraction)
            xu = r*np.cos(theta_u)
            yu = r*np.sin(theta_u)
            
            line = np.zeros([n,3])
            line[:,0] = xu*scale
            line[:,1] = yu*scale
            line[:,2] = zu*scale
            
            top_lines.append(line)
            top_edge.append(line[-1,:])
            
            line = np.zeros([n,3])
            line[:,0] = xl*scale
            line[:,1] = yl*scale
            line[:,2] = zl*scale
            
            bottom_lines.append(line)
            bottom_edge.append(line[-1,:])

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
        
        print bottom_edge

        stl.gen_stl(filename)


class NACAProp(Prop):
    ''' Prop that uses NACA Airfoils
    '''
    def design(self, trailing_thickness):
        forward_travel_per_rev = self.param.forward_airspeed / (self.param.rps())
        print("Revs per second %f" % self.param.rps())
        print("Forward travel per rev %f" % forward_travel_per_rev)
        self.foils = []
        for r in np.linspace(self.param.hub_radius, self.param.radius, self.radial_steps):
            circumference = np.pi * 2 * r
            # Assume a slow velocity forward, and an angle of attack of 8 degrees
            
            angle_of_attack = math.atan(forward_travel_per_rev / circumference) + 15.0*np.pi / 180

            depth_max = self.get_max_depth(r)
            chord = min(self.get_max_chord(r), depth_max / np.sin(angle_of_attack))
            thickness = self.get_foil_thickness(r)/1.5
            f = foil.NACA4(chord=chord, thickness=thickness / chord, \
                m=0.1, p=0.5, angle_of_attack=angle_of_attack)
            f.set_trailing_edge(trailing_thickness/chord)
            self.foils.append([r, f])

        for r,f in self.foils:
            v = self.get_blade_velocity(r)
            print "r=%f, %s, v=%f, Re=%f" % (r, f, v, f.Reynolds(v))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Design a prop blade.')
    parser.add_argument('--param', default='prop_design.json', help="Propeller design parameters.")
    parser.add_argument('--n', type=int, default=20, help="The number of points in the top and bottom of the foil")
    parser.add_argument('--min-edge', type=float, default=0.5, help="The minimum thickness of the foil (mm).")
    parser.add_argument('--stl-file', default='prop.stl', help="The STL filename to generate.")
    args = parser.parse_args()
    
    param = DesignParameters(args.param)
    p = NACAProp(param)

    p.design(args.min_edge / 1000)
    p.gen_stl(args.stl_file, args.n)