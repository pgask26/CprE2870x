from node_config import * 
#DAMPERS

# Don't import hardware libraries if simulating
# Preston: How am I supposed to do lab 8 without importing the hardware modules and simulating? maybe revert this later
#if node_type != NODE_TYPE_SIMULATED:
import digitalio
import simulation
import time
import board
import pwmio
from adafruit_motor import servo

# ------------ Damper control ----------- #
# Parallax Standard Servo (https://www.parallax.com/product/parallax-standard-servo/)
SERVO_ACTUATION_RANGE = 180  # degrees
SERVO_MIN_PULSE = 750  # us, for PWM control
SERVO_MAX_PULSE = 2250  # us, for PWM control
MIN_ANGLE = 45  # degrees
MAX_ANGLE = 135  # degrees

damper_servos = {}

#if node_type == NODE_TYPE_SIMULATED:
#    pwm1 = pwmio.PWMOut(board.A0, duty_cycle=2 ** 15, frequency=50)
#    pwm2 = pwmio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)
#    pwm3 = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)
#
 #   my_servo1 = servo.Servo(pwm1)
#    my_servo2 = servo.Servo(pwm2)
 #   my_servo3 = servo.Servo(pwm3)
#    
 #   damper_servos = [my_servo1, my_servo2, my_servo3]

#Set the damper for the given zone to the given percent (0 means closed, 100 means fully open)
#FUTURE PRESTON NOTE HERE IT IS FLIPPED DONT FORGET TO CHANGE IT FOR THE FINAL DEMO
def set_damper(zone, percent):
    if zone < 0 or zone >= len(damper_servos):
        print("Invalid zone")
    
    #Map percent to angle between 45 and 135 degrees
    angle = MIN_ANGLE + (MAX_ANGLE - MIN_ANGLE) * (percent / 100)
    
    #Ensure angle is within valid range
    # do I need this? angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))
    
    damper_servos[zone].angle = angle

# ------------ End damper control ----------- #

# ------------ Heat/cool control ----------- #
heatingPin = digitalio.DigitalInOut(board.D13)
heatingPin.direction = digitalio.Direction.OUTPUT

coolingPin1 = digitalio.DigitalInOut(board.D9)
coolingPin1.direction = digitalio.Direction.OUTPUT
coolingPin2 = digitalio.DigitalInOut(board.D6)
coolingPin2.direction = digitalio.Direction.OUTPUT

fanPin = digitalio.DigitalInOut(board.D12)
fanPin.direction = digitalio.Direction.OUTPUT



def set_heating(value):
    if value:
        heatingPin.value = True
    else:
        heatingPin.value = False

    simulation.get_instance().heating = value

def set_cooling(value):
    if value:
        coolingPin1.value = True
        coolingPin2.value = True
    else:
        coolingPin1.value = False
        coolingPin2.value = False

    simulation.get_instance().cooling = value

def set_circulating(value):
    # Circulation fan control (to be implemented)
    if value:
        fanPin.value = True
    else:
        fanPin.value = False
# ------------ End heat/cool control ----------- #