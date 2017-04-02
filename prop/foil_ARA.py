from foil import Foil

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
        if (self.thickness <= 0.06):
            self.xu, self.yu, self.xl, self.yl = self.load_selig('foils/ara_d_6.dat')
            self.yu *= self.thickness / 0.06
            self.yl *= self.thickness / 0.06
        elif (self.thickness <= 0.10):
            self.xu, self.yu, self.xl, self.yl = self.load_selig('foils/ara_d_10.dat')
            self.yu *= self.thickness / 0.1
            self.yl *= self.thickness / 0.1
        elif (self.thickness <= 0.13):
            self.xu, self.yu, self.xl, self.yl = self.load_selig('foils/ara_d_13.dat')
            self.yu *= self.thickness / 0.13
            self.yl *= self.thickness / 0.13
        else:
            self.xu, self.yu, self.xl, self.yl = self.load_selig('foils/ara_d_20.dat')
            self.yu *= self.thickness / 0.2
            self.yl *= self.thickness / 0.2

    def hash(self):
        ''' Generate a unique hash for this foil'''
        return "ARAD2 %5.2f,%5.2f" % (self.thickness, self.trailing_edge)

    def __repr__(self):
      return "ARAD ch={:5.1f}mm, thickness={:4.2f}%  depth={:4.2}mm te={:4.3f}".format(self.chord*1000, self.thickness*100, \
          (self.chord*self.thickness)*1000, self.trailing_edge)
  
  
    def get_shape_points(self, n):
        c = self.chord
        
        return [[self.xl*c,self.yl*c],[self.xu*c,self.yu*c]]

if __name__ == "__main__":
    
    f = ARADFoil(chord=0.1, thickness=0.05)
    f.set_trailing_edge(0.01)
    print f
    print f.hash()
    f.plot()
    
