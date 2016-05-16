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

import sqlite3

class XfoilSimulatedFoil(SimulatedFoil):
  
    def __init__(self, foil):
        SimulatedFoil.__init__(self, foil)
        print "Creating XFOIL Simulator %s" % foil
        self.hash = foil.hash()
        conn = sqlite3.connect('foil_simulator.db')
        c = conn.cursor()
        self.db_id = c.execute("SELECT f.id FROM foil f WHERE (f.hash=?)", (self.hash,)).fetchone()[0]
        if self.db_id == None:
            c.execute("INSERT INTO foil(hash) VALUES (?)", (self.hash,))
            c.execute("SELEC id FROM foil WHERE (hash=?)", (self.hash,))
            self.db_id = c.fetchone()[0]
            print self.db_id
        else:
            print "Already in table with id %s" % self.db_id
        conn.commit()
        conn.close()
        self.polars = {}
        
    def read_from_db(self):
        conn = sqlite3.connect('foil_simulator.db')
        c = conn.cursor()
        for fow in c.execute("SELECT s.re, s.id FROM foil f, simulation s WHERE (f.hash=?) AND (f.id = s.foil_id)", (self.hash,)):
            polars = []
            key = "%5.2f" % row['re']
            for pol in c.execute("SELECT s.re FROM polar p WHERE (p.sim_id=?) AND (f.id = s.foil_id)", (row['id'],)):
                polars.append()
            self.polars[key] = polars
        conn.commit()
        conn.close()

    def get_cl(self, v, alpha):
        try:
            cl, cd = self.get_polars(v)
        except ValueError:
            print "Failure"
            return  2.0 * np.pi * alpha
        return cl(alpha)

    def get_cd(self, v, alpha):
        try:
            cl, cd = self.get_polars(v)
        except ValueError:
            print "Failure"
            return 0.5
        return cd(alpha)

    def get_polars(self, velocity):
        re = self.foil.Reynolds(velocity)
        
        # Check if we're in the databse
        conn = sqlite3.connect('foil_simulator.db')
        c = conn.cursor()
        print self.db_id
        c.execute("SELECT s.id FROM simulation s WHERE (s.foil_id=?) AND (s.re = ?)", (self.db_id, re, ))
        result = c.fetchone()
        if (result != None):
            # Read from database
            sim_id = result[0]
            alpha = []
            cl = []
            cd = []
            for pol in c.execute("SELECT p.alpha, p.cl, p.cd FROM polar p WHERE (p.sim_id=?)", (sim_id,)):
                alpha.append(pol[0])
                cl.append(pol[1])
                cd.append(pol[2])
            cl_poly = np.poly1d(np.polyfit(alpha, cl, 4))
            cd_poly = np.poly1d(np.polyfit(alpha, cd, 4))
            key = "%5.2f" % re
            self.polars[key] = [cl_poly, cd_poly]
            conn.commit()
            conn.close()
            return self.polars[key]
        
        if (self.foil.Reynolds(velocity) < 20000.0):
            alpha = np.radians(np.linspace(-5, 40, 20))
            cl = 2.0 * np.pi * alpha

            cd = 1.28 * np.sin(alpha)
           


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
    
        # Insert into database
        conn = sqlite3.connect('foil_simulator.db')
        c = conn.cursor()
        c.execute("INSERT INTO simulation(foil_id, re) VALUES (?,?)", (self.db_id, re, ))
        c.execute("SELECT id FROM simulation WHERE (foil_id=?) AND (re=?)", (self.db_id, re, ))
        sim_id = c.fetchone()[0]

        for i, a in enumerate(alfa):
            c.execute("INSERT INTO polar(sim_id, alpha, cl, cd) VALUES (?,?,?,?)", (sim_id, a, cl[i], cd[i]))
        conn.commit()
        conn.close()
        return self.get_polars(velocity)

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
