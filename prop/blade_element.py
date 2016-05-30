import numpy as np
from foil_simulator import XfoilSimulatedFoil as FoilSimulator
#from foil_simulator import PlateSimulatedFoil as FoilSimulator

class BladeElement:
    def __init__(self, r, dr, foil, twist, alpha, velocity):
        self.r = r
        self.dr = dr
        self.foil = foil
        self.twist = twist
        self.velocity = velocity
        self.fs = FoilSimulator(self.foil)
        self.set_alpha(alpha)


    def set_alpha(self, alpha):
        z = self.fs.get_zero_cl_angle(self.velocity)
        print "Twist offset: %5.2f degrees" % np.degrees(z)
        self.alpha = alpha - z
        
    def get_forces(self, v):
        torque = 0.0
        lift = 0.0
        cd = self.fs.get_cd(v, self.alpha)
        drag = self.foil.drag_per_unit_length(v, cd)
        cl = self.fs.get_cl(v, self.alpha)
        section_lift = self.foil.lift_per_unit_length(v, cl)

        torque += self.dr*self.r*(drag*np.cos(self.twist) + lift*np.sin(self.twist))
        lift += self.dr*section_lift*self.r*np.cos(self.twist)

        return torque, lift

    def __repr__(self):
        return "BladeElement(r=%5.3f, twist=%5.2f, foil[%s], v=%5.1f, Re=%f)" % (self.r, np.degrees(self.twist), self.foil, self.velocity, self.foil.Reynolds(self.velocity))

if __name__ == "__main__":

    f = NACA4(chord=0.1, thickness=0.15, m=0.06, p=0.4, angle_of_attack=8.0 * np.pi / 180.0)
    f.set_trailing_edge(0.01)
    print f.hash()
    f.plot()
