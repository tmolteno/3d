'''
    Prop Design Code
    
    Author Tim Molteno tim@elec.ac.nz
    
    Copyright 2016-2017

'''
import numpy as np

import logging
logger = logging.getLogger(__name__)

class Foil(object):
    def __init__(self, chord, thickness):
        self.chord = chord
        self.thickness = thickness
        self.trailing_edge = 0.0

    def modify_chord(self, c):
        old_chord = self.chord
        self.chord = c
        #self.thickness = self.thickness*old_chord / c
        #self.trailing_edge = self.trailing_edge*old_chord / c

    ''' Calculate Reynolds number from air density rho
        and kinematic ciscoscity (nu)
        
        rho - density of air  kg/m3
        nu  - kinematic viscoscity m^2/s
    '''
    def Reynolds(self, velocity, rho=1.225, nu=15.11e-6):
        L = self.chord
        return rho*velocity*L/nu
      
    def Mach(self, velocity, rho=1.225, nu=15.11e-6):
        return velocity / 330.0
    
    def polar_aux(self, v, rho=1.225, nu=15.11e-6):
        return 0.5*rho*v*v*self.chord
     
    def lift_per_unit_length(self, v, cl):
        return self.polar_aux(v) * cl

    def drag_per_unit_length(self, v, cd):
        return self.polar_aux(v) * cd
    
    def hash(self):
        ''' Generate a unique hash for this foil'''
        pl, pu = self.get_shape_points(10)
        return "%s" % (np.sum(pu[1]) + np.sum(pl[1]))
    
    def __repr__(self):
      return "ch=%f, a=%f" % (self.chord, self.thickness)
  
    def set_trailing_edge(self, te):
        self.trailing_edge = te / self.chord
  
    def get_shape_points(self, n):
        ''' Return a list of x,y coordinates for the foil with zero angle of attack
        '''
        x = np.linspace(0, self.chord, n)
        y = self.thickness*self.chord*np.ones(n)
        return [[x,-y],[x,y]]
    
    @staticmethod
    def load_selig(filename):
        ''' Load points from a file and normalize '''
        fd = open(filename, 'r')
        seligFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        points = seligFile.split('\n')

        # Execute every command from the input file
        xu = []
        yu = []
        xl = []
        yl = []
        x_prev = 9e99
        import re
        expr = re.compile(r'[0-9.-]+')
        for p in points:
            try:
                pts = re.findall(expr, p)
                x0 = float(pts[0])
                y0 = float(pts[1])
                if x0 < x_prev:
                    xu.append(x0)
                    yu.append(y0)
                else:
                    xl.append(x0)
                    yl.append(y0)
                x_prev = x0

                    
            except:
                logger.info("No information on line {}".format(p))
        #xl.reverse()
        #yl.reverse()
        xu.reverse()
        yu.reverse()
        return np.array(xl),np.array(yl),np.array(xu),np.array(yu)

    def get_points(self, n, rotation_angle):
        pl, pu = self.get_shape_points(n)
        xl, yl = pl
        xu, yu = pu
        
        y0 = 0.0
        x0 = 0.67*(np.max(xu)-np.min(xu))
        
        xl,yl = self.rotate(xl-x0, yl-y0, rotation_angle)
        xu,yu = self.rotate(xu-x0, yu-y0, rotation_angle)
        
        return [[xl,yl],[xu,yu]]

    
    ''' Return the lowest and highest point in the foil '''
    def get_bounding_box(self, theta):
        pl, pu = self.get_points(50, theta)
        xu, yu = pu
        xl, yl = pl

        x = np.concatenate([xl, xu])
        y = np.concatenate([yl, yu])
        
        return np.min(x), np.max(x), np.min(y), np.max(y)
    
    def get_max_chord(self, x_limit, y_limit, theta):
        ''' Find the largest chord that could fit the foil into a box'''
        x0, x1, y0, y1 = self.get_bounding_box(theta)
        print(("get_bounding_box({},{},{},{},".format(x0, x1, y0, y1)))
        dy = y1 - y0
        dx = x1 - x0
        
        print(("get_max_chord({},{},{}) dx={}, dy={}".format( x_limit, y_limit, theta, dx, dy)))
        y_scale = y_limit/dy
        x_scale = x_limit/dx
        
        return self.chord*min(x_scale, y_scale)
    
    def rotate(self, x, y, theta):
        ''' Rotate the points to the angle of attack around'''
        x2 = x*np.cos(theta) + y*np.sin(theta)
        y2 = -x*np.sin(theta) + y*np.cos(theta)
        return [x2,y2]

    def plot(self):
        pb, pt = self.get_points(60, rotation_angle=0.0)
        import matplotlib.pyplot as plt
        plt.plot(pt[0], pt[1], 'x', label='top')
        plt.plot(pb[0], pb[1], 'o', label='bottom')
        plt.legend()
        plt.show()

'''
   Flat plate has analytic polars. Useful for simple testing
'''
class FlatPlate(Foil):
  
    def __init__(self, chord):
        Foil.__init__(self,chord)

  

class NACA4(Foil):
    '''
    Foil generated from the NACA 4 series
    '''
    
    def __init__(self, chord, thickness, m=0.0, p=0.4):
        ''' 
            Parameters:
              m - maximum camber as a percentage of the chord.
              p - location of maximum camber as a percentage of chord line from leading edge
        '''
        Foil.__init__(self,chord, thickness)
        self.m = m
        self.p = p

    def hash(self):
        ''' Generate a unique hash for this foil'''
        
        return "%5.2f,%5.2f,%5.2f, %5.2f" % (self.m, self.p, self.thickness, self.trailing_edge)

    def __repr__(self):
      return "ch=%f, te=%4.3f, NACA%02d%02d%2d" % (self.chord, self.trailing_edge, (self.m*100), (self.p*10) , (self.thickness*100))
  
  
    def get_shape_points(self, n):
        ''' Return a list of x,y coordinates for the foil
            NACA report 460
            
            The zero in the x axis is shifted to the center of pressure (chord / 4)
        '''
        
        t = self.thickness
        p = self.p
        m = self.m
        
        n = n*5
        beta = np.linspace(0, np.pi, n)    # Use cosine spacing of points.
        x = (1.0 - np.cos(beta))/2
        
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
        
        if (False):
            # Translate to a system where 0,0 is the max_x, max_y (these are defined by p and t)
            # max(yt) = 0.5, occurs at x=.2998
            # max(dyc) = p
            max_x = xu[np.argmax(yu)] #0.3
            if (max_x > 0.5):
                max_x = 0.5
            max_y = np.max(yu)
            # print np.max(yu), max_y, np.argmax(yu) 
            
            xu = xu - max_x
            xl = xl - max_x
            
            yu = yu - max_y
            yl = yl - max_y
        
        c = self.chord
        return [[xl[::5]*c,yl[::5]*c],[xu[::5]*c,yu[::5]*c]]
    
        
if __name__ == "__main__":
    
    f = NACA4(chord=0.1, thickness=0.15, m=0.06, p=0.4)
    #f = Foil(chord=0.1, thickness=0.15)
    f.set_trailing_edge(0.01)
    print(f)
    print(f.hash())
    f.plot()
    
