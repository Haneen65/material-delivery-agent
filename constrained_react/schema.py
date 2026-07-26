from tools import ALLOWED_ACTIONS

REQUIRED_KEYS = ["thought", "action", "status"]

VALID_STATUS = [
    "APPROVED",
    "PENDING",
    "REJECTED",
    "SCHEDULED",
    "ESCALATE"
]


def validate_schema(decision):
    if not isinstance(decision, dict):
        return False

    for key in REQUIRED_KEYS:
        if key not in decision:
            return False

    if decision["status"] not in VALID_STATUS:
        return False

    if decision["action"] not in ALLOWED_ACTIONS:
        return False

    return True
