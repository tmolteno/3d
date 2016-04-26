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
      self.velocity = 0.0  # m/s
      self.altitude = 0.0  # MAS
      self.RPM = 10000.0   #
      self.power = 70      # Watts
      self.radius = 0.0    # m
      
      
class Prop:
    
    def __init__(self, diameter, pitch):
        ''' TODO don't use pitch. It only works in cases where
            the flow is uniform
        '''
        self.diameter = diameter  # m
        self.pitch = pitch # m
        self.radius = self.diameter / 2.0
        
    def get_chord(self,r):
        chord_root = 20.0 / 1000
        chord_end = 10.0 / 1000
        chord = chord_end + (1.0 - r / self.radius)*(chord_root - chord_end)
        return chord

    def design(self):
        trailing_thickness = 0.0
        self.foils = []
        for r in np.linspace(1e-6, self.radius, 40):
            circumference = np.pi * 2 * r
            helical_length = np.sqrt(circumference*circumference + self.pitch*self.pitch)
            chord = self.get_chord(r)
            angle_of_attack = math.atan(self.pitch / circumference)
            f = foil.Foil(chord, angle_of_attack)
            self.foils.append([r, f])

        for x in self.foils:
            r, f = x
            rpm = 10000.0
            omega = (rpm/60)*2.0*np.pi
            r_m = r
            v = r_m * omega
            #print "r=%f, %s, v=%f, Re=%f" % (r, f, v, f.Reynolds(v))

    def designNACA(self):
        trailing_thickness = 0.02
        self.foils = []
        for r in np.linspace(1e-6, self.radius, 40):
            circumference = np.pi * 2 * r
            helical_length = np.sqrt(circumference*circumference + self.pitch*self.pitch)
            chord = self.get_chord(r)
            angle_of_attack = math.atan(self.pitch / circumference)
            f = foil.NACA4(chord=chord, thickness=0.15, m=0.04, p=0.5, angle_of_attack=angle_of_attack)
            f.set_trailing_edge(trailing_thickness)
            self.foils.append([r, f])

        for x in self.foils:
            r, f = x
            rpm = 10000.0
            omega = (rpm/60)*2.0*np.pi
            r_m = r
            v = r_m * omega
            print "r=%f, %s, v=%f, Re=%f" % (r, f, v, f.Reynolds(v))
            
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
            
            line = np.zeros([n,3])
            line[:,0] = x*scale
            line[:,1] = yu*scale
            line[:,2] = zu*scale
            
            top_lines.append(line)
            top_edge.append(line[-1,:])
            
            line = np.zeros([n,3])
            line[:,0] = x*scale
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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Design a prop.')
    parser.add_argument('--diameter', type=float, required=True, help="Propeller diameter in mm.")
    parser.add_argument('--pitch', type=float, required=True, help="The pitch in mm")
    parser.add_argument('--n', type=int, default=20, help="The number of points in the top and bottom of the foil")
    parser.add_argument('--stl', default='prop.stl', help="The STL filename to generate.")
    args = parser.parse_args()
    

    p = Prop(args.diameter/1000, args.pitch / 1000)

    p.designNACA()
    p.gen_stl(args.stl, args.n)