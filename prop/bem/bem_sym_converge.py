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
dr = Symbol('dr', real=True)

'''
    Velocity at the disk is average of u_0 and u_1. We create a dv factor that 
    Expresses the blade velocity (u) and the wake velocity (u_1) in terms of the
    upstream velocity (u_0) and dv, where
    Wake velocity u_1 = u_0 + 2*dv
    Disk Velocity u = u_0 + dv
'''
dv = Symbol('dv', real=True)
u_1 = u_0 + 2*dv
#u = u_0 + dv


dA = pi*(r + dr)**2 - pi*r**2
m_dot = rho*u*dA
print simplify(m_dot)
print expand(dA, dr)
#m_dot = 2*pi*r*dr*rho*u


dT = m_dot * (u_1 - u_0)


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

#dT_2 = dT_2.subs(V_rel, u / sin(phi))
#dT_2 = simplify(dT_2)

#dM = dM.subs(u, V_rel * sin(phi))
#dM = dM.subs(V_rel, v / cos(phi))
#dM = dM.subs(v, omega*r*(1 - a_prime))
#dM = simplify(dM)

#dM_2 = dM_2.subs(u, V_rel * sin(phi))
#dM_2 = dM_2.subs(V_rel, v / cos(phi))
#dM_2 = dM_2.subs(v, omega*r*(1 - a_prime))
#dM_2 = simplify(dM_2)

print("dT = {}".format(dT))  # Equivalent to 8.4
print("dT_2 = {}".format(dT_2))  # Equivalent to 8.4

solnT = simplify(solveset(dT - dT_2, dv))
pprint(solnT)

print("dv #########################################")
dv_soln = next(iter(solnT))
dv_soln = simplify(dv_soln.subs(V_rel, u/sin(phi)))
dv_soln = simplify(dv_soln.subs(tan(phi), u/v))
dv_soln = simplify(dv_soln.subs(sin(phi), u/sqrt(v**2 + u**2)))
dv_soln = dv_soln.subs([(u, u_0 + dv), (v, omega*r*(1 - a_prime))])
print python(simplify(dv_soln))

# Now calcluate the derivative of dv wrt a_prime and dv.

print("a_prime #########################################")
print("dM = {}".format(dM))  # Equivalent to 8.4
print("dM_2 = {}".format(dM_2))  # Equivalent to 8.4

solnM = simplify(solveset(dM - dM_2, a_prime))
pprint(solnM)

aprime_soln = next(iter(solnM))
aprime_soln = simplify(aprime_soln.subs(V_rel, u/sin(phi)))
aprime_soln = simplify(aprime_soln.subs(tan(phi), u/v))
aprime_soln = simplify(aprime_soln.subs(sin(phi), u/sqrt(v**2 + u**2)))
aprime_soln = aprime_soln.subs([(u, u_0 + dv), (v, omega*r*(1 - a_prime))])

print simplify(aprime_soln)

print("Iterative Solution in 2 DOF")

minfun = ((dv - dv_soln)/dv)**2 + ((a_prime - aprime_soln)/(a_prime+0.01))**2
print "minfun={}".format(minfun)

dmindv= simplify(diff(minfun, dv))
print "dmindv={}".format(dmindv)
dminda= simplify(diff(minfun, a_prime))
print "dminda={}".format(dminda)


#print("Iterative Solution in 3 DOF")

#dv_goal = Symbol('dv_goal', real=True)

#minfun = (dv - dv_goal)**2 + (dv - dv_soln)**2 + (a_prime - aprime_soln)**2
#print "minfun={}".format(minfun)

#dmindv= diff(minfun, dv)
#print "dmindv={}".format(dmindv)
#dminda= diff(minfun, a_prime)
#print "dminda={}".format(dminda)
#dmindtheta= diff(minfun, theta)
#print "dmindtheta={}".format(dmindtheta)


#dm_calc = dM.subs([(tan(phi), u/v), (v, omega*r*(1 - a_prime))])
#print("dM = {}".format(simplify(dm_calc)))  # Equivalent to 8.4
#print("dM_2 = {}".format(dM_2))  # Equivalent to 8.4

#solnM = simplify(solve([Eq(dM, dM_2)], a_prime))
#pprint(solnM)

