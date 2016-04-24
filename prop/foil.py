import numpy as np


class Foil(object):
    def __init__(self, chord, angle_of_attack):
        self.chord = chord
        self.aoa = angle_of_attack

    ''' Calculate Reynolds number from air density rho
        and kinematic ciscoscity (nu)
        
        rho - density of air  kg/m3
        nu  - kinematic viscoscity m^2/s
    '''
    def Reynolds(self, velocity, rho=1.225, nu=15.11e-6):
        L = self.chord
        return rho*velocity*L/nu
      
      
    def __repr__(self):
      return "ch=%f, a=%f" % (self.chord, self.aoa *180 / np.pi)
  
  
  
    def get_points(self, n):
        ''' Return a list of x,y coordinates for the foil
        '''
        return None


class NACA4Foil(Foil):
    def __init__(self, chord, thickness, m=0.0, p=0.4, angle_of_attack=0.0):
        Foil.__init__(self,chord, angle_of_attack)
        self.thickness = thickness
        self.m = m
        self.p = p

      
    def __repr__(self):
      return "ch=%f, a=%f" % (self.chord, self.aoa *180 / np.pi)
  
  
    def get_points(self, n):
        ''' Return a list of x,y coordinates for the foil
            http://www.aerospaceweb.org/question/airfoils/q0041.shtml
        '''
        
        t = self.thickness
        p = self.p
        m = self.m
        
        
        x = np.linspace(0, 1.0, n)
      
        yt = 5.0*t*(0.2969*np.sqrt(x) + \
            -0.1260*(x) + \
            -0.3516*(x**2) + \
             0.2843*(x**3) + \
            -0.1015*(x**4))

        ## TODO complete the cambered calculations below.
        
        yc = (m / (p**2)) * (2.0*p*x - x**2) 
        yc2 = (m / ((1.0 - p)**2)) * (1.0 - 2.0*p + 2*p*x - x**2)
        yc[x > p] = yc2[x > p]
        
        dyc=m*(2.0*p - 2*x)/p**2
        dyc[x > p]=(2*m*(p - x)/(p - 1.0)**2)[x > p]
        
        theta = np.arctan(dyc)
        
        xu = x - yt*np.sin(theta)
        yu = yc + yt*np.cos(theta)
        
        xl = x + yt*np.sin(theta)
        yl = yc - yt*np.cos(theta)
        
        c = self.chord
        return [[xl*c,yl*c],[xu*c,yu*c]]
    
        # return [[x,y],[x,-y]]

if __name__ == "__main__":
    
    f = NACA4Foil(chord=0.1, thickness=0.15, m=0.02, p=0.4)
    pt, pb = f.get_points(200)
    import matplotlib.pyplot as plt
    plt.plot(pt[0], pt[1])
    plt.plot(pb[0], pb[1])
    plt.show()
    print pt[0]
    