from sympy import *

r = Symbol('r', real=True, positive=True)    # Radius
theta = Symbol('theta', real=True)           # Element twist
u_1 = Symbol('u_1', real=True)               # Downstream Velocity 
u = Symbol('u', real=True)                   #  Velocity at prop
V_0 = Symbol('V_0', real=True)               # Upstream Velocity 
C_L = Symbol('C_L', real=True)               # Coefficient of Lift for the element
C_D = Symbol('C_D', real=True)               # Coefficient of Drag for the element

'''
  Derive expressions for the blade element momentum theory
  for a propeller blade element.
  
  Reference. Hanson, Wind Turbine Aerodynamics
'''

# Flow tube is annular at a radius r from the axis of the propeller.
rho = Symbol('rho', real=True)
a = Symbol('a', real=True)
dr = Symbol('dr', real=True)


dT = 2*pi*r*rho* u * (V_0 - u_1) * dr

# Velocity at the disk is average of V_0 and u_1

deltaV = a*u_1
u_subs = [(V_0, u - deltaV), (u, u_1 - deltaV)]
dT = dT.subs(u_subs)
dT = simplify(dT)
print("dT = {}".format(dT))  # Equivalent to 8.4

C_inf = Symbol('C_oo')
a_prime = Symbol('a_prime')
omega = Symbol('omega')

dM = 2*pi*r**2 * rho*u*C_inf*dr
dM = dM.subs(C_inf, 2*omega*r*a_prime)
dM = dM.subs(u_subs)
dM = simplify(dM)

print("dM = {}".format(dM))  # Equivalent to 8.5

v_radial = omega*r*(1 + a_prime)
phi = atan(u/v_radial)
phi = phi.subs(u_subs)
print("phi = {}".format(phi))  # Equivalent to 8.7


## Now get Lift and Drag

c = Symbol('c', real=True)  # Chord of element airfoil
V_rel = sqrt(u**2 + v_radial**2)

L = rho*V_rel**2*c*C_l/2
D = rho*V_rel**2*c*C_d/2
