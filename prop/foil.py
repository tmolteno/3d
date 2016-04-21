import numpy as np


class Foil:
    def __init__(self, chord, angle_of_attack):
        self.chord = chord
        self.aoa = angle_of_attack

    ''' Calculate Reynolds number from air density rho
        and kinematic ciscoscity (nu)
        
        rho - density of air  kg/m3
        nu  - kinematic viscoscity m^2/s
    '''
    def Reynolds(self, velocity, rho=1.225, nu=15.11e-6):
        L = self.chord
        return rho*velocity*L/nu
      
      
    def __repr__(self):
      return "ch=%f, a=%f" % (self.chord, self.aoa *180 / np.pi)