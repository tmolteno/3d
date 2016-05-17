from sympy import *

'''
    Static Thrust.
    
    from http://www.dept.aoe.vt.edu/~lutze/AOE3104/thrustmodels.pdf
    
    
'''
torque = Symbol('tau')  # motor torque in N.m = kg m^2 s^-2
rps = Symbol('rps')     # Revolutions per second
r = Symbol('r')         # Radius

Pt0 = (torque / r) * (rps * r * 2 * pi)
pprint(Pt0)

A = Symbol('A')    # Prop Area
rho = Symbol('rho') # Air Density


'''
    This is the theoretical maximum static thrust calculated
    from momentum conservation, and assuming no losses due to 
    drag, or tip vortices e.t.c.
    
    The efficiency is therefore the ratio of this maximum thrust
    to the actual thrust.
'''
thrust = (Pt0**Rational(2,3))*(2*rho*A)**Rational(1,3)
pprint(thrust)
