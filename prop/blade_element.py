import numpy as np
#from foil_simulator import XfoilSimulatedFoil as FoilSimulator
from foil_simulator import PlateSimulatedFoil as FoilSimulator
import math


'''
    This objects holds an element that describes the foil geometry
    
    - twist, this is the angle that the air-flow makes to the horizontal, a twist of 90 would mean that
             the air-flow were pointing straight ahead
    - chord_angle, this is the angle that the chord makes to the horizontal
    - alpha, the angle of attack of the foil (measured from its chord line, to the twist angle)
    - zero_lift_angle. The angle of attack where Cl is zero.
    
    
    Why does the zero lift angle matter? Well, if we have no effect on the wake, then the foil will be oriented so that 
    it is twisted to point this angle at the upstream air.
    
    The angle of attack is given by
    
    twist + zero_lift_angle
'''
class BladeElement:
    def __init__(self, r, dr, foil, twist, alpha, velocity):
        self.r = r
        self.dr = dr
        self.foil = foil
        self.velocity = velocity
        self.fs = FoilSimulator(self.foil)
        self.zero_lift_angle = self.fs.get_zero_cl_angle(self.velocity)
        self.set_alpha(alpha)
        self.set_twist(twist)

    def get_zero_cl_angle(self):
        return self.zero_lift_angle

    def set_twist(self, twist):
        self._twist = twist
        self.chord_angle = self._twist + self.zero_lift_angle

    def get_twist(self):
        return self._twist

    def set_alpha(self, alpha):
        self._alpha = alpha

    def get_alpha(self):
        return self._alpha

    def get_forces(self, v):
        # Twist angle is the angle the incoming flow arrives at. 
        # Chord angle is the angle of the foil chord (reference angle for simulations)
        cd = self.fs.get_cd(v, self._alpha)
        cl = self.fs.get_cl(v, self._alpha)

        # Lift is perpendicular to incoming flow
        section_lift = self.dr*self.foil.lift_per_unit_length(v, cl)
        # Drag is in the direction of incoming flow
        section_drag = self.dr*self.foil.drag_per_unit_length(v, cd)

        torque = self.r*(section_drag*np.cos(self._twist) + section_lift*np.sin(self._twist))
        lift = section_lift*np.cos(self._twist) - section_drag*np.sin(self._twist)

        return torque, lift

    def get_foil_points(self, n, scimitar_offset):
        pl, pu = self.foil.get_points(n, self._alpha + self._twist)
        r = self.r
        ''' points are in the y - z plane. The x value is set by the radius'''
        yl, zl = pl
        yu, zu = pu
        x = np.zeros(n) + r

        scimitar_angle = math.atan(scimitar_offset / r)
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

    def __repr__(self):
        return "BladeElement(r=%5.3f, a=%5.2f, twist=%5.2f, z=%4.1f, foil[%s], v=%5.1f, Re=%f)" % (self.r, np.degrees(self._alpha), np.degrees(self._twist), np.degrees(self.zero_lift_angle), self.foil, self.velocity, self.foil.Reynolds(self.velocity))

if __name__ == "__main__":

    f = NACA4(chord=0.1, thickness=0.15, m=0.06, p=0.4, angle_of_attack=8.0 * np.pi / 180.0)
    f.set_trailing_edge(0.01)
    print f.hash()
    f.plot()
