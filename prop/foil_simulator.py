import xfoil 
import numpy as np

class SimulatedFoil:
    def __init__(self, foil):
      self.foil = foil
      
      
    def get_cd(self, v, alpha):
      return None
    
    def get_cl(self, v, alpha):
      return None
    
class PlateSimulatedFoil(SimulatedFoil):
  
    def get_cl(self, v, alpha):
        return 2.0 * np.pi * alpha

    def get_cd(self, v, alpha):
        return 1.28 * np.sin(alpha)

from random import choice
from string import ascii_uppercase
import os

class XfoilSimulatedFoil(SimulatedFoil):
  
    def __init__(self, foil):
        SimulatedFoil.__init__(self, foil)
        print "Creating Sumulator %s" % foil
        hash = foil.hash()
        self.polars = {}
        
    def get_cl(self, v, alpha):
        cl, cd = self.get_polars(v)
        return cl(alpha)

    def get_cd(self, v, alpha):
        cl, cd = self.get_polars(v)
        return cd(alpha)

    def get_polars(self, velocity):
        key = "%5.2f" % velocity
        if (key in self.polars):
            return self.polars[key]
        
        print "get_polars(%s)" % key
        
        if (self.foil.Reynolds(velocity) < 20000.0):
            alpha = np.radians(np.linspace(-5, 40, 20))
            cl = 2.0 * np.pi * alpha

            cd = 1.28 * np.sin(alpha)

            cl_poly = np.poly1d(np.polyfit(alpha, cl, 4))
            cd_poly = np.poly1d(np.polyfit(alpha, cd, 4))
            self.polars[key] = [cl_poly, cd_poly]
            return self.polars[key]

        ''' Use XFOIL to simulate the performance of this get_shape
        '''
        pl, pu = self.foil.get_shape_points(n=80)
        
        ''' This contains only the X,Y coordinates, which run from the 
            trailing edge, round the leading edge, back to the trailing edge 
            in either direction:
        '''
        xcoords = np.concatenate((pl[0][::-1], pu[0]), axis=0)
        ycoords = np.concatenate((pl[1][::-1], pu[1]), axis=0)
        
        # Chop off overhang.
        limit = xcoords <= xcoords[0]
        xcoords = xcoords[limit]
        ycoords = ycoords[limit]
        #xcoords = np.append(xcoords, xcoords[0] )
        #ycoords = np.append(ycoords, ycoords[0] )
        
        coordslist = np.array((xcoords, ycoords)).T
        coordstrlist = ["{:.6f} {:.6f}".format(coord[0], coord[1])
                        for coord in coordslist]
        # Join with linebreaks in between
        points = '\n'.join(coordstrlist)
        
        Re = self.foil.Reynolds(velocity)

        # Save points to a file
        randstr = ''.join(choice(ascii_uppercase) for i in range(20))
        filename = "parsec_{}.dat".format(randstr)
        with open(filename, 'w') as af:
            af.write(points)
            
        # Let Xfoil do its magic
        alfa = (0, 45, 2.1)
        results = xfoil.oper_visc_alpha(filename, alfa, Re, Mach=self.foil.Mach(velocity),
                                        iterlim=88, show_seconds=3)
        labels = results[1]
        values = results[0]
        
        polar = {}
        for label in labels:
            polar[label] = []
        
        for v in values:
            for label, value in zip(labels, v):
                polar[label].append(value)
        
        os.remove(filename)
                
        cl = np.array(polar['CL'])
        cd = np.array(polar['CD'])
        top_xtr = np.array(polar['Top_Xtr'])
        alfa = np.radians(polar['alpha'])

        cl_poly = np.poly1d(np.polyfit(alfa, cl, 4))
        cd_poly = np.poly1d(np.polyfit(alfa, cd, 4))

        self.polars[key] = [cl_poly, cd_poly]
        return self.polars[key]

if __name__ == "__main__":
    from foil import NACA4
    f = NACA4(chord=0.1, thickness=0.15, m=0.06, p=0.4, angle_of_attack=8.0 * np.pi / 180.0)
    f.set_trailing_edge(0.01)
    fs = XfoilSimulatedFoil(f)
    
    alpha = np.radians(np.linspace(0, 40, 20))
    v = 3
    cl = []
    cd = []
    for a in alpha:
     cd.append(fs.get_cd(v, a))
     cl.append(fs.get_cl(v, a))

    import matplotlib.pyplot as plt
    plt.plot(alpha, cl)
    plt.plot(alpha, cd)
    plt.show()
