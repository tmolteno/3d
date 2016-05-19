import json

class DesignParameters:
    '''Design Parameters for prop
    
    '''
    def __init__(self, filename=0):
        self.name = "hello world"
        self.radius = 0.0625    # m
        self.hub_radius = 5.0 / 1000
        self.trailing_edge = 0.5 / 1000
        
        self.forward_airspeed = 1.0  # m/s
        self.altitude = 0.0  # MAS
        
        self.motor_volts = 11.0 
        self.motor_Kv = 1200   # Watts
        self.motor_winding_resistance = 0.206
        self.motor_no_load_current = 0.5
        
        self.scimitar_percent = 0.0   # Percentage scimitar

        if filename != 0:
          f = open(filename, 'r')
          data = f.read()
          f.close()
          self.from_json(data)

    def area(self):
        return 3.1415*self.radius*self.radius
      
    def to_json(self):
        configdict = {}
        configdict['name'] = self.name
        
        configdict['radius'] = self.radius
        configdict['hub_radius'] = self.hub_radius
        configdict['hub_depth'] = self.hub_depth
        
        configdict['scimitar_percent'] = self.param.scimitar_percent
        configdict['trailing_edge'] = self.param.trailing_edge
        
        configdict['forward_airspeed'] = self.forward_airspeed
        configdict['altitude'] = self.altitude
        
        configdict['motor_Kv'] = self.motor_Kv
        configdict['motor_volts'] = self.motor_volts
        configdict['motor_winding_resistance'] = self.motor_winding_resistance
        configdict['motor_no_load_current'] = self.motor_no_load_current
        
        
        json_str = json.dumps(configdict, sort_keys=True, indent=4, separators=(',', ': '))
        return json_str
      
    def from_json(self, data):
        settings = json.loads(data)
        self.name = settings['name']

        self.radius = settings['radius']
        self.hub_radius = settings['hub_radius']
        self.hub_depth = settings['hub_depth']
        
        self.scimitar_percent = settings['scimitar_percent']
        self.trailing_edge = settings['trailing_edge']
        
        self.forward_airspeed = float(settings['forward_airspeed'])
        self.altitude = float(settings['altitude'])
        
        self.motor_Kv = float(settings['motor_Kv'])
        self.motor_volts = settings['motor_volts']
        self.motor_winding_resistance = settings['motor_winding_resistance']
        self.motor_no_load_current = settings['motor_no_load_current']
        
    def save(self, fname):
        f=open(fname,"w")
        f.write(self.to_json())
        f.close()
      
if __name__ == "__main__":
    d = DesignParameters()
    d.save('prop_design.json')