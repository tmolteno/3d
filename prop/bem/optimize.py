from numpy import pi, sin, cos, tan, arctan, degrees, sqrt, radians, arange

def C_lift(alpha):
    Clo = 2.0 * pi * alpha 
    return Clo

def C_drag(alpha):
    return 1.28 * sin(alpha)

def iterate(dv, a_prime, theta, omega, r, u_0, c, B):
    u_1 = u_0 + 2*dv
    u = u_0 + dv
    v = 2.0*omega*r*(1.0 - a_prime)
    
    phi = arctan(u/v)
    
    alpha = theta - phi
    C_D = C_drag(alpha)
    C_L = C_lift(alpha)
    #print u, v, degrees(theta), degrees(phi), degrees(alpha), C_D, C_L
    dv = B*c*u*(-C_D*tan(phi) + C_L)/(8*pi*r*sin(phi)*tan(phi))
    #print u_0, u, u_1
    a_prime_new =  B*c*(C_D + C_L*tan(phi))/(B*C_D*c + B*C_L*c*tan(phi) + 8*pi*r*sin(phi))

    return dv, a_prime_new

def bem(theta, rpm, r, u_0, c, B):

    rps = rpm / 60.0
    omega = rps * 2 * pi

    err_min = 1e6

    for dv in arange(1.0, 50.0, 0.2):
        for a_prime in arange(0.0, 0.5, 0.01):
            dv2, a_prime2 = iterate(dv, a_prime, theta, omega, r, u_0, c, B)
            err = abs(dv - dv2)/dv + 10.0*abs(a_prime - a_prime2)
            if (err < err_min):
                dv_guess = dv
                a_prime_guess = a_prime
                err_min = err
            #print dv_guess, dummy

    #print dv_guess, a_prime_guess
    dv = dv_guess
    a_prime = a_prime_guess
    while (True):
        dv2, a_prime2 = iterate(dv,a_prime, theta, omega, r, u_0, c, B)
        err = abs(dv - dv2)/dv + 10.0*abs(a_prime - a_prime2)
        if (abs(err) < 0.0001):
            break
        dv += (dv2 - dv)/20
        a_prime += (a_prime2 - a_prime)/20

    return (dv2 + dv)/2, (a_prime2 + a_prime)/2



dv, a_prime = bem(theta = radians(5.0), rpm = 15000.0, B = 3, c = 0.01, r = 0.05, u_0 = 0.0)
print("dv={}, a_prime={} ".format(dv, a_prime))
