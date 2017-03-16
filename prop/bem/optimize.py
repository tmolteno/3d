from numpy import pi, sin, cos, tan, arctan, degrees, sqrt, radians, arange

import sys
sys.path.append('..')

from foil_simulator import XfoilSimulatedFoil as FoilSim
from foil import NACA4

def C_lift(alpha):
    Clo = 2.0 * pi * alpha 
    return Clo

def C_drag(alpha):
    return 1.28 * sin(alpha)

def iterate(foil_simulator, dv, a_prime, theta, omega, r, u_0, B):
    u = u_0 + dv
    v = 2.0*omega*r*(1.0 - a_prime)
    c = foil_simulator.foil.chord
    
    phi = arctan(u/v)
    
    alpha = theta - phi
    v_rel = sqrt(u**2 + v**2)
    
    C_D = foil_simulator.get_cd(v_rel, alpha)
    C_L = foil_simulator.get_cl(v_rel, alpha)
    
    # These are created from the sympy file bem.sym.py, and are based on a modified
    # Blade Element Momentum method.
    dv_new = B*c*u*(-C_D*tan(phi) + C_L)/(8*pi*r*sin(phi)*tan(phi))
    a_prime_new =  B*c*(C_D + C_L*tan(phi))/(B*C_D*c + B*C_L*c*tan(phi) + 8*pi*r*sin(phi))

    return dv_new, a_prime_new

def bem(foil_simulator, theta, rpm, r, u_0, B):

    rps = rpm / 60.0
    omega = rps * 2 * pi

    err_min = 1e6
    
    for dv in arange(1.0, 50.0, 0.2):
        for a_prime in arange(0.0, 0.5, 0.01):
            dv2, a_prime2 = iterate(foil_simulator, dv, a_prime, theta, omega, r, u_0, B)
            err = abs(dv - dv2)/dv + 10.0*abs(a_prime - a_prime2)
            if (err < err_min):
                dv_guess = dv
                a_prime_guess = a_prime
                err_min = err
            #print dv_guess, dummy

    #print dv_guess, a_prime_guess
    dv = dv_guess
    a_prime = a_prime_guess
    while (True):
        dv2, a_prime2 = iterate(foil_simulator, dv,a_prime, theta, omega, r, u_0, B)
        err = abs(dv - dv2)/dv + 10.0*abs(a_prime - a_prime2)
        if (abs(err) < 0.0001):
            break
        dv += (dv2 - dv)/20
        a_prime += (a_prime2 - a_prime)/20

    return (dv2 + dv)/2, (a_prime2 + a_prime)/2


def dT(theta, rpm, r, u_0, c, B):
    print "dT"
    dv, a_prime = bem(theta, rpm, B, c, r, u_0)

f = NACA4(chord=0.01, thickness=0.15, m=0.06, p=0.4)
f.set_trailing_edge(0.01)
fs = FoilSim(f)
dv, a_prime = bem(foil_simulator=fs, theta = radians(5.0), rpm = 15000.0, B = 3, r = 0.05, u_0 = 0.0)
print("dv={}, a_prime={} ".format(dv, a_prime))
