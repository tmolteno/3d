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
        
    ''' RPM at torque Q:'''
    def get_rpm(self, q_in):
        return np.pi*self.Kv**2*q_in/30
        
    def get_efficiency(self, V, I):
        return (I - self.I0)*(-I*self.Rm + V)/(I*V)

    def get_Imax(self, V):
        ''' Current at Max Efficiency (Amps) '''
        return np.sqrt(V*self.I0 / self.Rm)
    
    def get_Qmax(self, V):
        ''' Torque at Max Efficiency (Newton meters)'''
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
    from sympy import Symbol, pi, sqrt, pprint, solve, Eq, solveset, refine


    Kv = Symbol('Kv', real=True, positive=True)  # Kv measured in RPM per volt back_emf - Kv * V
    Rm = Symbol('Rm', real=True, positive=True)  # Winding Resistance
    V = Symbol('V', real=True, positive=True)
    I = Symbol('I', real=True, positive=True) # Peak Current
    I0 = Symbol('I0', real=True, positive=True) # No load current
    V0 = Symbol('V0', real=True, positive=True) # No load voltage

    rpm2omega = pi / 30   # multiply RPM by this value to get angular frequency omega
    
    Kv_SI = Kv * rpm2omega  # Kv in  rad/s per volt.
    
    # Torque Constant
    Kq = 1 / Kv_SI


    # RPM at current I

    RPM = Kv*(I - I0)
    Q = Kq*(I - I0)

    # RPM at voltage V and torque q_in
    q_in = Symbol('q_in', real=True, positive=True)
    rpm_in = Symbol('rpm_in', real=True, positive=True)
    eqns = (Eq(Q, q_in))
    soln = solve(eqns, I, exclude=[I0])
    pprint(eqns)
    print(("RPM at torque Q: {}".format(RPM.subs(I, soln[0]))))
    # Efficiency

    eta = (V - I*Rm)*(I - I0)/(V*I)
    print(("efficiency={}".format(eta)))

    # Current at Max Efficiency

    Imax = sqrt(V*I0/Rm)

    # Torque at max efficiency:

    Qmax = Kq*(Imax - I0)

    # RPM at max eff.

    RPMmax = Kv*( V - Imax*Rm)


    print("Current at Max Efficiency: {}".format(Imax))
    print("RPM at Max Efficiency    : {}".format(RPMmax))
    print("Torque at Max Efficiency : {}".format(Qmax))
    
    I_max = Symbol('I_max', real=True, positive=True)
    
    eqns = (Imax - I_max)
    pprint( eqns)
    IOsoln = refine(solve(eqns, I0))
    print("No-load-current : {}".format(IOsoln))
    IOsoln = refine(solveset(eqns, I0))
    print("No-load-current : {}".format(IOsoln))

if __name__ == "__main__":
    
    m = Motor(Kv = 1900.0, I0 = 0.5, Rm = 0.405)
    
    i = np.linspace(1,12,50)
    e = m.get_efficiency(11.0, i)
    q = m.get_torque(i)
    #q, rpm = m.get_Qmax(v)
    import matplotlib.pyplot as plt
    plt.plot(q, e, label='Efficiency')
    #plt.plot(q, m.get_rpm(q), label='RPM')
    #plt.plot(v, q, label='Q_max')
    #plt.plot(v, rpm/1000, label='RPM')
    #plt.plot(v, m.get_Pmax(v), label='P_max')
    plt.legend()
    plt.grid(True)
    plt.title('Turnigy Multistar 1704 1900kV')
    plt.ylabel('Efficiency')
    plt.xlabel('Torque (Nm)')
    plt.savefig('multistar_17041900kv.png')
    #plt.show()

    symbolic_stuff()
