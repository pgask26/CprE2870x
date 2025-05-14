from node_config import *
import networking
import time
import sensing  # Ensure this module has get_current_temperature_f()
#import adafruit_dotstar
import board, analogio, digitalio

# Initialize power for LDO2 if needed
#ldo2 = digitalio.DigitalInOut(board.LDO2)
# ldo2.direction = digitalio.Direction.OUTPUT

# def enable_LDO2(state):
#     """Set power for the second onboard LDO to allow no current draw when not needed."""
#     ldo2.value = state
#     time.sleep(0.035)  # Small delay to let the IO change state

# # Enable LDO2 (if required for DotStar operation)
# enable_LDO2(True)

# Set up networking.
networking.connect_to_network()
networking.mqtt_initialize()
networking.mqtt_connect()

# The previously reported temperature values.
prev_temps = [None] * num_zones
last_values = [1, 2, 3]

# Initialize DotStar LED (Fixed)
#led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Timing variables.
LOOP_INTERVAL_NS = 1000000000
_prev_time = time.monotonic_ns()

# Runs periodic node tasks.
def loop():
    global _prev_time
    global last_values
    curr_time = time.monotonic_ns()
    if curr_time - _prev_time < LOOP_INTERVAL_NS:
        return

    _prev_time = curr_time

    # Determine the zones to report temperature for
    zones = [zone_id]
    if node_type == NODE_TYPE_SIMULATED:
        zones = [i for i in range(num_zones)]

    i = 0
    for zone in zones:
        # Get current temperature from sensing module
        current_temp = sensing.get_current_temperature_f(zone)
        current_temp = round(current_temp)

        print(f'Zone {zone} temp: {current_temp}')

        # Change LED color based on temperature range
        # if current_temp < 65:  # Cold (Blue)
        #     led[0] = (0, 0, 255)  
        # elif 65 <= current_temp < 75:  # Comfortable (Green)
        #     led[0] = (0, 255, 0)
        # elif current_temp >= 75:  # Hot (Red)
        #     led[0] = (255, 0, 0)

        # Optional: Add logic to only report significant temperature changes

        if abs(last_values[i] - current_temp) >= 2:
            networking.mqtt_publish_message(networking.TEMP_FEEDS[zone], current_temp)
            last_values[i] = current_temp
            i = i + 1
