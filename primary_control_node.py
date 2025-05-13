import actuation
import time
import networking
import command
import node_config
import board
import pwmio
from adafruit_motor import servo

#Desired set point (unused)
desiredPoint = 50.0

#Track last heartbeat sent duration
_last_heartbeat_ns = 0

#MODE TYPE (MAUNAL (0) OR AUTOMATIC (1))
MODE_TYPE = "0"

def message_received(client, topic, message):
    global MODE_TYPE
    print(f"New message on topic {topic}: {message}")
    #You could implement command parsing here if needed
    if topic == networking.OPERATION_FEED[0]:
        MODE_TYPE = message

def operation_message_received(client, topic, message):
    global MODE_TYPE
    print(f"OPERATION TYPE {topic}: {message}")
    MODE_TYPE = message
    #You could implement command parsing here if needed

#Set up networking and connections
networking.connect_to_network()
networking.socket_connect()
networking.mqtt_initialize()
#networking.mqtt_connect(feeds=networking.SETPOINT_FEEDS, message_callback=message_received) #Set points is for the temp
#networking.mqtt_connect(feeds=networking.SET_DAMPER_FEEDS, message_callback=message_received) #Set for the damper

networking.mqtt_connect(feeds=networking.COOLING_FEED + networking.HEATING_FEED + networking.OPERATION_FEED + networking.SET_DAMPER_FEEDS + networking.SETPOINT_FEEDS = networking.TEMP_FEEDS, message_callback=message_received) 
#networking.mqtt_connect(feeds=networking.HEATING_FEED, message_callback=message_received) 
#networking.mqtt_connect(feeds=networking.OPERATION_FEED, message_callback=operation_message_received)

#LIST DAMPERS
pwm1 = pwmio.PWMOut(board.A0, duty_cycle=2 ** 15, frequency=50)
pwm2 = pwmio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)
pwm3AND4 = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

damper1 = servo.Servo(pwm1)
damper2 = servo.Servo(pwm2)
damper3AND4 = servo.Servo(pwm3AND4)

damper1.angle = 45.0
damper2.angle = 45.0
damper3AND4.angle = 45.0

#ACTUAL LIST TEMPS
temp1 = 1.0
temp2 = 2.0
temp3 = 3.0

#DESIRED LIST TEMPS
destemp1 = 4.0
destemp2 = 5.0
destemp3 = 6.0

#LISTS
dampersList = [damper1, damper2, damper3AND4]
tempsList = [temp1, temp2, temp3]

def loop():
    global MODE_TYPE
    #UPDATE INTERNAL TEMPS
    #setAllDampers(0.0)
    #publishDampers()
    #time.sleep(15)
    #setAllDampers(100.0)
    #publishDampers()
    #time.sleep(15)
    
    print(MODE_TYPE)
    #ACT ACCORDINGLY
    if (MODE_TYPE == "0"): #MANUAL

        print("RUNNING MANUAL")

    if (MODE_TYPE == "1"): #AUTOMATIC

        print("RUNNING AUTOMATIC")
        
        #for i, temp in enumerate(tempsList):
        #    set_point = desiredPoint
        #    if temp < set_point - 1:
        #        sendHeatORCool(command.HEAT_COOL_HEATING)
        #    elif temp > set_point + 1:
        #        sendHeatORCool(command.HEAT_COOL_COOLING)
        #    else:
        #        sendHeatORCool(command.HEAT_COOL_OFF)

    #PUBLISH INFORMATION
    #publishTemps()
    #publishDampers()
    
    

def setAllDampers(openingPercent):
    #See actuation for dampers
    counter = 0

    for damper in dampersList:
        
        setXDamper(openingPercent, counter) #Set a single damper to a specific % of opening
        counter = counter + 1
        

def publishDampers():

    iterator = 0
    for damper in dampersList:
        time.sleep(1)
        #print(f'Damper {iterator} temp: {damper}')
        networking.mqtt_publish_message(networking.DAMPER_FEEDS[iterator], round(((damper.angle - 55.0)/(125.0 - 55.0))*100.0))
        iterator = iterator + 1

def publishTemps():

    iterator = 0
    for temp in tempsList:
        print(f'Zone {iterator} temp: {temp}')
        networking.mqtt_publish_message(networking.TEMP_FEEDS[iterator], temp)
        iterator = iterator + 1

def sendHeatORCool(mode):
    #command.HEAT_COOL_HEATING, command.HEAT_COOL_COOLING, or command.HEAT_COOL_OFF

    cmd = command.Command(
        type=command.TYPE_HEAT_COOL,
        values=[mode]
    )

    networking.socket_send_message(str(cmd))
    print(f"Sent heat/cool command: {cmd}")


def setXDamper(openingPercent, damper): #dampers for 0-3
    #See actuation for dampers

    MIN_ANGLE = 55.0  # degrees FULLY OPEN
    MAX_ANGLE = 125.0  # degrees FULLY CLOSED

    angle = MIN_ANGLE + ((MAX_ANGLE - MIN_ANGLE) * (openingPercent / 100.0))
    dampersList[damper].angle = angle

    print("Angle: " + str(dampersList[damper].angle))
