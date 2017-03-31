from foil import Foil

class ARAD_6_Foil(Foil):
    '''         ARA-D 20% AIRFOIL
    '''
    def __init__(self, chord):
        Foil.__init__(self,chord, chord*0.1)

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
        Foil.__init__(self,chord, chord*0.1)

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
        Foil.__init__(self,chord, chord*0.1)

    def hash(self):
        ''' Generate a unique hash for this foil'''
        return "ARAD20 %5.2f,%5.2f" % (self.thickness, self.trailing_edge)

    def __repr__(self):
      return "ch=%f, te=%4.3f, ARAD20 %d" % (self.chord, self.trailing_edge, (self.thickness*100))
  
  
    def get_shape_points(self, n):
        xu, yu, xl, yl = self.load_selig('foils/ara_d_20.dat')
        c = self.chord
        
        return [[xl*c,yl*c],[xu*c,yu*c]]
    
if __name__ == "__main__":
    
    f = ARAD_20_Foil(chord=0.1)
    f.set_trailing_edge(0.01)
    print f
    print f.hash()
    f.plot()
    
