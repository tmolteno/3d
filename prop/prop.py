# Super simple prop design by Tim Molteno
# tim@molteno.net
#

# Basic idea is to generate an STL file from a description

import numpy as np
import math
from stl import mesh

import foil

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
        trailing_thickness = 0.5
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
            print "r=%f, %s, v=%f, Re=%f" % (r, f, v, f.Reynolds(v))
            
    def gen_stl(self, filename):
        
        for x in self.foils:
            r, f = x
            pts = f.get_points(30)
            print pts

        # Define the 8 vertices of the cube
        vertices = np.array([\
            [-1, -1, -1],
            [+1, -1, -1],
            [+1, +1, -1],
            [-1, +1, -1],
            [-1, -1, +1],
            [+1, -1, +1],
            [+1, +1, +1],
            [-1, +1, +1]])
        # Define the 12 triangles composing the cube
        faces = np.array([\
            [0,3,1],
            [1,3,2],
            [0,4,7],
            [0,7,3],
            [4,5,6],
            [4,6,7],
            [5,1,2],
            [5,2,6],
            [2,3,6],
            [3,7,6],
            [0,1,5],
            [0,5,4]])

        # Create the mesh
        cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                cube.vectors[i][j] = vertices[f[j],:]

        # Write the mesh to file "cube.stl"
        cube.save(filename)

diameter = 120.0  # mm
pitch = 60.0 # mm

p = Prop(diameter/1000, pitch / 1000)

p.design()
p.gen_stl('test.stl')