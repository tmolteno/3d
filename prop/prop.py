# Super simple prop design by Tim Molteno
# tim@molteno.net
#

# Basic idea is to generate an STL file from a description

import numpy as np
import math
from stl import mesh

import foil

class Prop:
    
    def __init__(self, diameter, pitch):
        self.diameter = diameter  # mm
        self.pitch = pitch # mm
        self.radius = self.diameter / 2.0
        
    def get_chord_self(r):
        chord_root = 4.0
        chord_end = 2.0
        chord = (r / self.radius)*(chord_root - chord_end)
        return chord
    
    def design(self):
        trailing_thickness = 0.5
        self.foils = []
        for r in np.linspace(0, self.radius, 20):
            circumference = np.pi * 2 * r
            helical_length = np.sqrt(circumference*circumference + self.pitch*self.pitch)
            chord = 12.0
            angle_of_attack = math.atan(self.pitch / circumference)
            f = foil.Foil(chord, angle_of_attack)
            self.foils.append([r, f])
            
    def gen_stl(self, filename):
        for x in self.foils:
            r, f = x
            rpm = 10000
            omega = (rpm/60)*2*np.pi
            r_m = r / 1000
            v = r_m * omega
            print r, f.aoa *180 / np.pi, f.Reynolds(v)
            
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
        
p = Prop(120.0, 25.0)

p.design()
p.gen_stl('test.stl')