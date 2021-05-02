'''
    Simulation Code for Airfoils
    
    Author Tim Molteno tim@elec.ac.nz
    
    Copyright 2016-2017
    
    Two classes are in here. The PlateSimulatedFoil returns C_L and C_D assuming the
    foil is a plate. Its quick and pretty rough.
    
    The XfoilSimulatedFoil uses the xfoil program to generate polars. Its slower and more accurate.
    
    
    TODO: Use some CFD to do the job better?

'''

import xfoil
import numpy as np
from scipy.optimize import brentq

import logging
logger = logging.getLogger(__name__)


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
conn_global = None

class XfoilSimulatedFoil(PlateSimulatedFoil):
  
    def __init__(self, foil):
        SimulatedFoil.__init__(self, foil)
        self.hash = foil.hash()
        conn = self.get_db()
        c = conn.cursor()
        result = c.execute("SELECT f.id FROM foil f WHERE (f.hash=?)", (self.hash,)).fetchone()
        if result == None:
            c.execute("INSERT INTO foil(hash) VALUES (?)", (self.hash,))
            c.execute("SELECT id FROM foil WHERE (hash=?)", (self.hash,))
            self.foil_id = c.fetchone()[0]
            logger.info("Creating Foil In Database, %s, id=%d" % (foil, self.foil_id))
        else:
            self.foil_id = result[0]
        conn.commit()
        #conn.close()
        self.polar_poly_cache = {}

    def get_db(self):
        global conn_global
        if conn_global is None:
            conn_global = sqlite3.connect('foil_simulator.db')
            c = conn_global.cursor()
            result = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='foil'").fetchone()
            if result == None:
                # Create database tables
                logger.info("Creating Database for the first time")
                fd = open('foil_simulator.sql', 'r')
                sqlFile = fd.read()
                fd.close()

                # all SQL commands (split on ';')
                sqlCommands = sqlFile.split(';')

                # Execute every command from the input file
                for command in sqlCommands:
                    # This will skip and report errors
                    # For example, if the tables do not yet exist, this will skip over
                    # the DROP TABLE commands
                    try:
                        logger.info(command)
                        c.execute(command)
                    except sqlite3.OperationalError as msg:
                        print("Command skipped: ", msg)
            conn_global.commit()

        return conn_global
    
    def get_zero_cl_angle(self, v):
        cl, cd = self.get_polars(v)
        try:
            zero = brentq(cl, np.radians(-30.0), np.radians(15.0))
        except:
            zero = 0.0
        return zero
        

    def get_cl(self, v, alpha):
        Ma = self.foil.Mach(v)
        if (Ma > 0.97 or abs(alpha) > np.radians(30) or (self.foil.Reynolds(v) < 30000)):
            return 2.0 * np.pi * alpha
        cl, cd = self.get_polars(v)
        return cl(alpha)

    def get_cd(self, v, alpha):
        Ma = self.foil.Mach(v)
        if (Ma > 0.97 or abs(alpha) > np.radians(30) or (self.foil.Reynolds(v) < 30000)):
            return 1.28 * np.sin(alpha)

        cl, cd = self.get_polars(v)
        return cd(alpha)

    def get_mach(self, velocity):
        # Round the Mach number to the neares 0.05
        Ma = np.round(self.foil.Mach(velocity)*2, 1)/2
        return Ma
    
    def get_reynolds(self, velocity):
        Re = self.foil.Reynolds(velocity)
        re_space = np.round(np.geomspace(30000, 2e6, 20), -4)
        idx = np.argmin(abs(re_space - Re))
        reynolds = re_space[idx] # np.round(Re, -4)  # Round to nearest 1000

        if (reynolds < 30000.0):
            reynolds = 30000.0
            
        return reynolds

    def get_from_db(self, velocity, reynolds, Ma):
        sim_id = None
        conn = self.get_db()
        c = conn.cursor()
        c.execute("SELECT s.id FROM simulation s WHERE (s.foil_id=?) AND (s.reynolds = ?) AND (s.mach = ?)", (self.foil_id, reynolds, Ma))
        result = c.fetchone()
        if (result != None):
            # Read from database
            sim_id = result[0]
        conn.commit()
        return sim_id
            
    def get_polars(self, velocity):
        
        reynolds = self.get_reynolds(velocity)
        Ma = self.get_mach(velocity)
        
        re_str = str(reynolds)
        if re_str in self.polar_poly_cache:
            return self.polar_poly_cache[re_str]

        # Check if we're in the databse
        sim_id = self.get_from_db(velocity, reynolds, Ma)
        if (sim_id != None):
            conn = self.get_db()
            c = conn.cursor()
            logger.info("retrieving from database sim_id=%d, %f" % (sim_id, reynolds))
            alpha = []
            cl = []
            cd = []
            for pol in c.execute("SELECT p.alpha, p.cl, p.cd FROM polar p WHERE (p.sim_id=?)", (sim_id,)):
                alpha.append(pol[0])
                cl.append(pol[1])
                cd.append(pol[2])
            if (len(alpha) > 20):
                
                cl_poly = np.poly1d(np.polyfit(alpha, cl, 9))
                cd_poly = np.poly1d(np.polyfit(alpha, cd, 9))
                conn.commit()
                #conn.close()
                
                #if (False):
                    #import matplotlib.pyplot as plt
                    #plt.plot(np.degrees(alpha), cl_poly(np.array(alpha)), label='Cl fit')
                    #plt.plot(np.degrees(alpha), cl, 'x', label='Cl')
                    #plt.plot(np.degrees(alpha), cd, 'o', label='Cd')
                    #plt.plot(np.degrees(alpha), np.array(cl)/np.array(cd), label='Cl/Cd')
                    #plt.legend()
                    #plt.grid(True)
                    #plt.xlabel('Angle of Attack')
                    #plt.title('{}'.format(self.foil))
                    #plt.show()

                self.polar_poly_cache[re_str] =  [cl_poly, cd_poly]

                return [cl_poly, cd_poly]
            else:
                logger.info("Cleaning up simulation with only {} points.".format(len(alpha)))
                c.execute("DELETE FROM simulation WHERE (id=?)", (sim_id,))
                conn.commit()
            
        self.xfoil_simulate_polars(reynolds, Ma)
        if (False):
            logger.info("Simulating Foil {}, at Re={} Ma={:5.2f}".format(self.foil, reynolds, Ma))
        
            ''' Use XFOIL to simulate the performance of this get_shape
            '''
        
            #n_points = int(101.0*self.foil.chord / self.foil.trailing_edge) + 30
            #n_points = min(81.0, n_points)
            #n_points = max(61, n_points)
            n_points = 43
            logger.info("N Points = %d" % n_points)
            
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
            polar = xfoil.get_polars(filename, alfa, reynolds, Mach=Ma,
                                            iterlim=200, normalize=True)
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
                logger.warning("Foil didn't simulate.")
                # Try modifying things.
                alpha = np.radians(np.linspace(-40, 40, 20))
                cl = 2.0 * np.pi * alpha
                cd = 1.28 * np.sin(alpha)
                cl_poly = np.poly1d(np.polyfit(alpha, cl, 4))
                cd_poly = np.poly1d(np.polyfit(alpha, cd, 4))
                return [cl_poly, cd_poly]
            else:
                # Insert into database
                conn = self.get_db()
                c = conn.cursor()
                c.execute("INSERT INTO simulation(foil_id, reynolds, mach) VALUES (?,?, ?)", (self.foil_id, reynolds, Ma))
                c.execute("SELECT id FROM simulation WHERE (foil_id=?) AND (reynolds=?) AND (mach=?)", (self.foil_id, reynolds, Ma ))
                sim_id = c.fetchone()[0]

                for i, a in enumerate(alfa):
                    c.execute("INSERT INTO polar(sim_id, alpha, cl, cd, cdp, cm, Top_Xtr, Bot_Xtr) VALUES (?,?,?,?,?,?,?,?)", 
                            (sim_id, a, cl[i], cd[i], cdp[i], cm[i], top_xtr[i], bot_xtr[i]))
                conn.commit()
        
        return self.get_polars(velocity)

    def xfoil_simulate_polars(self, reynolds, Ma):
        logger.info("Simulating Foil {}, at Re={} Ma={:5.2f}".format(self.foil, reynolds, Ma))
    
        ''' Use XFOIL to simulate the performance of this get_shape
        '''
        
        #n_points = int(101.0*self.foil.chord / self.foil.trailing_edge) + 30
        #n_points = min(81.0, n_points)
        #n_points = max(61, n_points)
        n_points = 42
        logger.info("N Points = %d" % n_points)
        
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
        polar = xfoil.get_polars(filename, alfa, reynolds, Mach=Ma,
                                        iterlim=200, normalize=True)
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
            logger.warning("Foil didn't simulate.")
            # Try modifying things.
            alpha = np.arange(np.linspace(-30, 30, 1.1))
            cl = 2.0 * np.pi * alpha
            cd = 1.28 * np.sin(alpha)
            cl_poly = np.poly1d(np.polyfit(alpha, cl, 4))
            cd_poly = np.poly1d(np.polyfit(alpha, cd, 4))
            return [cl_poly, cd_poly]
        else:
            # Insert into database
            conn = self.get_db()
            c = conn.cursor()
            c.execute("INSERT INTO simulation(foil_id, reynolds, mach) VALUES (?,?, ?)", (self.foil_id, reynolds, Ma))
            c.execute("SELECT id FROM simulation WHERE (foil_id=?) AND (reynolds=?) AND (mach=?)", (self.foil_id, reynolds, Ma ))
            sim_id = c.fetchone()[0]

            for i, a in enumerate(alfa):
                c.execute("INSERT INTO polar(sim_id, alpha, cl, cd, cdp, cm, Top_Xtr, Bot_Xtr) VALUES (?,?,?,?,?,?,?,?)", 
                          (sim_id, a, cl[i], cd[i], cdp[i], cm[i], top_xtr[i], bot_xtr[i]))
            conn.commit()
        


if __name__ == "__main__":
    import sys
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    logger.addHandler(out_hdlr)
    logger.setLevel(logging.INFO)

    if False:
        from foil import NACA4
        f = NACA4(chord=0.1, thickness=0.15, m=0.06, p=0.4)
    else:
        from foil_ARA import ARAD_20_Foil
        f = ARAD_20_Foil(chord=0.1)

    f.set_trailing_edge(0.1)
    fs = XfoilSimulatedFoil(f)
    
    alpha = np.radians(np.linspace(-30, 30, 40))
    v = 3
    cl = []
    cd = []
    for a in alpha:
     cd.append(fs.get_cd(v, a))
     cl.append(fs.get_cl(v, a))
    cl = np.array(cl)
    cd = np.array(cd)
    z = fs.get_zero_cl_angle(v)
    print("Zero angle %f " % np.degrees(z))
    
    import matplotlib.pyplot as plt
    plt.plot(np.degrees(alpha), cl, label='Cl')
    plt.plot(np.degrees(alpha), cd, label='Cd')
    plt.plot(np.degrees(alpha), cl/cd, label='Cl/Cd')
    plt.plot([np.degrees(z)], [fs.get_cl(v, z)], 'x', label='Zero CL')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Angle of Attack')
    plt.title('{}'.format(f))
    plt.show()
