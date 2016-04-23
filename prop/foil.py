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
    def __init__(self, chord, thickness, m=0.0, p=0.25, angle_of_attack=0.0):
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
        
        c = self.chord
        t = self.thickness
        p = self.p
        m = self.m
        
        
        x = np.linspace(0, self.chord, n)
        xc = np.linspace(0, 1.0, n)
      

        a = 0.2969*np.sqrt(xc)
        b = -0.1260*(xc)
        c = -0.3516*(xc**2)
        d = 0.2843*(xc**3)
        e = -0.1015*(xc**4)
        
        y = 5.0*t*(a+b+c+d+e)

        ## TODO complete the cambered calculations below.
        
        yc = (m * x / (p**2)) * (2.0*p - xc) 
        yc[xc > p] = ((m*(c-x) / ((1.0 - p)**2)) * (1.0 + xc - 2.0*p))[xc > p]

        dyc = 2.0 * m * (p - xc) / (p**2)
        dyc[xc > p] = (2.0*m * (p - xc) / ((1.0 - p)**2))[xc > p]
        
        theta = np.arctan(dyc)
        xu = x - yc*np.sin(theta)
        yu = y + yc*np.cos(theta)
        
        xl = x + yc*np.sin(theta)
        yl = y - yc*np.cos(theta)
        
        return [[xl,yl],[xu,yu]]
    
        # return [[x,y],[x,-y]]

if __name__ == "__main__":
    f = NACA4Foil(0.1, 0.1)
    pt, pb = f.get_points(200)
    import matplotlib.pyplot as plt
    plt.plot(pt[0], pt[1])
    plt.plot(pb[0], pb[1])
    plt.show()
    print pt[0]
    