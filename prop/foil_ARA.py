from foil import Foil
from scipy.interpolate import PchipInterpolator
import numpy as np

class ARAD_6_Foil(Foil):
    '''         ARA-D 20% AIRFOIL
    '''
    def __init__(self, chord):
        Foil.__init__(self,chord, chord*0.06)

    def hash(self):
        ''' Generate a unique hash for this foil'''
        return "ARAD6 %5.2f,%5.2f" % (self.thickness, self.trailing_edge)

    def __repr__(self):
      return "ch=%f, te=%4.3f, ARAD6 %d" % (self.chord, self.trailing_edge, (self.thickness*100))
  
  
    def get_shape_points(self, n):
        xu, yu, xl, yl = self.load_selig('foils/ara_d_6.dat')
        c = self.chord
        
        return [[xl*c,yl*c],[xu*c,yu*c]]

class ARAD_10_Foil(Foil):
    '''         ARA-D 10% AIRFOIL
    '''
    def __init__(self, chord):
        Foil.__init__(self,chord, chord*0.1)

    def hash(self):
        ''' Generate a unique hash for this foil'''
        return "ARAD10 %5.2f,%5.2f" % (self.thickness, self.trailing_edge)

    def __repr__(self):
      return "ch=%f, te=%4.3f, ARAD10 %d" % (self.chord, self.trailing_edge, (self.thickness*100))
  
  
    def get_shape_points(self, n):
        xu, yu, xl, yl = self.load_selig('foils/ara_d_10.dat')
        c = self.chord
        
        return [[xl*c,yl*c],[xu*c,yu*c]]
    
class ARAD_13_Foil(Foil):
    '''         ARA-D 13% AIRFOIL
    '''
    def __init__(self, chord):
        Foil.__init__(self,chord, chord*0.13)

    def hash(self):
        ''' Generate a unique hash for this foil'''
        return "ARAD13 %5.2f,%5.2f" % (self.thickness, self.trailing_edge)

    def __repr__(self):
      return "ch=%f, te=%4.3f, ARAD13 %d" % (self.chord, self.trailing_edge, (self.thickness*100))
  
  
    def get_shape_points(self, n):
        xu, yu, xl, yl = self.load_selig('foils/ara_d_13.dat')
        c = self.chord
        
        return [[xl*c,yl*c],[xu*c,yu*c]]
    
class ARAD_20_Foil(Foil):
    '''         ARA-D 20% AIRFOIL
    '''
    def __init__(self, chord):
        Foil.__init__(self,chord, chord*0.2)

    def hash(self):
        ''' Generate a unique hash for this foil'''
        return "ARAD20 %5.2f,%5.2f" % (self.thickness, self.trailing_edge)

    def __repr__(self):
      return "ch=%f, te=%4.3f, ARAD20 %d" % (self.chord, self.trailing_edge, (self.thickness*100))
  
  
    def get_shape_points(self, n):
        xu, yu, xl, yl = self.load_selig('foils/ara_d_20.dat')
        c = self.chord
        
        return [[xl*c,yl*c],[xu*c,yu*c]]

class ARADFoil(Foil):
    ''' Interpolate between thickness 0.06 and 0.2 '''
    def __init__(self, chord, thickness):
        Foil.__init__(self,chord, thickness)
        t = np.array([0.06, 0.10, 0.13, 0.2])
        if (self.thickness <= 0.06):
            self.xl, self.yl, self.xu, self.yu = self.load_selig('foils/ara_d_6.dat')
            self.yu *= self.thickness / 0.06
            self.yl *= self.thickness / 0.06
        elif (self.thickness <= 0.10):
            self.xl, self.yl, self.xu, self.yu = self.load_selig('foils/ara_d_10.dat')
            self.yu *= self.thickness / 0.1
            self.yl *= self.thickness / 0.1
        elif (self.thickness <= 0.13):
            self.xl, self.yl, self.xu, self.yu = self.load_selig('foils/ara_d_13.dat')
            self.yu *= self.thickness / 0.13
            self.yl *= self.thickness / 0.13
        else:
            self.xl, self.yl, self.xu, self.yu= self.load_selig('foils/ara_d_20.dat')
            self.yu *= self.thickness / 0.2
            self.yl *= self.thickness / 0.2
        self.init_te = (self.yu[-1] - self.yl[-1])

    def hash(self):
        ''' Generate a unique hash for this foil'''
        return "ARAD2 %5.2f,%5.2f" % (self.thickness, self.trailing_edge)

    def __repr__(self):
        hsh = self.hash()
        return "ARAD ch={:5.1f}mm, thickness={:4.2f}%  depth={:4.2}mm te={:4.3f} hsh={}".format(self.chord*1000, self.thickness*100, \
            (self.chord*self.thickness)*1000, self.trailing_edge, hsh)
  
  
    def get_shape_points(self, n):
        c = self.chord
        # Interpolate the points 
        l_interp = PchipInterpolator(self.xl, self.yl)
        u_interp = PchipInterpolator(self.xu, self.yu)

        n = n*5
        beta = np.linspace(0, np.pi, n)    # Use cosine spacing of points.
        x = (1.0 - np.cos(beta))/2

        xl = x
        xu = x
        y_offset = np.linspace(0, (self.trailing_edge - self.init_te)/2, n)

        yl = l_interp(xl) - y_offset
        yu = u_interp(xu) + y_offset

        if (True):
            max_x = xu[np.argmax(yu)] #0.3
            if (max_x > 0.5):
                max_x = 0.5
            max_y = np.max(yu)
            # print np.max(yu), max_y, np.argmax(yu) 
            
            xu = xu - max_x
            xl = xl - max_x
            
            yu = yu - max_y
            yl = yl - max_y
        
        yu[0] = yl[0]
        
        return [[xl[::5]*c,yl[::5]*c],[xu[::5]*c,yu[::5]*c]]

if __name__ == "__main__":
    chord = 12.0 / 1000 
    thickness = 1.0 / 1000
    f = ARADFoil(chord=chord, thickness=thickness/chord)
    f.set_trailing_edge(0.1 / 1000)
    print f
    print f.hash()
    f.plot()
    
