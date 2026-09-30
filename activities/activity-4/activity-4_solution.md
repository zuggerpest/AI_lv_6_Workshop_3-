## Before refactor
```python
def should_upsell(order: dict) -> bool:
    """Predict if a customer will buy a drink."""
    if order.get("time_of_day") == "lunch":
        if order.get("loyalty_member") == "no":
            return False

        return True

    if order.get("temperature", 0) >= 30:
        return True

    if order.get("order_size", 0) >= 4:
        return True

    return False
```

## After refactor
```python
def should_upsell(order: dict) -> bool:
    """Simple rule-based upsell logic."""
    if order.get("temperature", 0) >= 30: return True
    if order.get("order_size", 0) >= 4: return True
    if order.get("loyalty_member") == "yes" and order.get("time_of_day") == "lunch": return True
    return False
```