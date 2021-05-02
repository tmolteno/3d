import numpy as np
from foil_simulator import XfoilSimulatedFoil as FoilSimulator
#from foil_simulator import PlateSimulatedFoil as FoilSimulator
import math
import optimize

import logging
logger = logging.getLogger(__name__)

'''
    This objects holds an element that describes the foil geometry
    
    - twist, this is the angle that the chord makes to the horizontal, a twist of 90 would mean that
             the air-flow were pointing straight ahead
    - zero_lift_angle. The angle of attack where Cl is zero.
    
    
    Why does the zero lift angle matter? Well, if we have no effect on the wake, then the foil will be oriented so that it is twisted to point this angle at the upstream air.
'''
class BladeElement:
    def __init__(self, r, dr, foil, twist, rpm, u_0):
        self.r = r
        self.dr = dr
        self.foil = foil
        self.fs = FoilSimulator(self.foil)
        self.zero_lift_angle = None
        self.set_twist(twist)
        self.dv = 0.0
        self.a_prime = 0.0
        self.velocity = 0.0
        self.rpm = rpm
        self.omega = 2.0*np.pi*rpm / 60
        self.u_0 = u_0

    def get_zero_cl_angle(self):
        return 0.0 
        #self.zero_lift_angle = self.fs.get_zero_cl_angle(self.velocity)
        #return self.zero_lift_angle

    def set_chord(self, c):
        self.foil.modify_chord(c)

    def set_twist(self, twist):
        self._twist = twist

    def get_twist(self):
        return self._twist
    
    ''' Thrust from this element '''
    def dT(self):
        return optimize.dT(self.dv, self.r, self.dr, self.u_0, rho=1.225)

    ''' Torque from this element '''
    def dM(self):
        return optimize.dM(self.dv, self.a_prime, self.r, self.dr, self.omega, self.u_0, rho=1.225)

    def bem(self, n_blades):
        logger.info("bem {}".format(self))
        dv, a_prime, err = optimize.bem_iterate(foil_simulator=self.fs, dv_goal=self.dv, \
            theta = self._twist, rpm = self.rpm, B = n_blades, \
            r = self.r, dr=self.dr, u_0 = self.u_0)

        self.set_bem(dv,a_prime)
        return dv, a_prime, err

    ''' Set parameters from a blade element momentum computation
    '''
    def set_bem(self, dv, a_prime):
        self.dv = dv
        self.a_prime = a_prime
        
        u = self.u_0 + dv
        v = self.omega*self.r*(1.0 - self.a_prime)
        self.velocity = np.sqrt(u**2 + v**2)


    def get_foil_points(self, n, scimitar_offset):
        pl, pu = self.foil.get_points(n, self._twist)
        r = self.r
        
        ''' points are in the y - z plane. The x value is set by the radius'''
        yl, zl = pl
        yu, zu = pu
        x = np.zeros(n) + r

        #y_offset = np.mean(np.append(yl,yu))
        
        #yl -= y_offset
        #yu -= y_offset
        
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
        dt = self.dT()
        dm = self.dM()
        return "BladeElement(r={:5.3f}, twist={:5.2f}, foil[{}], dv={:4.1f}, eff={:4.1f})".format(self.r, np.degrees(self._twist), self.foil, self.dv, dt/dm)

if __name__ == "__main__":

    f = NACA4(chord=0.1, thickness=0.15, m=0.06, p=0.4, angle_of_attack=8.0 * np.pi / 180.0)
    f.set_trailing_edge(0.01)
    print(f.hash())
    f.plot()
