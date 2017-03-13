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

# Velocity at the disk is average of V_0 and u_1. We create an axial induction factor that 
# Expresses the blade velocity (u) and the upstream velocity (V_0) in terms of the
# Wake velocity u_1.
a_prime = Symbol('a_prime')
omega = Symbol('omega')

v_radial = omega*r*(1 + a_prime)
v_radial = Symbol('V_radial') # omega*r*(1 + a_prime)

u_subs = [(V_0, u_1*(1 - 2*a)), (u, u_1*(1 - a))]
v_subs = [(v_radial, omega*r*(1 + a_prime))]
dT = dT.subs(u_subs)
dT = simplify(dT)
print("dT = {}".format(dT))  # Equivalent to 8.4

C_inf = Symbol('C_oo')

dM = 2*pi*r**2 * rho*u*C_inf*dr
dM = dM.subs(C_inf, 2*omega*r*a_prime)
dM = dM.subs(u_subs)
dM = simplify(dM)

print("dM = {}".format(dM))  # Equivalent to 8.5



#phi = atan(u/v_radial)
#phi = phi.subs(u_subs)
#print("phi = {}".format(phi))  # Equivalent to 8.7
phi = Symbol('phi')

## Now get Lift and Drag

c = Symbol('c', real=True)  # Chord of element airfoil
V_rel = Symbol('V_rel') # sqrt(u**2 + v_radial**2)

norm = rho*V_rel**2*c/2
alpha = phi - theta

L = norm*C_L    # Lift Force per unit length of prop
D = norm*C_D    # Drag Force per unit length of prop

F_N = L*cos(phi) + D*sin(phi)
F_T = L*sin(phi) + D*cos(phi)

C_n = F_N / norm
C_t = F_T / norm


B = Symbol('B', real=True)  # Number of blades

# Expressions for Thrust & Torque
dT_2 = B*F_N*dr
dM_2 = B*F_T*r*dr

dT_2 = dT_2.subs(sin(phi), u/V_rel)
dT_2 = dT_2.subs(cos(phi), v_radial/V_rel)

dT_2 = dT_2.subs(u_subs)
dT_2 = dT_2.subs(v_subs)
dM_2 = dM_2.subs(u_subs)


pprint(simplify(dT_2))
pprint(simplify(dM_2))

solnT = simplify(solve(Eq(dT, dT_2), a))
pprint(solnT)
