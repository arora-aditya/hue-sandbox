from phue import Bridge

bridge = Bridge('192.168.0.10')
bridge.connect()

lightstrip = bridge.get_light_objects('name')['Lightstrip']
lightstrip.on = True
lightstrip.transitiontime = 20
lightstrip.hue = 5000

print(bridge.get_schedule(1))
