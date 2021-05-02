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

class ARADFoil_Old(Foil):
    ''' Interpolate between thickness 0.06 and 0.2 '''
    def __init__(self, chord, thickness):
        Foil.__init__(self,chord, thickness)
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

        if (False):
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

from scipy.interpolate import NearestNDInterpolator, LinearNDInterpolator, CloughTocher2DInterpolator

g_linterp = None
g_uinterp = None
g_x0 = None
g_x1 = None

class ARADFoil(Foil):
    ''' Interpolate between thickness 0.06 and 0.2 '''
    def __init__(self, chord, thickness):
        Foil.__init__(self,chord, thickness)
        self.linterp, self.uinterp, x0, x1 = ARADFoil.load_interpolator()
        self.xl = np.linspace(x0, x1, 60)
        self.xu = np.linspace(x0, x1, 60)
        t_pts = np.ones(60)*thickness
        #print t_pts
        self.yl = self.linterp(np.transpose([t_pts, self.xl]))
        self.yu = self.uinterp(np.transpose([t_pts, self.xu]))
        #print self.xl, self.yl
        #print self.xu, self.yu
        #print x0, x1
        self.init_te = (self.yu[-1] - self.yl[-1])

    @staticmethod
    def polyfit(x, y):
        coeff = np.polyfit(x, y, 12)
        return np.poly1d(coeff)

    @staticmethod
    def load_interpolator():
        global g_linterp, g_uinterp, g_x0, g_x1
        if g_linterp is not None:
            return g_linterp, g_uinterp, g_x0, g_x1
        
        files = ['foils/ara_d_6.dat', 'foils/ara_d_10.dat', 'foils/ara_d_13.dat', 'foils/ara_d_20.dat']
        thickness = np.array([0.06, 0.10, 0.13, 0.2])
        lpts = []
        lval = []
        upts = []
        uval = []
        # Lower Bound, linear interpolate here from the 6% foil
        xl, yl, xu, yu = Foil.load_selig('foils/ara_d_6.dat')
        l_interp = ARADFoil.polyfit(xl, yl)
        u_interp = ARADFoil.polyfit(xu, yu)
        
        beta = np.linspace(0, np.pi, 90)    # Use cosine spacing of points.
        x = (1.0 - np.cos(beta))/2


        for t in np.linspace(0.0, 0.04, 7):
            l = l_interp(x)
            u = u_interp(x)
            for xx, ll, uu in zip(x, l, u):
                lpts.append([t, xx])
                upts.append([t, xx])
                lval.append(ll*t/0.06)
                uval.append(uu*t/0.06)

        for t, fname in zip(thickness, files):
            xl, yl, xu, yu = Foil.load_selig(fname)
            l_interp = ARADFoil.polyfit(xl, yl)
            u_interp = ARADFoil.polyfit(xu, yu)
            l = l_interp(x)
            u = u_interp(x)
            for xx, ll, uu in zip(x, l, u):
                lpts.append([t, xx])
                upts.append([t, xx])
                lval.append(ll)
                uval.append(uu)
        
        # Upper Bound is a circle
        xl, yl, xu, yu = Foil.load_selig('foils/ara_d_20.dat')
        l_interp = ARADFoil.polyfit(xl, yl)
        u_interp = ARADFoil.polyfit(xu, yu)
        for t in np.linspace(0.25, 1.0, 9):
            l = l_interp(x)
            u = u_interp(x)
            for xx, ll, uu in zip(x, l, u):
                lpts.append([t, xx])
                upts.append([t, xx])
                lval.append(ll*t/0.2)
                uval.append(uu*t/0.2)

        lpts = np.array(lpts)
        upts = np.array(upts)
        lval = np.array(lval)
        uval = np.array(uval)
        g_linterp = CloughTocher2DInterpolator(lpts, lval)
        g_uinterp = CloughTocher2DInterpolator(upts, uval)
        g_x0 = xl[0]
        g_x1 = xl[-1]
        
        return g_linterp, g_uinterp, g_x0, g_x1

    def hash(self):
        ''' Generate a unique hash for this foil'''
        return "ARAD_I %5.2f,%5.2f" % (self.thickness, self.trailing_edge)

    def __repr__(self):
        hsh = self.hash()
        return "ARAD_I ch={:5.1f}mm, thickness={:4.2f}%  depth={:4.2}mm te={:4.3f} hsh={}".format(self.chord*1000, self.thickness*100, \
            (self.chord*self.thickness)*1000, self.trailing_edge, hsh)
  
  
    def get_shape_points(self, n):
        #return [self.xl, self.yl], [self.xu, self.yu]
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

        if (False):
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
    import matplotlib.pyplot as plt

    thickness = np.linspace(0.3 / 1000, 5.0/1000, 5)
    for t in thickness:
        f = ARADFoil(chord=chord, thickness=t/chord)
        #f = ARADFoil(chord=chord, thickness=t/chord)
        f.set_trailing_edge(0.1 / 1000)
        print(f)
        print(f.hash())
        pb, pt = f.get_points(60, rotation_angle=0.0)
        plt.plot(pt[0], pt[1], '.', label='top')
        plt.plot(pb[0], pb[1], '.', label='bottom')
    plt.show()
    
