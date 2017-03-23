'''
    Simulation Code for Airfoils
    
    Author Tim Molteno tim@elec.ac.nz
    
    Copyright 2016-2017
    
    Two classes are in here. The PlateSimulatedFoil returns C_L and C_D assuming the
    foil is a plate. Its quick and pretty rough.
    
    The XfoilSimulatedFoil uses the xfoil program to generate polars. Its slower and more accurate.
    
    
    TODO: Use some CFD to do the job better?

'''

import xfoil_2 as xfoil
import numpy as np
from scipy.optimize import brentq

class SimulatedFoil:
    def __init__(self, foil):
      self.foil = foil
      
      
    def get_cd(self, v, alpha):
      return None
    
    def get_cl(self, v, alpha):
      return None
    
class PlateSimulatedFoil(SimulatedFoil):
  
    def get_zero_cl_angle(self, v):
        zero = 0.1
        return zero

    def get_cl(self, v, alpha):
        return 2.0 * np.pi * alpha

    def get_cd(self, v, alpha):
        return 1.28 * np.sin(alpha)

from random import choice
from string import ascii_uppercase
import os

import sqlite3
import logging

class XfoilSimulatedFoil(SimulatedFoil):
  
    def __init__(self, foil):
        SimulatedFoil.__init__(self, foil)
        self.hash = foil.hash()
        conn = sqlite3.connect('foil_simulator.db')
        c = conn.cursor()
        result = c.execute("SELECT f.id FROM foil f WHERE (f.hash=?)", (self.hash,)).fetchone()
        if result == None:
            c.execute("INSERT INTO foil(hash) VALUES (?)", (self.hash,))
            c.execute("SELECT id FROM foil WHERE (hash=?)", (self.hash,))
            self.foil_id = c.fetchone()[0]
            logging.info("Creating Foil In Database, %s, id=%d" % (foil, self.foil_id))
        else:
            self.foil_id = result[0]
        conn.commit()
        conn.close()

    def get_zero_cl_angle(self, v):
        cl, cd = self.get_polars(v)
        try:
            zero = brentq(cl, np.radians(-30.0), np.radians(15.0))
        except:
            zero = 0.0
        return zero
        

    def get_cl(self, v, alpha):
        try:
            cl, cd = self.get_polars(v)
        except ValueError:
            logging.info("Failure to get foil polars")
            return  2.0 * np.pi * alpha
        return cl(alpha)

    def get_cd(self, v, alpha):
        try:
            cl, cd = self.get_polars(v)
        except ValueError:
            logging.info("Failure to get foil polars")
            return 0.5
        return cd(alpha)

    def get_polars(self, velocity):
        reynolds = np.round(self.foil.Reynolds(velocity), -4)  # Round to nearest 1000

        # Check if we're in the databse
        conn = sqlite3.connect('foil_simulator.db')
        c = conn.cursor()
        c.execute("SELECT s.id FROM simulation s WHERE (s.foil_id=?) AND (s.reynolds = ?)", (self.foil_id, reynolds, ))
        result = c.fetchone()
        if (result != None):
            # Read from database
            sim_id = result[0]
            logging.info("retrieving from database sim_id=%d, %f" % (sim_id, reynolds))
            alpha = []
            cl = []
            cd = []
            for pol in c.execute("SELECT p.alpha, p.cl, p.cd FROM polar p WHERE (p.sim_id=?)", (sim_id,)):
                alpha.append(pol[0])
                cl.append(pol[1])
                cd.append(pol[2])
            cl_poly = np.poly1d(np.polyfit(alpha, cl, 4))
            cd_poly = np.poly1d(np.polyfit(alpha, cd, 4))
            conn.commit()
            conn.close()
            return [cl_poly, cd_poly]
        
        if (self.foil.Reynolds(velocity) < 20000.0):
            alpha = np.radians(np.linspace(-30, 40, 20))
            cl = 2.0 * np.pi * alpha

            cd = 1.28 * np.sin(alpha)
           

        print "Simulating Foil %s, at Re=%f" % (self.foil, reynolds)
        ''' Use XFOIL to simulate the performance of this get_shape
        '''
        
        #n_points = int(101.0*self.foil.chord / self.foil.trailing_edge) + 30
        #n_points = min(81.0, n_points)
        #n_points = max(61, n_points)
        n_points = 71
        print "N Points = %d" % n_points
        
        pl, pu = self.foil.get_shape_points(n=n_points)
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
        if (False):
            xcoords = np.append(xcoords, xcoords[0] )
            ycoords = np.append(ycoords, ycoords[0] )
        #if (False):
            #xcoords = np.append(xcoords, xcoords[0] )
            #ycoords = np.append(ycoords, ycoords[-1] )
        
        coordslist = np.array((xcoords, ycoords)).T
        coordstrlist = ["{:.6f} {:.6f}".format(coord[0], coord[1])
                        for coord in coordslist]
        # Join with linebreaks in between
        points = '\n'.join(coordstrlist)

        # Save points to a file
        randstr = ''.join(choice(ascii_uppercase) for i in range(20))
        filename = "parsec_{}.dat".format(randstr)
        with open(filename, 'w') as af:
            af.write(points)
            
        # Let Xfoil do its magic
        alfa = np.arange(-30, 30, 1.0)
        polar = xfoil.get_polars(filename, alfa, reynolds, Mach=self.foil.Mach(velocity),
                                        iterlim=n_points*10, normalize=True, show_seconds=1)        
        #print polar.keys()
        os.remove(filename)
                
        cl = np.array(polar['CL'])
        cd = np.array(polar['CD'])
        cdp = np.array(polar['CDp'])
        cm = np.array(polar['CM'])
        top_xtr = np.array(polar['Top_Xtr'])
        bot_xtr = np.array(polar['Bot_Xtr'])
        alfa = np.radians(polar['alpha'])
        if len(alfa) < 5:
            logging.warning("Foil didn't simulate.")
            # Try modifying things.
            alpha = np.radians(np.linspace(-5, 40, 20))
            cl = 2.0 * np.pi * alpha
            cd = 1.28 * np.sin(alpha)
            cl_poly = np.poly1d(np.polyfit(alpha, cl, 4))
            cd_poly = np.poly1d(np.polyfit(alpha, cd, 4))
            return [cl_poly, cd_poly]

            cd = 1.28 * np.sin(alpha)
        else:
            # Insert into database
            conn = sqlite3.connect('foil_simulator.db')
            c = conn.cursor()
            c.execute("INSERT INTO simulation(foil_id, reynolds, mach) VALUES (?,?, ?)", (self.foil_id, reynolds, self.foil.Mach(velocity)))
            c.execute("SELECT id FROM simulation WHERE (foil_id=?) AND (reynolds=?)", (self.foil_id, reynolds, ))
            sim_id = c.fetchone()[0]

            for i, a in enumerate(alfa):
                c.execute("INSERT INTO polar(sim_id, alpha, cl, cd, cdp, cm, Top_Xtr, Bot_Xtr) VALUES (?,?,?,?,?,?,?,?)", 
                          (sim_id, a, cl[i], cd[i], cdp[i], cm[i], top_xtr[i], bot_xtr[i]))
            conn.commit()
            conn.close()
        
        return self.get_polars(velocity)

if __name__ == "__main__":
    from foil import NACA4
    f = NACA4(chord=0.1, thickness=0.15, m=0.06, p=0.4)
    f.set_trailing_edge(0.1)
    fs = XfoilSimulatedFoil(f)
    
    alpha = np.radians(np.linspace(-30, 40, 40))
    v = 3
    cl = []
    cd = []
    for a in alpha:
     cd.append(fs.get_cd(v, a))
     cl.append(fs.get_cl(v, a))
    cl = np.array(cl)
    cd = np.array(cd)
    z = fs.get_zero_cl_angle(v)
    print "Zero angle %f " % np.degrees(z)
    
    import matplotlib.pyplot as plt
    plt.plot(np.degrees(alpha), cl, label='Cl')
    plt.plot(np.degrees(alpha), cd, label='Cd')
    plt.plot(np.degrees(alpha), cl/cd, label='Cl/Cd')
    plt.plot([np.degrees(z)], [fs.get_cl(v, z)], 'x', label='Zero CL')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Angle of Attack')
    plt.show()
