from sympy import *

m = Symbol('m')
p = Symbol('p')
x = Symbol('x')
c = Symbol('c')
t = Symbol('t')
xc = x / c

yc = (m / (p**2)) * (2.0*p*x - x**2) 
yc2 = (m / ((1.0 - p)**2)) * (1.0 - 2.0*p + 2*p*x - x**2)
       
pprint(simplify(yc))
pprint(simplify(yc2))

print("dyc=%s" % simplify(diff(yc,x)))
print("dyc[x > p]=(%s)[x > p]" % simplify(diff(yc2,x)))




yt = 5.0*t*(0.2969*sqrt(x) + \
    -0.1260*(x) + \
    -0.3516*(x**2) + \
      0.2843*(x**3) + \
    -0.1015*(x**4))

pprint(yt)

print(solve(diff(yt,x), x))

#x = 0.3
#yt = 5.0*t*(0.2969*sqrt(x) + \
    #-0.1260*(x) + \
    #-0.3516*(x**2) + \
      #0.2843*(x**3) + \
    #-0.1015*(x**4))
#print yt


print(solve(diff(yc,x), x))
