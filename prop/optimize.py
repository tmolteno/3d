'''
   Proply Core Optimisation Routines
   
   Authon: Tim Molteno (c) 2017.
'''
from numpy import pi, sin, cos, tan, arctan, degrees, sqrt, radians, arange, zeros, array

import logging
logger = logging.getLogger(__name__)

def rpm2omega(rpm):
    rps = rpm / 60.0
    return 2*pi*rps

def iterate(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B):
    C_L, C_D, c, phi = precalc(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B)
    
    dv_new = -B*c*(C_D*(dv + u_0) + C_L*omega*r*(a_prime - 1))*sqrt(omega**2*r**2*(a_prime - 1)**2 + (dv + u_0)**2)/(4*pi*(dr + 2*r)*(dv + u_0))
    
    a_prime_new = -B*c*sqrt(omega**2*r**2*(a_prime - 1)**2 + (dv + u_0)**2)*(C_D*omega*r*(a_prime - 1) - C_L*(dv + u_0))/(4*pi*omega*r*(dr + 2*r)*(dv + u_0))
    
    return dv_new, a_prime_new

def precalc(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B):
    u = u_0 + dv
    v = omega*r*(1.0 - a_prime)
    c = foil_simulator.foil.chord
    phi = arctan(u/v)
    alpha = theta - phi
    v_rel = sqrt(u**2 + v**2)
    C_D = foil_simulator.get_cd(v_rel, alpha)
    C_L = foil_simulator.get_cl(v_rel, alpha)
    return C_L, C_D, c, phi

def lsq(C_L, C_D, c, dv, a_prime, theta, omega, r, dr, u_0, B):
    minfun=(-B*c*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)*(C_D*omega*r*(-a_prime + 1) + C_L*(dv + u_0))/(4*pi*omega*r*(dr + 2*r)*(dv + u_0)) + a_prime)**2/(a_prime + 0.01)**2 + (B*c*(C_D*(dv + u_0) - C_L*omega*r*(-a_prime + 1))*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)/(4*pi*(dr + 2*r)*(dv + u_0)) + dv)**2/dv**2
    return minfun

def jac(C_L, C_D, c, dv, a_prime, theta, omega, r, dr, u_0, B):
    dmindv=(-B*c*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)*(C_D*omega*r*(-a_prime + 1) + C_L*(dv + u_0))/(4*pi*omega*r*(dr + 2*r)*(dv + u_0)) + a_prime)*(-B*C_L*c*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)/(2*pi*omega*r*(dr + 2*r)*(dv + u_0)) - B*c*(C_D*omega*r*(-a_prime + 1) + C_L*(dv + u_0))/(2*pi*omega*r*(dr + 2*r)*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)) + B*c*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)*(C_D*omega*r*(-a_prime + 1) + C_L*(dv + u_0))/(2*pi*omega*r*(dr + 2*r)*(dv + u_0)**2))/(a_prime + 0.01)**2 + (B*c*(C_D*(dv + u_0) - C_L*omega*r*(-a_prime + 1))*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)/(4*pi*(dr + 2*r)*(dv + u_0)) + dv)*(B*C_D*c*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)/(2*pi*(dr + 2*r)*(dv + u_0)) + B*c*(C_D*(dv + u_0) - C_L*omega*r*(-a_prime + 1))/(2*pi*(dr + 2*r)*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)) - B*c*(C_D*(dv + u_0) - C_L*omega*r*(-a_prime + 1))*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)/(2*pi*(dr + 2*r)*(dv + u_0)**2) + 2)/dv**2 - 2*(B*c*(C_D*(dv + u_0) - C_L*omega*r*(-a_prime + 1))*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)/(4*pi*(dr + 2*r)*(dv + u_0)) + dv)**2/dv**3
    dminda=(-B*c*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)*(C_D*omega*r*(-a_prime + 1) + C_L*(dv + u_0))/(4*pi*omega*r*(dr + 2*r)*(dv + u_0)) + a_prime)*(B*C_D*c*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)/(2*pi*(dr + 2*r)*(dv + u_0)) - B*c*omega*r*(2*a_prime - 2)*(C_D*omega*r*(-a_prime + 1) + C_L*(dv + u_0))/(4*pi*(dr + 2*r)*(dv + u_0)*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)) + 2)/(a_prime + 0.01)**2 - 2*(-B*c*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)*(C_D*omega*r*(-a_prime + 1) + C_L*(dv + u_0))/(4*pi*omega*r*(dr + 2*r)*(dv + u_0)) + a_prime)**2/(a_prime + 0.01)**3 + (B*c*(C_D*(dv + u_0) - C_L*omega*r*(-a_prime + 1))*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)/(4*pi*(dr + 2*r)*(dv + u_0)) + dv)*(B*C_L*c*omega*r*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)/(2*pi*(dr + 2*r)*(dv + u_0)) + B*c*omega**2*r**2*(2*a_prime - 2)*(C_D*(dv + u_0) - C_L*omega*r*(-a_prime + 1))/(4*pi*(dr + 2*r)*(dv + u_0)*sqrt(omega**2*r**2*(-a_prime + 1)**2 + (dv + u_0)**2)))/dv**2
    return array([dmindv, dminda])

def min_func2(x, theta, omega, r, dr, u_0, B, foil_simulator):
    dv, a_prime = x
    C_L, C_D, c, phi = precalc(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B)
    return lsq(C_L, C_D, c, dv, a_prime, theta, omega, r, dr, u_0, B)

def jac_func2(x, theta, omega, r, dr, u_0, B, foil_simulator):
    dv, a_prime = x
    C_L, C_D, c, phi = precalc(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B)
    return jac(C_L, C_D, c, dv, a_prime, theta, omega, r, dr, u_0, B)
    
def iterate_old(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B):
    C_L, C_D, c, phi = precalc(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B)

    # These are created from the sympy file bem.sym.py, and are based on a modified
    # Blade Element Momentum method.

    dv_new = -B*c*(C_D*(dv + u_0) + C_L*omega*r*(a_prime - 1))*sqrt(omega**2*r**2*(a_prime - 1)**2 + (dv + u_0)**2)/(4*pi*(dr + 2*r)*(dv + u_0))
    a_prime_new = -B*c*sqrt(omega**2*r**2*(a_prime - 1)**2 + (dv + u_0)**2)*(C_D*omega*r*(a_prime - 1) - C_L*(dv + u_0))/(4*pi*omega*r*(dr + 2*r)*(dv + u_0))

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


def error(dv, dv2, a_prime, a_prime2):
    return abs((dv - dv2)/(dv + dv2)) + abs((a_prime - a_prime2)/(a_prime + a_prime2))

def initial_simplex_bem(x0):
    ret = zeros((3,2))
    dv_guess, a_prime_guess = x0
    ret[0] = array([dv_guess, a_prime_guess])
    ret[1] = array([dv_guess-5.0, a_prime_guess/2])
    ret[2] = array([dv_guess+5.0, a_prime_guess*2])
    return ret

def min_func(x, theta, omega, r, dr, u_0, B, foil_simulator):
    dv, a_prime = x
    if (a_prime > 0.35):
        return a_prime*1000
    if (a_prime < 0.0):
        return 10 - a_prime*1000
    try:
        dv2, a_prime2 = iterate(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B)
        return error(dv, dv2, a_prime, a_prime2)
    except ValueError:
        logging.info("ValueError in iteration")
        return 1e6


from scipy.optimize import minimize, fixed_point

def fp_func(x, theta, omega, r, dr, u_0, B, foil_simulator):
    dv, a_prime = x
    #print x
    dv2, a_prime2 = iterate(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B)
    return array([dv2, a_prime2])

def bem_iterate(foil_simulator, dv_goal, theta, rpm, r, dr, u_0, B):
    x0 = [dv_goal, 0.01]
    res = minimize(min_func2, x0, jac=jac_func2, args=(theta, rpm2omega(rpm), r, dr, u_0, B, foil_simulator), \
        method='SLSQP', bounds=[(0,2*dv_goal),(0.0,0.2)], options={'disp': False, 'maxiter': 1000})
        #method='nelder-mead', options={'initial_simplex': initial_simplex_bem(x0), \
            #'xtol': 1e-8, 'disp': False})
    dv, a_prime = res.x
    err = res.fun
    
    #x0 = [dv, a_prime]
    #res = fixed_point(fp_func, x0, args=(theta, omega, r, dr, u_0, B, foil_simulator), maxiter=10000)
    #dv, a_prime = res
    #dv2, a_prime2 = iterate(foil_simulator, dv, a_prime, theta, omega, r, dr, u_0, B)s
    #err = error(dv, dv2, a_prime, a_prime2)s

    return dv, a_prime, err

def initial_simplex_all(x0):
    ret = zeros((4,3))
    th_guess, dv_guess, a_prime_guess = x0
    ret[0] = array([th_guess, dv_guess-1, a_prime_guess])
    ret[1] = array([th_guess-0.02, dv_guess, a_prime_guess])
    ret[2] = array([th_guess, dv_guess+1.0, a_prime_guess])
    ret[3] = array([th_guess+0.02, dv_guess, a_prime_guess+0.01])
    return ret
        
''' Get a desired dv, by modifying alpha '''
def min_all(x, goal, rpm, r, dr, u_0, B, foil_simulator):
    theta, dv, a_prime = x
    try:
        if (theta < radians(-5.0)):
            return 1e6
        if (theta > radians(70)):
            return 1e6
        if (a_prime > 0.35):
            return a_prime*1000
        if (a_prime < 0.0):
            return 10 - a_prime*1000

        dv2, a_prime2 = iterate(foil_simulator, dv, a_prime, theta, rpm2omega(rpm), r, dr, u_0, B)
        err = error(dv, dv2, a_prime, a_prime2)
        err += ((dv - goal)/goal)**2
        return err
    except ValueError as ve:
        logging.info("ValueError in iteration {}".format(ve))
        return 1e6

def design_for_dv(foil_simulator, th_guess, dv_guess, a_prime_guess, dv_goal, rpm, r, dr, u_0, B):
    C_L, C_D, c, phi = precalc(foil_simulator, dv_goal, 0, 0, (rpm/60) * 2 * pi, r, dr, u_0, B)
    print  C_L, C_D, c, degrees(phi)
    x0 = [th_guess, dv_goal, a_prime_guess] # theta, dv, a_prime
    res = minimize(min_all, x0, args=(dv_goal, rpm, r, dr, u_0, B, foil_simulator), tol=1e-10, \
        method='SLSQP', bounds=((phi-3,phi+10), (dv_goal/2,2*dv_goal),(0.001,0.1)), options={'disp': True, 'maxiter': 1000})
        #method='BFGS', options={'gtol': 1e-6, 'eps': [1e-3, 1e-2, 1e-6], 'disp': True, 'maxiter': 1000})
          #method='Nelder-Mead', options={'initial_simplex': initial_simplex_all(x0), \
              #'xatol': 1e-7, 'disp': False, 'maxiter': 10000})
    #if (res.fun > 0.1):
        ## Restart optimization around previous best
        ##x0 = [res.x[0], dv_goal, res.x[2]] # theta, dv, a_prime
        #x0 = [radians(5), dv_goal, 0.01] # theta, dv, a_prime

        #res = minimize(min_all, x0, args=(dv_goal, rpm, r, dr, u_0, B, foil_simulator), tol=1e-8, \
            #method='Nelder-Mead', options={'xatol': 1e-8, 'disp': True, 'maxiter': 1000})
            ##method='BFGS', options={'gtol': 1e-8, 'eps': 1e-5, 'disp': True, 'maxiter': 1000})
    logger.info("dv: {}, goal: {} a_prime={}".format(res.x[1], dv_goal, res.x[2]))
    return res.x, res.fun


from foil import NACA4
from foil_simulator import PlateSimulatedFoil as FoilSim
#from foil_simulator import XfoilSimulatedFoil as FoilSim

def prop_design(R0 = 2.0/100, R = 10.0/100, tip_chord = 0.01, dr = 0.005, u_0 = 0.0, rpm = 10000.0):
    chord_scaling = tip_chord*R

    rps = rpm / 60.0
    omega = rps * 2 * pi

    for r in arange(R0, R, dr):
        
        chord = min(3*tip_chord, chord_scaling/r)
        f = NACA4(chord=chord, thickness=0.15, m=0.06, p=0.4)
        f.set_trailing_edge(0.001)
        fs = FoilSim(f)

        dv = 5.0
        a_prime = 0.001
        theta = radians(10)
        B = 2
        #for i in range(0,100):
            #print dv, a_prime
            #dv, a_prime = iterate(fs, dv, a_prime, theta, omega, r, dr, u_0, B)
        dv, a_prime, err = bem_iterate(fs, 5.0, theta, rpm, r, dr, u_0, B)
        print dv, a_prime, err
        x, fun = design_for_dv(foil_simulator=fs, th_guess=0, dv_guess=5, a_prime_guess=0.01, dv_goal=5.0,  rpm = rpm, B = B, r = r, dr=dr, u_0 = u_0)
        theta, dv, a_prime = x
        print("r={}, theta={}, dv={}, a_prime={} \t:err={} ".format(r*100, degrees(theta), dv, a_prime, fun))

if __name__=="__main__":
    prop_design()
