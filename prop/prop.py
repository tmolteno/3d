# Super simple prop design by Tim Molteno
# tim@molteno.net
#

# Basic idea is to generate an STL file from a description

import numpy as np
import math
import foil
import stl_tools

class DesignParameters:
    '''Design Parameters for prop
    
    '''
    def __init__(self):
      self.velocity = 1.0  # m/s
      self.altitude = 0.0  # MAS
      self.RPM = 10000.0   #
      self.power = 70      # Watts
      self.radius = 0.0    # m
      self.hub_radius = 5.0 / 1000
      
    def rps(self):
      return self.RPM / 60.0
    
from scipy.interpolate import PchipInterpolator

class Prop:
    
    def __init__(self, diameter, pitch):
        ''' TODO don't use pitch. It only works in cases where
            the flow is uniform
        '''
        self.diameter = diameter  # m
        self.pitch = pitch # m
        self.radius = self.diameter / 2.0
        self.radial_resolution = 2.0 / 1000  # How often to create a profile
        self.radial_steps = self.radius / self.radial_resolution
        
        self.param = DesignParameters()
        
    def get_max_chord(self,r):
        ''' Allowed chord as a function of radius (m) 
            Limited by mechanical strength, or weight issues
        '''

        hub_r = self.param.hub_radius
        max_r = self.radius / 4

        hub_c = hub_r
        max_c = self.radius / 3
        end_c = hub_r

        x = np.array([0, hub_r, max_r, 0.9*self.radius, self.radius] )
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
        thickness = thickness_end + (1.0 - r / self.radius)*(thickness_root - thickness_end)
        return thickness

    def get_max_depth(self,r):
        ''' Allowed depth of the prop as a function of radius (m)
            This is a property of the environment that the prop operates in.
        '''
        hub_r = self.param.hub_radius
        hub_depth = 6.0 / 1000
        max_depth = 12.0 / 1000
        max_r = self.radius / 4.0
        end_depth = 2.0 / 1000

        x = np.array([0, hub_r, max_r, 0.9*self.radius, self.radius] )
        y = np.array([hub_depth, 1.1*hub_depth, max_depth, 1.2*end_depth, end_depth] )

        s = PchipInterpolator(x, y)

        depth = s(r)
        return depth

    def get_velocity(self, r):
        circumference = np.pi * 2 * r
        helical_length = np.sqrt(circumference*circumference + self.pitch*self.pitch)
        v = helical_length * self.param.rps()
        return v
      
    def design(self, trailing_thickness):
        self.foils = []
        for r in np.linspace(1e-6, self.radius, self.radial_steps):
            circumference = np.pi * 2 * r
            chord = self.get_max_chord(r)
            angle_of_attack = math.atan(self.pitch / circumference)
            f = foil.Foil(chord, angle_of_attack)
            self.foils.append([r, f])

        for r,f in self.foils:
            v = self.get_velocity(r)
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
        self.foils = []
        for r in np.linspace(self.param.hub_radius, self.radius, self.radial_steps):
            circumference = np.pi * 2 * r
            # Assume a slow velocity forward, and an angle of attack of 8 degrees
            pitch_per_rev = self.param.velocity / (self.param.rps())
            angle_of_attack = math.atan(pitch_per_rev / circumference) + 8.0*np.pi / 180

            depth_max = self.get_max_depth(r)
            chord = min(self.get_max_chord(r), depth_max / np.sin(angle_of_attack))
            thickness = self.get_foil_thickness(r)
            f = foil.NACA4(chord=chord, thickness=thickness / chord, \
                m=0.04, p=0.5, angle_of_attack=angle_of_attack)
            f.set_trailing_edge(trailing_thickness/chord)
            self.foils.append([r, f])

        for r,f in self.foils:
            v = self.get_velocity(r)
            print "r=%f, %s, v=%f, Re=%f" % (r, f, v, f.Reynolds(v))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Design a prop.')
    parser.add_argument('--diameter', type=float, required=True, help="Propeller diameter in mm.")
    parser.add_argument('--pitch', type=float, required=True, help="The pitch in mm")
    parser.add_argument('--n', type=int, default=20, help="The number of points in the top and bottom of the foil")
    parser.add_argument('--min-edge', type=float, default=0.5, help="The minimum thickness of the foil (mm).")
    parser.add_argument('--stl', default='prop.stl', help="The STL filename to generate.")
    args = parser.parse_args()
    

    p = NACAProp(args.diameter/1000, args.pitch / 1000)

    p.design(args.min_edge / 1000)
    p.gen_stl(args.stl, args.n)