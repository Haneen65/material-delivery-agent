ALLOWED_ACTIONS = [
    "Deliver Immediately",
    "Wait for Restock",
    "Schedule Vehicle",
    "Review System Logs"
]

VALID_TOOLS = [
    "check_inventory",
    "check_vehicle",
    "dispatch_material",
    "schedule_delivery"
]


def check_inventory(quantity, inventory):
    return inventory >= quantity


def check_vehicle(vehicle):
    return vehicle


def dispatch_material():
    return "Deliver Immediately"


def schedule_delivery():
    return "Schedule Vehicle"