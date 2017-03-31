from foil import Foil

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
        ''' Return a list of x,y coordinates for the foil
            NACA report 460
            
            The zero in the x axis is shifted to the center of pressure (chord / 4)
        '''
        xu, yu, xl, yl = self.load_selig('foils/ara_d_10.dat')

        c = self.chord
        return [[xl[::5]*c,yl[::5]*c],[xu[::5]*c,yu[::5]*c]]
    
if __name__ == "__main__":
    
    f = ARAD_10_Foil(chord=0.1)
    #f = Foil(chord=0.1, thickness=0.15)
    f.set_trailing_edge(0.01)
    print f
    print f.hash()
    f.plot()
    
