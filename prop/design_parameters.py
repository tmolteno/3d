import json

class DesignParameters:
    '''Design Parameters for prop
    
    '''
    def __init__(self, filename=0):
        self.radius = 0.0625    # m
        self.hub_radius = 5.0 / 1000
        
        self.forward_airspeed = 1.0  # m/s
        self.altitude = 0.0  # MAS
        
        self.motor_torque = 12.0   # N cm
        self.motor_power = 100   # Watts
        self.motor_rpm = 10000.0   #
        self.scimitar_percent = 0.0   # Percentage scimitar

        if filename != 0:
          f = open(filename, 'r')
          data = f.read()
          f.close()
          self.from_json(data)

    def area(self):
        return 3.1415*self.radius*self.radius
      
    def rps(self):
        return self.motor_rpm / 60.0
    
    def to_json(self):
        configdict = {}
        configdict['radius'] = self.radius
        configdict['hub_radius'] = self.hub_radius
        configdict['scimitar_percent'] = self.param.scimitar_percent
        
        configdict['forward_airspeed'] = self.forward_airspeed
        configdict['altitude'] = self.altitude
        
        configdict['motor_rpm'] = self.motor_rpm
        configdict['motor_power'] = self.motor_power
        configdict['motor_torque'] = self.motor_torque
        
        json_str = json.dumps(configdict, sort_keys=True, indent=4, separators=(',', ': '))
        return json_str
      
    def from_json(self, data):
        settings = json.loads(data)
        self.radius = settings['radius']
        self.hub_radius = settings['hub_radius']
        self.scimitar_percent = settings['scimitar_percent']
        
        self.forward_airspeed = float(settings['forward_airspeed'])
        self.altitude = float(settings['altitude'])
        
        self.motor_rpm = float(settings['motor_rpm'])
        self.motor_power = settings['motor_power']
        self.motor_torque = settings['motor_torque']
        
    def save(self, fname):
        f=open(fname,"w")
        f.write(self.to_json())
        f.close()
      
if __name__ == "__main__":
    d = DesignParameters()
    d.save('prop_design.json')