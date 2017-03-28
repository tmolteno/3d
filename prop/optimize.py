from numpy import pi, sin, cos, tan, arctan, degrees, sqrt, radians, arange

import sys
sys.path.append('..')

def C_lift(alpha):
    Clo = 2.0 * pi * alpha 
    return Clo

def C_drag(alpha):
    return 1.28 * sin(alpha)

def iterate(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B):
    u = u_0 + dv
    #print dv, a_prime, u_0, omega, r
    v = 2.0*omega*r*(1.0 - a_prime)
    c = foil_simulator.foil.chord
    #print u, v
    phi = arctan(u/v)
    
    alpha = theta - phi
    v_rel = sqrt(u**2 + v**2)
    C_D = foil_simulator.get_cd(v_rel, alpha)
    C_L = foil_simulator.get_cl(v_rel, alpha)
    
    # These are created from the sympy file bem.sym.py, and are based on a modified
    # Blade Element Momentum method.
    dv_new = B*c*u*(-C_D*tan(phi) + C_L)/(8*pi*r*sin(phi)*tan(phi))
    a_prime_new =  B*c*(C_D + C_L*tan(phi))/(B*C_D*c + B*C_L*c*tan(phi) + 8*pi*r*sin(phi))
    #print dv_new, a_prime_new

    dv_new = B*c*u*(-C_D*tan(phi) + C_L)/(4*pi*(dr + 2*r)*sin(phi)*tan(phi))
    a_prime_new = B*c*(C_D + C_L*tan(phi))/(B*C_D*c + B*C_L*c*tan(phi) + 4*pi*dr*sin(phi) + 8*pi*r*sin(phi))

    #print dv_new, a_prime_new
    return dv_new, a_prime_new


def dT(dv, r, dr, u_0, rho=1.225):
    u = u_0 + dv
    return 2*pi*dr*dv*rho*u*(dr + 2*r)

''' 
    http://web.mit.edu/16.unified/www/FALL/thermodynamics/notes/node86.html 
    see integral_momentum.sym.py
'''
def dv_from_thrust(T, R, u_0, rho=1.225):
    dv = -u_0/2 + sqrt(pi*R**2*rho**2*u_0**2 + 2*T*rho)/(2*sqrt(pi)*R*rho)
    return dv

'''
4*pi*a_prime*dr*omega*r**3*rho*u
'''
def dM(dv, a_prime, r, dr, omega, u_0, rho=1.225):
    u = u_0 + dv
    return 2*pi*a_prime*dr*omega*r**2*rho*u*(dr + 2*r)

def min_func(x, theta, omega, r, dr, u_0, B, foil_simulator):
    dv, a_prime = x
    dv2, a_prime2 = iterate(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B)
    err = ((dv - dv2)/dv)**2 + ((a_prime - a_prime2)/a_prime2)**2
    return err

from scipy.optimize import minimize
def bem_iterate(foil_simulator, dv_goal, theta, rpm, r, dr, u_0, B):

    rps = rpm / 60.0
    omega = rps * 2 * pi

    x0 = [dv_goal, 0.001]
    res = minimize(min_func, x0, args=(theta, omega, r, dr, u_0, B, foil_simulator), \
        #method='BFGS', options={'gtol': 1e-7, 'eps': 1e-7, 'disp': False, 'maxiter': 1000})
        method='nelder-mead', options={'xtol': 1e-8, 'disp': False})
    dv, a_prime = res.x
    return dv, a_prime, res.fun

''' Get a desired dv, by modifying alpha '''
def min_all(x, goal, rpm, r, dr, u_0, B, foil_simulator):
    theta, dv, a_prime = x
    if (theta < radians(-5.0)):
        return 1e6
    if (theta > radians(70)):
        return 1e6
    if (a_prime > 0.35):
        return 1e6
    if (a_prime < 0.0):
        return 1e6
    omega = (rpm/60) * 2 * pi

    dv2, a_prime2 = iterate(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B)
    err = ((dv - dv2)/dv2)**2 + ((a_prime - a_prime2)/a_prime2)**2
    err += ((dv - goal)/goal)**2
    return err

def design_for_dv(foil_simulator, th_guess, dv_guess, a_prime_guess, dv_goal, rpm, r, dr, u_0, B):
    x0 = [th_guess, dv_guess, a_prime_guess] # theta, dv, a_prime
    res = minimize(min_all, x0, args=(dv_goal, rpm, r, dr, u_0, B, foil_simulator), tol=1e-6, \
        #method='BFGS', options={'gtol': 1e-5, 'eps': 1e-4, 'disp': False, 'maxiter': 1000})
          method='Nelder-Mead', options={'xatol': 1e-8, 'disp': False, 'maxiter': 1000})
    if (res.fun > 0.001):
        # Restart optimization around previous best
        x0 = [res.x[0], dv_goal, res.x[2]] # theta, dv, a_prime
        x0 = [radians(5), dv_goal, 0.01] # theta, dv, a_prime

        res = minimize(min_all, x0, args=(dv_goal, rpm, r, dr, u_0, B, foil_simulator), tol=1e-8, \
            method='Nelder-Mead', options={'xatol': 1e-8, 'disp': True, 'maxiter': 1000})
    print("dv: {}, goal: {} a_prime={}".format(res.x[1], dv_goal, res.x[2]))
    return res.x, res.fun


def prop_design(R0 = 2.0/100, R = 10.0/100, tip_chord = 0.01, dr = 0.005, u_0 = 0.0, rpm = 15000.0):
    chord_scaling = tip_chord*R

    rps = rpm / 60.0
    omega = rps * 2 * pi

    for r in arange(R0, R, dr):
        
        chord = min(3*tip_chord, chord_scaling/r)
        f = NACA4(chord=chord, thickness=0.15, m=0.06, p=0.4)
        f.set_trailing_edge(0.01)
        fs = FoilSim(f)

        x, fun = design_for_dv(foil_simulator=fs, dv_goal=30.0,  rpm = rpm, B = 3, r = r, u_0 = u_0)
        theta, dv, a_prime = x
        print("r={}, theta={}, dv={}, a_prime={} \t:err={} ".format(r*100, degrees(theta), dv, a_prime, fun))

if __name__=="__main__":
    prop_design()

#if (False):
    #from foil_simulator import XfoilSimulatedFoil as FoilSim
    #from foil import NACA4


    ##r = 0.03
    #chord = min(3*tip_chord, chord_scaling/r)
    #f = NACA4(chord=chord, thickness=0.15, m=0.06, p=0.4)
    #f.set_trailing_edge(0.01)
    #fs = FoilSim(f)
    #print f
    #for th_deg in arange(0.0, 35.0):

        #dv, a_prime = bem2(foil_simulator=fs, theta = radians(th_deg), rpm = rpm, B = 3, r = r, u_0 = u_0)
        #thrust =  dT(dv, r, dr, u_0)

        #torque = dM(dv, a_prime, r, dr, omega, u_0)
        #print("theta={}, dv={}, a_prime={}, thrust={}, torque={}, eff={} ".format(th_deg, dv, a_prime, thrust, torque, thrust/torque))