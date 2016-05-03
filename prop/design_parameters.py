import json

class DesignParameters:
    '''Design Parameters for prop
    
    '''
    def __init__(self, filename=0):
        self.forward_airspeed = 1.0  # m/s
        self.altitude = 0.0  # MAS
        self.RPM = 3000.0   #
        self.power = 70      # Watts
        self.radius = 0.0    # m
        self.hub_radius = 5.0 / 1000
        if filename != 0:
          f = open(filename, 'r')
          data = f.read()
          f.close()
          self.from_json(data)

      
    def rps(self):
        return self.RPM / 60.0
    
    def to_json(self):
        configdict = {}
        configdict['forward_airspeed'] = self.forward_airspeed
        configdict['altitude'] = self.altitude
        configdict['RPM'] = self.RPM
        configdict['power'] = self.power
        configdict['radius'] = self.radius
        configdict['hub_radius'] = self.hub_radius
        json_str = json.dumps(configdict)
        return json_str
      
    def from_json(self, data):
        settings = json.loads(data)
        self.forward_airspeed = float(settings['forward_airspeed'])
        self.altitude = float(settings['altitude'])
        self.RPM = float(settings['RPM'])
        self.power = settings['power']
        self.radius = settings['radius']
        self.hub_radius = settings['hub_radius']
        
    def save(self, fname):
      f=open(fname,"w")
      f.write(self.to_json())
      f.close()
      
if __name__ == "__main__":
    d = DesignParameters()
    d.save('prop_design.json')