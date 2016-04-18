# Super simple prop design by Tim Molteno
# tim@molteno.net
#

# Basic idea is to generate an STL file from a description

import numpy as np
import math

class Foil:
    def __init__(self, chord, angle_of_attack):
        self.chord = chord
        self.aoa = angle_of_attack
        
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
        
        for r in np.linspace(0, self.radius, 20):
            print r,
            circumference = np.pi * 2 * r
            helical_length = np.sqrt(circumference*circumference + self.pitch*self.pitch)
            angle_of_attack = math.atan(self.pitch / circumference)
            print angle_of_attack*180 / np.pi

p = Prop(120.0, 25.0)

p.design()