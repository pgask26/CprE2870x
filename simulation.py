from node_config import num_zones
import time

# TODO: define some values?


# The Simulation(R)
_sim = None

# We only want ONE Simulation object, and we want to share it between all of the modules. We can accomplish this
# using the singleton design pattern. This function is a key part of that pattern. It returns the singleton instance.
# Call "simulation.get_instance()" to get a Simulation, instead of instantiating a Simulation directly.
def get_instance():
    global _sim
    if _sim is None:
        _sim = Simulation(num_zones)
    return _sim

# A class that simulates the physical environment for the system.
class Simulation:
    # Initializes the simulation.
    def __init__(self, num_zones):
       # TODO: initialize additional class variables. These are probably variables that represent the state of the physical system.
       self.heating = False
       self.cooling = False
       self.lastTimeRun = time.monotonic_ns()
       self.zoneTemps = []
       self.dampPerct = []


       for i in range(num_zones):
           self.zoneTemps.append(i)
           self.dampPerct.append(i)
           self.zoneTemps[i] = 0.0 #whatever inital temperture here
           self.dampPerct[i] = 100/100 #whatever inital temperture here
        

    # Returns the current temperature in the zone specified by zone_id
    def get_temperature_f(self, zone_id):
        
        return self.zoneTemps[zone_id]

    # Sets the damper(s) for the zone specified by zone_id to the percentage
    # specified by percent. 0 is closed, 100 is fully open.
    def set_damper(self, zone_id, percent):

        self.dampPerct[zone_id] = percent/100

    # Update the temperatures of the zones, given that elapsed_time_ms milliseconds
    # have elapsed since this was previously called.
    def _update_temps(self, elapsed_time_ms):

        elapsedTimeSeconds = elapsed_time_ms/1_000_000_000
            
        for i in range(num_zones):
            if self.heating:
                self.zoneTemps[i] += 1 * self.dampPerct[i] * elapsedTimeSeconds
            if self.cooling:
                self.zoneTemps[i] -= 1 * self.dampPerct[i] * elapsedTimeSeconds

    
    # Runs periodic simulation actions.
    def loop(self):
        # TODO: Calculate the amount of time elapsed since this last time this function was run. See CircuitPython's time module documentation
        # at http://docs.circuitpython.org/en/latest/shared-bindings/time/index.html. We recommend time.monotonic_ns(). Also note that
        # temperature_measurement_node.py has an elapsed time calculation, and you may be able to use a similar approach here.

        # TODO: pass in the actual elapsed time.
        self._update_temps(time.monotonic_ns() - self.lastTimeRun)

        self.lastTimeRun = time.monotonic_ns()


    #Set heating to on
    def setHeating(self, heating):

        if heating != self.heating:
            self.heating = heating
        


    #Set cooling to on
    def setCooling(self, cooling):
        
        if cooling != self.cooling:
            self.cooling = cooling


# Used for testing the simulation.
if __name__ == '__main__':
    sim = get_instance()
    i = 0

    while True:
        sim.loop()
        time.sleep(1)

        for zone in range(num_zones):
            temp = sim.get_temperature_f(zone)
            print(f'Zone {zone} temp: {temp}')
        print()
        
        #TODO: add additional testing code, e.g. what happens if you turn on heating/cooling?
        #if i == 0:
            #sim.setHeating(1) #turn on for second loop
            #sim.setCooling(1)

        # sim.set_damper(0,50)

        #print("Heating:", sim.heating, "Cooling:", sim.cooling)
        #sim.setCooling(False)
        #sim.setHeating(True)

        i = i+1