from sympy import *

m = Symbol('m')
p = Symbol('p')
x = Symbol('x')
c = Symbol('c')
xc = x / c

yc = (m / (p**2)) * (2.0*p*x - x**2) 
yc2 = (m / ((1.0 - p)**2)) * (1.0 - 2.0*p + 2*p*x - x**2)
       
pprint(simplify(yc))
pprint(simplify(yc2))

print "dyc=%s" % simplify(diff(yc,x))
print "dyc[x > p]=(%s)[x > p]" % simplify(diff(yc2,x))