import command
import networking
import actuation
import time

# Track the last time a heartbeat was received
_last_heartbeat_received = time.monotonic_ns()
FAULT_DETECTED = False

# Handle incoming socket messages
def socket_message_received(msg):
    global _last_heartbeat_received, FAULT_DETECTED

    # Heartbeat message from primary
    if msg == networking.HEARTBEAT_MESSAGE:
        _last_heartbeat_received = time.monotonic_ns()
        if FAULT_DETECTED:
            print("Heartbeat restored.")
        FAULT_DETECTED = False
        return

    # Parse command message
    cmd = command.Command(msg=msg)
    print(f'Command received: {cmd}, values: {cmd.values}')

    if cmd.type == command.TYPE_HEAT_COOL:
        mode = int(cmd.values[0])
        actuation.set_heating(mode == command.HEAT_COOL_HEATING)
        actuation.set_cooling(mode == command.HEAT_COOL_COOLING)
        update_circulation_fan()
        publishHeatingCoolingStatus()

# Update fan based on heating/cooling state
def update_circulation_fan():
    heat = actuation.get_heating()
    cool = actuation.get_cooling()
    actuation.set_circulating(heat or cool)

# Publish current heat/cool status to MQTT
def publishHeatingCoolingStatus():
    status = "off"
    if actuation.get_heating():
        status = "heating"
    elif actuation.get_cooling():
        status = "cooling"
    
    networking.mqtt_publish_message(networking.COOLING_HEATING_FEED, status)

# Setup networking and listeners
networking.connect_to_network()
networking.socket_connect()
networking.mqtt_initialize()
networking.mqtt_connect()
networking.socket_listen(socket_message_received)

# Loop to monitor heartbeat and process networking
def loop():
    #global _last_heartbeat_received, FAULT_DETECTED

    #now = time.monotonic_ns()

    # Detect loss of heartbeat from primary
    #if now - _last_heartbeat_received > networking.HEARTBEAT_JITTER_NS:
    #    if not FAULT_DETECTED:
    #        print("FAULT: Primary node heartbeat lost!")
    #        FAULT_DETECTED = True

    networking.loop()
    time.sleep(0.1)