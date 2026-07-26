def check_inventory(request):
    amount = request["inventory"]
    material = request["material"]

    return f"{material} available quantity is {amount}"


def dispatch_vehicle(material, quantity):
    return f"Vehicle dispatched for {quantity} {material}"


def order_from_supplier(material, quantity):
    return f"Supplier order created for {quantity} {material}"


def inform_manager(message):
    return f"Manager informed: {message}"