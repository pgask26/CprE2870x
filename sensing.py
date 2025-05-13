from node_config import *
# Only import hardware modules if we're not simulating
if node_type != NODE_TYPE_SIMULATED:
    import board
import simulation

#---------LM35 code----------#
ADC_MAX_VOLTAGE = 2.5 # Voltage range for the ADC input
ADC_MAX_VALUE = 65535 # Max value coming off the ADC
LM35_MV_PER_C = 10.0  # millivolts per degrees Celsius

# LM35 temperature sensor initialization
# TODO: pin configuration
if node_type == NODE_TYPE_SIMULATED:
    _lm35_pin = None
elif board.board_id == 'unexpectedmaker_feathers2':
    # Initialize LM35 input on pin A3
    import analogio
    _lm35_pin = analogio.AnalogIn(board.A3)
else:
    _lm35_pin = None

# Get a temperature reading from the LM35
def lm35_temperature_c():
    # TODO: read from lm35 and return value in degrees C
    if _lm35_pin is None:
        return 0  #Return 0 if LM35 is not working right

    raw_adc = _lm35_pin.value  # Read ADC value
    voltage = (raw_adc / ADC_MAX_VALUE) * ADC_MAX_VOLTAGE  #Convert ADC reading to voltage
    temperature_c = (voltage * 1000) / LM35_MV_PER_C  #Convert millivolts to degrees Celsius
    return temperature_c
#---------End LM35 code----------#

#---------FunHouse code----------#
# FunHouse initialization
if node_type == NODE_TYPE_SIMULATED:
    _lm35_pin = None
elif board.board_id == 'adafruit_funhouse':
    import analogio
    _lm35_pin = analogio.AnalogIn(board.A0)
else:
    _lm35_pin = None

# Get a temperature reading from the FunHouse internal temperature sensor
def funhouse_temperature_c():
    return lm35_temperature_c()
#---------End FunHouse code----------#

# Convert Celsius to Fahrenheit
def c_to_f(value):
    # TODO: implement
    return (value * 9/5) + 32

# Get a temperature reading using whatever sensor is configured. zone is the zone ID of 
# the zone we're getting the reading for (used when simulating)
def get_current_temperature_f(zone): #was zone=0
    if node_type == NODE_TYPE_SIMULATED:
        return (simulation.get_instance()).get_temperature_f(zone)
    if board.board_id == 'unexpectedmaker_feathers2':
        return c_to_f(lm35_temperature_c())

    if board.board_id == 'adafruit_funhouse':
        return c_to_f(funhouse_temperature_c())