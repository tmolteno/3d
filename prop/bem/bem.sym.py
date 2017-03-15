from sympy import *

r = Symbol('r', real=True, positive=True)    # Radius
theta = Symbol('theta', real=True)           # Element twist
u_1 = Symbol('u_1', real=True)               # Downstream Velocity 
u = Symbol('u', real=True)                   #  Velocity at prop
u_0 = Symbol('u_0', real=True)               # Upstream Velocity 
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

dv = Symbol('dv', real=True)
u_1 = u_0 + 2*dv
#u = u_0 + dv


m_dot = 2*pi*r*dr*rho*u


dT = m_dot * (u_1 - u_0)

# Velocity at the disk is average of V_0 and u_1. We create an axial induction factor that 
# Expresses the blade velocity (u) and the upstream velocity (V_0) in terms of the
# Wake velocity u_1.
a_prime = Symbol('a_prime', real=True)
omega = Symbol('omega', real=True)

v = Symbol('v', real=True)

dT = simplify(dT)
print("dT = {}".format(dT))  # Equivalent to 8.4


C_theta = 2*omega*r*a_prime # rotational wake velocity

dM = m_dot * r * C_theta
dM = simplify(dM)

print("dM = {}".format(dM))  # Equivalent to 8.5



#phi = atan(u/v_radial)
#phi = phi.subs(u_subs)
#print("phi = {}".format(phi))  # Equivalent to 8.7
phi = Symbol('phi')

## Now get Lift and Drag

c = Symbol('c', real=True)  # Chord of element airfoil
V_rel = Symbol('V_rel', real=True) # sqrt(u**2 + v_radial**2)

norm = rho*V_rel**2*c/2
alpha = theta - phi

L = norm*C_L    # Lift Force per unit length of prop
D = norm*C_D    # Drag Force per unit length of prop

F_N = L*cos(phi) - D*sin(phi)
F_T = L*sin(phi) + D*cos(phi)

C_n = F_N / norm
C_t = F_T / norm


B = Symbol('B', real=True)  # Number of blades

# Expressions for Thrust & Torque
dT_2 = B*F_N*dr
dM_2 = B*F_T*r*dr


#dT_2 = dT_2.subs(sin(phi), u/V_rel)
#dT_2 = dT_2.subs(cos(phi), v/V_rel)

dT_2 = dT_2.subs(V_rel, u / sin(phi))
dT_2 = simplify(dT_2)

dM = dM.subs(u, V_rel * sin(phi))
dM = dM.subs(V_rel, v / cos(phi))
dM = dM.subs(v, omega*r*(1 - a_prime))
dM = simplify(dM)

dM_2 = dM_2.subs(u, V_rel * sin(phi))
dM_2 = dM_2.subs(V_rel, v / cos(phi))
dM_2 = dM_2.subs(v, omega*r*(1 - a_prime))
dM_2 = simplify(dM_2)

print("dT = {}".format(dT))  # Equivalent to 8.4
print("dT_2 = {}".format(dT_2))  # Equivalent to 8.4

solnT = simplify(solve([Eq(dT, dT_2)], dv))
pprint(solnT)
print python(solnT)

print("dM = {}".format(dM))  # Equivalent to 8.4
print("dM_2 = {}".format(dM_2))  # Equivalent to 8.4

solnM = simplify(solve([Eq(dM, dM_2)], a_prime))[1][0]
pprint(solnM)

print python(solnM)
