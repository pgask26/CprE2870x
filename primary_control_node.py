from node_config import *
import time
import board
import pwmio
import networking
import command
import node_config
import simulation
# if node_type == NODE_TYPE_SIMULATED:
#     import secondary_control_node
from adafruit_motor import servo

# --------------------------
# Configuration and Globals
# --------------------------

# Mode Type: Manual ("0") or Automatic ("1")
MODE_TYPE = "0"

# Temperatures
temp1 = "0"
temp2 = "0"
temp3 = "0"

# Desired Temperature Setpoints
destemp1 = "0"
destemp2 = "0"
destemp3 = "0"

# HVAC Status
coolingstatus = "0"
heatingstatus = "0"

# Desired Damper Angles
desDamper1 = "0"
desDamper2 = "0"
desDamper3 = "0"

# Internal tracking
_last_heartbeat_ns = 0

currentlyunderwork = "none"
currentlyunderwork2 = "none"

# --------------------------
# MQTT Message Handling
# --------------------------

def message_received(client, topic, message):
    global MODE_TYPE
    global destemp1, destemp2, destemp3
    global heatingstatus, coolingstatus
    global desDamper1, desDamper2, desDamper3
    global temp1, temp2, temp3

    print(f"New message on topic {topic}: {message}")

    if topic == networking.OPERATION_FEED[0]:
        MODE_TYPE = message
    elif topic == networking.COOLING_FEED[0]:
        coolingstatus = message
    elif topic == networking.HEATING_FEED[0]:
        heatingstatus = message
    elif topic == networking.SETPOINT_FEEDS[0]:
        destemp1 = message
    elif topic == networking.SETPOINT_FEEDS[1]:
        destemp2 = message
    elif topic == networking.SETPOINT_FEEDS[2]:
        destemp3 = message
    elif topic == networking.SET_DAMPER_FEEDS[0]:
        desDamper1 = message
    elif topic == networking.SET_DAMPER_FEEDS[1]:
        desDamper2 = message
    elif topic == networking.SET_DAMPER_FEEDS[2]:
        desDamper3 = message
    elif topic == networking.TEMP_FEEDS[0]:
        temp1 = message
    elif topic == networking.TEMP_FEEDS[1]:
        temp2 = message
    elif topic == networking.TEMP_FEEDS[2]:
        temp3 = message

# --------------------------
# Networking Setup
# --------------------------

networking.connect_to_network()
networking.socket_connect()
networking.mqtt_initialize()

networking.mqtt_connect(
    feeds=networking.COOLING_FEED +
          networking.HEATING_FEED +
          networking.OPERATION_FEED +
          networking.SET_DAMPER_FEEDS +
          networking.TEMP_FEEDS +
          networking.SETPOINT_FEEDS,
    message_callback=message_received
)

# --------------------------
# Damper Setup
# --------------------------

if node_type != NODE_TYPE_SIMULATED:
    pwm1 = pwmio.PWMOut(board.A0, duty_cycle=2**15, frequency=50)
    pwm2 = pwmio.PWMOut(board.A1, duty_cycle=2**15, frequency=50)
    pwm3AND4 = pwmio.PWMOut(board.A2, duty_cycle=2**15, frequency=50)

    damper1 = servo.Servo(pwm1)
    damper2 = servo.Servo(pwm2)
    damper3AND4 = servo.Servo(pwm3AND4)

    damper1.angle = 55.0
    damper2.angle = 55.0
    damper3AND4.angle = 55.0

    dampersList = [damper1, damper2, damper3AND4]

# --------------------------
# Main Loop
# --------------------------

def loop():
    global MODE_TYPE
    global destemp1, destemp2, destemp3
    global heatingstatus, coolingstatus
    global desDamper1, desDamper2, desDamper3
    global temp1, temp2, temp3
    global currentlyunderwork
    global currentlyunderwork2


    #print("=== Current System State ===")
    #print(f"MODE_TYPE: {MODE_TYPE}")
    #print(f"Desired Temps -> Zone 1: {destemp1}, Zone 2: {destemp2}, Zone 3: {destemp3}")
    #print(f"Actual Temperatures -> Zone 1: {temp1}, Zone 2: {temp2}, Zone 3: {temp3}")
    #print(f"Heating Status: {heatingstatus}")
    #print(f"Cooling Status: {coolingstatus}")
    #print(f"Damper Positions -> Zone 1: {desDamper1}, Zone 2: {desDamper2}, Zone 3: {desDamper3}")
    #print("============================")

    if node_type != NODE_TYPE_SIMULATED:
        if MODE_TYPE == "0":  # MANUAL
            print("RUNNING MANUAL")
            setXDamper(float(desDamper1), 0)
            setXDamper(float(desDamper2), 1)
            setXDamper(float(desDamper3), 2)
            #TBD

        elif MODE_TYPE == "1":  # AUTOMATIC
            print("RUNNING AUTOMATIC")
            
            if (currentlyunderwork == "none"):
                setAllDampers(100)
                setCoolMode(0)
                setHeatMode(0)
                

            if (currentlyunderwork == "none") or (currentlyunderwork == "one"):
                if abs(int(destemp1) - int(temp1)) >= 1:
                    currentlyunderwork = "one"
                    if int(destemp1) > int(temp1):
                        setHeatMode(1)
                        setCoolMode(0)
                    elif int(destemp1) < int(temp1):
                        setHeatMode(0)
                        setCoolMode(1)
                    
                    setXDamper(0, 0)
                else:
                    setXDamper(100, 0)
                    currentlyunderwork = "none"

            if (currentlyunderwork == "none") or (currentlyunderwork == "two"):
                if abs(int(destemp2) - int(temp2)) >= 1:
                    currentlyunderwork = "two"
                    if int(destemp2) > int(temp2):
                        setHeatMode(1)
                        setCoolMode(0)
                    elif int(destemp2) < int(temp2):
                        setHeatMode(0)
                        setCoolMode(1)

                    setXDamper(0, 1)
                else:
                    setXDamper(100, 1)
                    currentlyunderwork = "none"

            if (currentlyunderwork == "none") or (currentlyunderwork == "three"):
                if abs(int(destemp3) - int(temp3)) >= 1:
                    currentlyunderwork = "three"
                    if int(destemp3) > int(temp3):
                        setHeatMode(1)
                        setCoolMode(0)
                    elif int(destemp3) < int(temp3):
                        setHeatMode(0)
                        setCoolMode(1)

                    setXDamper(0, 2)
                else:
                    setXDamper(100, 2)
                    currentlyunderwork = "none"
            
    else:#SECOND HALF STARTS HERE
        if MODE_TYPE == "0":  # MANUAL
            print("RUNNING MANUAL")
            #TBD

        elif MODE_TYPE == "1":  # AUTOMATIC
            print("RUNNING AUTOMATIC IN PRIMARY")
            
            if (currentlyunderwork2 == "none"):
                #setAllDampers(100)
                (simulation.get_instance()).set_damper(0,100)
                (simulation.get_instance()).set_damper(1,100)
                (simulation.get_instance()).set_damper(2,100)
            
                
                (simulation.get_instance()).setCooling(False)
                (simulation.get_instance()).setHeating(False)

                

            if (currentlyunderwork2 == "none") or (currentlyunderwork2 == "one"):
                if abs(int(destemp1) - int((simulation.get_instance()).zoneTemps[0])) >= 1:
                    currentlyunderwork2 = "one"
                    if int(destemp1) > int((simulation.get_instance()).zoneTemps[0]):
                        (simulation.get_instance()).setCooling(False)
                        (simulation.get_instance()).setHeating(True)
                    elif int(destemp1) < int((simulation.get_instance()).zoneTemps[0]):
                        (simulation.get_instance()).setCooling(True)
                        (simulation.get_instance()).setHeating(False)
                    
                    #setXDamper(0, 0)
                    (simulation.get_instance()).set_damper(0,100)
                else:
                    #setXDamper(100, 0)
                    (simulation.get_instance()).set_damper(0,0)
                    currentlyunderwork2 = "none"

            if (currentlyunderwork2 == "none") or (currentlyunderwork2 == "two"):
                if abs(int(destemp2) - int((simulation.get_instance()).zoneTemps[1])) >= 1:
                    currentlyunderwork2 = "two"
                    if int(destemp2) > int((simulation.get_instance()).zoneTemps[1]):
                        (simulation.get_instance()).setCooling(False)
                        (simulation.get_instance()).setHeating(True)
                    elif int(destemp2) < int((simulation.get_instance()).zoneTemps[1]):
                        (simulation.get_instance()).setCooling(True)
                        (simulation.get_instance()).setHeating(False)

                    #setXDamper(0, 1)
                    (simulation.get_instance()).set_damper(1,100)
                else:
                    #setXDamper(100, 1)
                    (simulation.get_instance()).set_damper(1,0)
                    currentlyunderwork2 = "none"

            if (currentlyunderwork2 == "none") or (currentlyunderwork2 == "three"):
                if abs(int(destemp3) - int((simulation.get_instance()).zoneTemps[2])) >= 1:
                    currentlyunderwork2 = "three"
                    if int(destemp3) > int((simulation.get_instance()).zoneTemps[2]):
                        (simulation.get_instance()).setCooling(False)
                        (simulation.get_instance()).setHeating(True)
                    elif int(destemp3) < int((simulation.get_instance()).zoneTemps[2]):
                        (simulation.get_instance()).setCooling(True)
                        (simulation.get_instance()).setHeating(False)

                    #setXDamper(0, 2)
                    (simulation.get_instance()).set_damper(2,100)
                else:
                    #setXDamper(100, 2)
                    (simulation.get_instance()).set_damper(2,0)
                    currentlyunderwork2 = "none"
            
            #TBD

    publishDampers()

# --------------------------
# Utility Functions
# --------------------------

def setAllDampers(openingPercent):
    
    for i, damper in enumerate(dampersList):
        setXDamper(openingPercent, i)

def publishDampers():
    if node_type != NODE_TYPE_SIMULATED:
        for i, damper in enumerate(dampersList):
            
            angle_percent = round(((damper.angle - 55.0) / (125.0 - 55.0)) * 100.0)
            networking.mqtt_publish_message(networking.DAMPER_FEEDS[i], angle_percent)
    else:
        
        angle_percent = (simulation.get_instance()).dampPerct[0]
        networking.mqtt_publish_message(networking.DAMPER_FEEDS[0], angle_percent)
        
        angle_percent = (simulation.get_instance()).dampPerct[1]
        networking.mqtt_publish_message(networking.DAMPER_FEEDS[1], angle_percent)

        angle_percent = (simulation.get_instance()).dampPerct[2]
        networking.mqtt_publish_message(networking.DAMPER_FEEDS[2], angle_percent)

def setHeatMode(mode): #1 or 0
    
    
    networking.mqtt_publish_message(networking.HEATING[0], mode)

def setCoolMode(mode): #1 or 0
    
    
    networking.mqtt_publish_message(networking.COOLING[0], mode)

def setXDamper(openingPercent, damper_index):

    if node_type != NODE_TYPE_SIMULATED:
        MIN_ANGLE = 55.0  # Fully open
        MAX_ANGLE = 125.0  # Fully closed

        angle = MIN_ANGLE + ((MAX_ANGLE - MIN_ANGLE) * (openingPercent / 100.0))
        dampersList[damper_index].angle = angle
        #print("Angle: " + str(dampersList[damper_index].angle))