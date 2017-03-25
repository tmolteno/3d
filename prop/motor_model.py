'''
    Motor Model to return optimum torque and RPM.
    
    Author Tim Molteno tim@elec.ac.nz
    
    Copyright 2016-2017

'''
import numpy as np

class Motor:
    def __init__(self, Kv, I0, Rm):
        self.Kv = Kv
        self.I0 = I0
        self.Rm = Rm
        self.Kq = 30.0 / (np.pi * self.Kv)

    def get_torque(self, I):
        Kq = 30.0 / (np.pi * self.Kv)
        return Kq*(I - self.I0)
        
    def get_efficiency(self, V, I):
        return (I - self.I0)*(-I*self.Rm + V)/(I*V)

    def get_Imax(self, V):
        ''' Current at Max Efficiency (Amps) '''
        return np.sqrt(V*self.I0 / self.Rm)
    
    def get_Qmax(self, V):
        ''' Torque at Max Efficiency (Newton meters)'''
        pi = 3.1415926
        Imax = self.get_Imax(V)
        Qmax = self.Kq*(Imax - self.I0)
        RPMmax = self.Kv*( V - Imax*self.Rm)
        return (Qmax, RPMmax)

    def get_Pmax(self, V):
        ''' Power at Max Efficiency (Watts)'''
        Qmax, RPMmax = self.get_Qmax(V)
        power = 2.0*np.pi*Qmax * (RPMmax / 60)
        return power

def symbolic_stuff():
    from sympy import Symbol, pi, sqrt, pprint


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


    print "Current at Max Efficiency: {}".format(Imax)
    print "RPM at Max Efficiency    : {}".format(RPMmax)
    print "Torque at Max Efficiency : {}".format(Qmax)
  

if __name__ == "__main__":
    
    m = Motor(Kv = 1900.0, I0 = 0.5, Rm = 0.405)
    
    i = np.linspace(1,12,50)
    e = m.get_efficiency(11.0, i)
    q = m.get_torque(i)
    #q, rpm = m.get_Qmax(v)
    import matplotlib.pyplot as plt
    plt.plot(q, e, label='Efficiency')
    #plt.plot(i, q, label='Torque')
    #plt.plot(v, q, label='Q_max')
    #plt.plot(v, rpm/1000, label='RPM')
    #plt.plot(v, m.get_Pmax(v), label='P_max')
    plt.legend()
    plt.grid(True)
    plt.title('Turnigy Multistar 1704 1900kV')
    plt.ylabel('Efficiency')
    plt.xlabel('Torque (Nm)')
    plt.savefig('multistar_17041900kv.png')
    plt.show()

    symbolic_stuff()
