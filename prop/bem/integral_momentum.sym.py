from sympy import *

r = Symbol('r', real=True, positive=True)    # Radius
R = Symbol('R', real=True, positive=True)    # Tip Radius
T = Symbol('T', real=True, positive=True)    # Tip Radius

u_1 = Symbol('u_1', real=True)               # Downstream Velocity 
u = Symbol('u', real=True)                   #  Velocity at prop
u_0 = 0 #Symbol('u_0', real=True)               # Upstream Velocity 


# Flow tube is annular at a radius r from the axis of the propeller.
rho = Symbol('rho', real=True)
dr = Symbol('dr', real=True)

dv = Symbol('dv', real=True)
u_1 = u_0 + 2*dv
u = u_0 + dv

A = pi*R*R
m_dot = rho * u * A


eqn = Eq(T , m_dot * (u_1 - u_0))

pprint(simplify(solve(eqn, dv)))
