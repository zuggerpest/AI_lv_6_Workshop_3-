"""
Hotdog upsell rules. This is an example of GOFAI... do you remember what that means?

This module implements a simple, testable function `should_upsell` used during the workshop.
"""
from typing import Any, Dict

def _to_bool_yes(value: Any) -> bool:
    """Interpret common yes/true indicators; everything else is False."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        # Treat non-zero numbers as True
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        return v in {"y", "yes", "true", "t", "1"}
    return False

def _to_int(value: Any, default: int = 0) -> int:
    """Convert a value to int safely, with a default for missing/invalid."""
    try:
        if value is None:
            return default
        if isinstance(value, bool):
            return int(value)
        return int(float(value))
    except Exception:
        return default

def should_upsell(order: Dict[str, Any]) -> bool:
    """
    Predict whether to upsell a drink given an order context.

    **Business rules** (final refactored version used in the workshop):
    1) Busy heatwave override: If temperature > 30 AND time_of_day == 'lunch' AND not a loyalty member -> do NOT upsell.
    2) Heatwave: If temperature > 30 -> upsell.
    3) Large order: If order_size >= 4 -> upsell.
    4) Loyalty lunch: If loyalty member AND time_of_day == 'lunch' -> upsell.
    5) Otherwise: do not upsell.

    The function is defensive: it tolerates missing keys and mixed types.
    """
    if order is None:
        order = {}
    time_of_day = str(order.get("time_of_day", "")).strip().lower()
    loyalty_member = _to_bool_yes(order.get("loyalty_member"))
    temperature = _to_int(order.get("temperature"), default=0)
    order_size = _to_int(order.get("order_size"), default=0)

    # 1) Busy heatwave override
    if temperature > 30 and time_of_day == "lunch" and not loyalty_member:
        return False

    # 2) Heatwave (general)
    if temperature > 30:
        return True

    # 3) Large order
    if order_size >= 4:
        return True

    # 4) Loyalty at lunch
    if loyalty_member and time_of_day == "lunch":
        return True

    # 5) Default: no upsell
    return False

if __name__ == "__main__":
    # Quick self-checks mirroring our notebook asserts
    # 1a) Loyalty member at lunch -> True
    assert should_upsell({"time_of_day": "lunch", "loyalty_member": "yes"}) is True
    # 1b) Non-loyalty member at lunch -> False
    assert should_upsell({"time_of_day": "lunch", "loyalty_member": "no"}) is False
    # 2) Loyalty member in evening -> False
    assert should_upsell({"time_of_day": "evening", "loyalty_member": "yes"}) is False
    # 3) Heatwave (evening, non-loyalty) -> True
    assert should_upsell({"time_of_day": "evening", "loyalty_member": "no", "temperature": 32}) is True
    # 4) Large order -> True
    assert should_upsell({"order_size": 4}) is True
    # 5) Busy heatwave at lunch, non-loyalty -> False
    assert should_upsell({"time_of_day": "lunch", "loyalty_member": "no", "temperature": 32}) is False
    print("All inline checks passed.")
