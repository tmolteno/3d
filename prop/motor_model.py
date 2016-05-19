import numpy as np


import math

class Motor:
  
  def __init__(self, Kv, I0, Rm):
    self.Kv = Kv
    self.I0 = I0
    self.Rm = Rm
    self.Kq = 30.0 / (math.pi * self.Kv)
    
    
  def get_Qmax(self, V):
    ''' Torque at Max Efficiency (Newton meters)'''
    pi = 3.1415926
    Imax = np.sqrt(V*self.I0 / self.Rm)
    Qmax = self.Kq*(Imax - self.I0)
    RPMmax = self.Kv*( V - Imax*self.Rm)
    return (Qmax, RPMmax)

  def get_Pmax(self, V):
    ''' Power at Max Efficiency (Watts)'''
    Qmax, RPMmax = self.get_Qmax(V)
    power = 2.0*np.pi*Qmax * (RPMmax / 60)
    return power

def symbolic_stuff():
  from sympy import Symbol, pi, sqrt


  Kv = Symbol('Kv')  
  Rm = Symbol('Rm')  # Winding Resistance
  V = Symbol('V')
  Ip = Symbol('Ip') # Peak Current
  I = Symbol('I') # Peak Current
  I0 = Symbol('I0') # No load current


  # Torque Constant
  Kq = 30 / (pi * Kv)


  # RPM at current I

  RPM = Kv*(I - I0)
  Q = Kq*(I - I0)

  # Efficiency

  eta = (V - I*Rm)*(I - I0)/(V*I)
  print eta

  # Current at Max Efficiency

  Imax = sqrt(V*I0/Rm)

  # Torque at max efficiency:

  Qmax = Kq*(Imax - I0)

  # RPM at max eff.

  RPMmax = Kv*( V - Imax*Rm)


  print "Torque at Max Efficiency %s" % Qmax
  

if __name__ == "__main__":
    
    m = Motor(Kv = 980.0, I0 = 0.5, Rm = 0.207)
    
    v = np.linspace(9,12,20)
    print m.get_Qmax(v)
    
    symbolic_stuff()
