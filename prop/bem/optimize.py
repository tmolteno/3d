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


def dT(dv, r, dr, u_0, rho=1.225):
    u = u_0 + dv
    return 4.0*pi*dr*dv*r*rho*u

def dM(a_prime, r, dr, omega, u_0, rho=1.225):
    u = u_0 + dv
    return 4*pi*a_prime*dr*omega*r**3*rho*u

def min_func(x, theta, omega, r, u_0, B, foil_simulator):
    dv, a_prime = x
    dv2, a_prime2 = iterate(foil_simulator, dv, a_prime, theta, omega, r, u_0, B)
    err = ((dv - dv2)/dv)**2 + ((a_prime - a_prime2)/a_prime2)**2
    return err

from scipy.optimize import minimize
def bem2(foil_simulator, theta, rpm, r, u_0, B):

    rps = rpm / 60.0
    omega = rps * 2 * pi

    x0 = [10.0, 0.0]
    res = minimize(min_func, x0, args=(theta, omega, r, u_0, B, foil_simulator), \
        method='nelder-mead', options={'xtol': 1e-6, 'disp': False})
    #res = minimize(min_func, res.x, args=(theta, omega, r, u_0, B, foil_simulator), \
        #method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
    dv, a_prime = res.x
    return dv, a_prime

''' Get a desired dv, by modifying alpha '''
def min_all(x, goal, rpm, r, u_0, B, foil_simulator):
    dv, a_prime, theta = x
    dv2, a_prime2 = iterate(foil_simulator, dv, a_prime, theta, omega, r, u_0, B)
    err = ((dv - dv2)/dv)**2 + ((a_prime - a_prime2)/a_prime2)**2
    err += ((dv - goal)/goal)**2
    return err

def design_for_dv(foil_simulator, dv_goal, rpm, r, u_0, B):
    x0 = [radians(0), 12.0, 0.0]
    res = minimize(min_all, x0, args=(dv_goal, rpm, r, u_0, B, foil_simulator), \
        method='nelder-mead', options={'xtol': 1e-6, 'disp': True, 'maxiter': 1000})
    #theta = res.x
    #dv, a_prime = bem2(foil_simulator, theta, rpm, r, u_0, B)
    return res.x

'''

Tihs is an old optimisation method that doesn't work very well.
def bem(foil_simulator, theta, rpm, r, u_0, B):

    rps = rpm / 60.0
    omega = rps * 2 * pi

    err_min = 1e6
    
    for dv in arange(1.0, 50.0, 0.5):
        for a_prime in arange(0.0, 0.5, 0.02):
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
'''




#print design_for_dv(foil_simulator=fs, dv_goal=15.0, rpm = 15000.0, B = 3, r = 0.05, u_0 = 0.0)
R = 0.1 # Radius of prop
tip_chord = 0.01
dr = 0.005
chord_scaling = tip_chord*R
u_0 = 0.0
rpm = 15000.0
rps = rpm / 60.0
omega = rps * 2 * pi

#for r in arange(0.01, R, dr):
    
    #chord = min(3*tip_chord, chord_scaling/r)
    #f = NACA4(chord=chord, thickness=0.15, m=0.06, p=0.4)
    #f.set_trailing_edge(0.01)
    #fs = FoilSim(f)

    #dv, a_prime, theta = design_for_dv(foil_simulator=fs, dv_goal=25.0,  rpm = rpm, B = 3, r = r, u_0 = u_0)
    #print("r={}, theta={}, dv={}, a_prime={} ".format(r*100, degrees(theta), dv, a_prime))
    
if (True):
    r = 0.03
    chord = min(3*tip_chord, chord_scaling/r)
    f = NACA4(chord=chord, thickness=0.15, m=0.06, p=0.4)
    f.set_trailing_edge(0.01)
    fs = FoilSim(f)

    for th_deg in arange(-10.0, 25.0):

        dv, a_prime = bem2(foil_simulator=fs, theta = radians(th_deg), rpm = rpm, B = 3, r = r, u_0 = u_0)
        thrust =  dT(dv, r, dr, u_0)

        torque = dM(a_prime, r, dr, omega, u_0)
        print("theta={}, dv={}, a_prime={}, thrust={}, torque={}, eff={} ".format(th_deg, dv, a_prime, thrust, torque, thrust/torque))
