## 📋 Expected Outputs
A new business rule has arrived: 
> **"During a heatwave, we are so busy that we should *not* offer drinks to non-loyalty members to speed up the queue."**

You have a test for this rule, but it's failing. You should do as you have been doing: fix `should_upsell()`. In this case, use the *debugging process* to fix the test. This is the systematic identification, isolation, and correction of defects or errors in software to ensure it behaves as intended.

By the end of this activity you will have updated the logic in `should_upsell()` using `print()` statements and logical reasoning to find the conflict in the rules and implement a fix that makes *all* tests (old and new) pass.

## 📝 Step 5 – Debugging Challenge (🔴 Red → 🟢 Green)

**💻 Cell 7 – Failing test for a new rule**

Add the new test.

```python
# Busy lunch heatwave (non-loyalty) → should NOT upsell
order_5 = {"time_of_day": "lunch", "loyalty_member": "no", "temperature": 32}
assert should_upsell(order_5) is False, "FAIL: Busy lunch heatwave (non-loyalty) should NOT upsell."
print("PASS: Test 5")
```

Run it - it should *fail*.

Now, use the *debugging process* to figure out how to change the logic in `should_upsell()` so that all unit tests pass.

### 💡 Hints
- Using `print()` statements:
    - Print inputs and outputs: Show the values your function receives and returns to confirm assumptions.
    - Print intermediate variables: Check calculations or condition evaluations inside the function.
    - Print decision points: Add prints before if statements to see which branch is taken.
    - Print expected vs actual: Compare what the test expects with what your function produces.
- Applying Logical Reasoning
    - Start from the failing test: Read the test name and expected outcome—what rule is it checking?
    - Trace the flow: Mentally (or on paper) follow the code path for the given input.
    - Check assumptions: Are you sure about default values, data types, and condition thresholds?
    - Simplify the problem: Reduce complex cases to smaller ones and test them individually.
    - Ask "why" repeatedly: Why did this branch run? Why is this value wrong? Keep drilling down.