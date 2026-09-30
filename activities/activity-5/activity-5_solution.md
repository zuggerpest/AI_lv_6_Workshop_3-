```python
def should_upsell(order: dict) -> bool:
    time = str(order.get("time_of_day", "")).strip().lower()
    loyalty = str(order.get("loyalty_member", "no")).strip().lower()
    temp = int(order.get("temperature", 0) or 0)
    size = int(order.get("order_size", 0) or 0)
    if temp > 30 and time == "lunch" and loyalty != "yes": return False
    if temp > 30: return True
    if size >= 4: return True
    if loyalty == "yes" and time == "lunch": return True
    return False
```