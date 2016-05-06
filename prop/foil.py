import numpy as np

import xfoil
from random import choice
from string import ascii_uppercase

class Foil(object):
    def __init__(self, chord, angle_of_attack):
        self.chord = chord
        self.aoa = angle_of_attack
        self.trailing_edge = 0.0

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
  
    def set_trailing_edge(self, t):
        self.trailing_edge = t
  
    def get_shape_points(self, n):
        ''' Return a list of x,y coordinates for the foil with zero angle of attack
        '''
        x = np.linspace(0, self.chord, n)
        y = 0.001*np.ones(n)
        return [[x,-y],[x,y]]
    
    
    def get_points(self, n):
        pl, pu = self.get_shape_points(n)
        xl, yl = pl
        xu, yu = pu
        xl,yl = self.rotate(xl,yl, self.aoa)
        xu,yu = self.rotate(xu,yu, self.aoa)
        return [[xl,yl],[xu,yu]]

        
    def rotate(self, x, y, theta):
        ''' Rotate the points to the angle of attack around'''
        x2 = x*np.cos(theta) + y*np.sin(theta)
        y2 = -x*np.sin(theta) + y*np.cos(theta)
        return [x2,y2]


    def simulate_coef(self, velocity):
      ''' Use XFOIL to simulate the performance of this get_shape
      '''
      pl, pu = self.get_shape_points(n=30)
      
      ''' This contains only the X,Y coordinates, which run from the 
          trailing edge, round the leading edge, back to the trailing edge 
          in either direction:
      '''
      xcoords = np.concatenate((pl[0][::-1], pu[0]), axis=0)
      ycoords = np.concatenate((pl[1][::-1], pu[1]), axis=0)
      
      coordslist = np.array((xcoords, ycoords)).T
      coordstrlist = ["{:.6f} {:.6f}".format(coord[0], coord[1])
                      for coord in coordslist]
      # Join with linebreaks in between
      points = '\n'.join(coordstrlist)
      
      Re = self.Reynolds(velocity)

      # Save points to a file
      randstr = ''.join(choice(ascii_uppercase) for i in range(20))
      filename = "parsec_{}.dat".format(randstr)
      with open(filename, 'w') as af:
        af.write(points)
        
      # Let Xfoil do its magic
      print self.aoa
      polar = xfoil.oper_visc_alpha(filename, self.aoa * 180 / np.pi, Re,
                                    iterlim=80, show_seconds=0)
      return polar
    
    
class NACA4(Foil):
    '''
    Foil generated from the NACA 4 series
    '''
    
    def __init__(self, chord, thickness, m=0.0, p=0.4, angle_of_attack=0.0):
        ''' 
            Parameters:
              m - maximum camber as a percentage of the chord.
              p - location of maximum camber as a percentage of chord line from leading edge
        '''
        Foil.__init__(self,chord, angle_of_attack)
        self.thickness = thickness
        self.m = m
        self.p = p

      
    def __repr__(self):
      return "ch=%f, a=%f" % (self.chord, self.aoa *180 / np.pi)
  
  
    def get_shape_points(self, n):
        ''' Return a list of x,y coordinates for the foil
            NACA report 460
            
            The zero in the x axis is shifted to the center of pressure (chord / 4)
        '''
        
        t = self.thickness
        p = self.p
        m = self.m
        
        beta = np.linspace(0, np.pi, n)    # Use cosine spacing of points.
        x = (1.0 - np.cos(beta))/2
        print x
        
        y_offset = np.linspace(0, self.trailing_edge/2, n)
      
        yt = 5.0*t*(0.2969*np.sqrt(x) + \
            -0.1260*(x) + \
            -0.3516*(x**2) + \
             0.2843*(x**3) + \
            -0.1036*(x**4)) + y_offset

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
        
        # Translate to a system where 0,0 is the max_x, max_y (these are defined by p and t)
        # max(yt) = 0.5, occurs at x=.2998
        # max(dyc) = p
        max_x = 0.3
        max_y = np.max(yu)
        # print np.max(yu), max_y, np.argmax(yu) 
        
        xu = xu - max_x
        xl = xl - max_x
        
        yu = yu - max_y
        yl = yl - max_y
        
        c = self.chord
        return [[xl*c,yl*c],[xu*c,yu*c]]
    
    def plot(self):
        pt, pb = f.get_points(30)
        import matplotlib.pyplot as plt
        plt.plot(pt[0], pt[1], 'x')
        plt.plot(pb[0], pb[1], 'o')
        plt.show()
        
if __name__ == "__main__":
    
    f = NACA4(chord=0.1, thickness=0.15, m=0.06, p=0.4, angle_of_attack=8.0 * np.pi / 180.0)
    f.set_trailing_edge(0.01)
    f.plot()
    print f.simulate_coef(1.0)
    