# Define possible node types
NODE_TYPE_SIMULATED = 0
NODE_TYPE_PRIMARY = 1
NODE_TYPE_SECONDARY = 2
NODE_TYPE_TEMPERATURE = 3

# Node's type, used to determine what code is run.
node_type = 1

# Total number of zones in the system
num_zones = 3

# Zone that the node is located in, starting at 0. Only relevant for temp measurement nodes.
zone_id = 1

ENABLE_MQTT = True
ENABLE_SOCKETS = False