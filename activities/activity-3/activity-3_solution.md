```python
def should_upsell(order: dict) -> bool:
    """Predict if a customer will buy a drink."""
    if order.get("time_of_day") == "lunch":
        if order.get("loyalty_member") == "no":
            return False

        return True

    return False
```