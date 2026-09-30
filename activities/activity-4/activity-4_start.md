## 📋 Expected Outputs
You'll now be learning how to handle more complexity and practice cleaning your code. This is called "refactoring". This is the process of restructuring existing code to improve its internal design, readability, and maintainability without changing its external behaviour.

By the end of this activity, you will have:
- added two new tests;
- updated your code to handle the new tests;
- *refactored* your code and verified that all tests still pass.

## 📝 Step 4 – Refactoring Cycle (🔴 Red → 🟢 Green → 🔄 Refactor)

**💻 Cell 6 – Extend tests**

```python
# Heatwave (temperature 30 or greater) → True
order_3 = {"time_of_day": "evening", "loyalty_member": "no", "temperature": 32}
assert should_upsell(order_3) is True, "FAIL: Hot weather should trigger upsell."
print("PASS: Test 3")

# Large order (order size 4 or greater) → True
order_4 = {"order_size": 4}
assert should_upsell(order_4) is True, "FAIL: Large orders should trigger upsell."
print("PASS: Test 4")
```

Now your logic must consider the `temperature` and `order_size` to make all tests green.

⚠️ **Warning:** When you modify the `should_upsell()` function, make sure you re-run that cell, too, to both save the changes to the function and make sure the old tests continue to pass! ***All* tests must continue to pass as you practice TDD.**

### 🔄 Now Refactor!
You may now have a long chain of `if-else` statements and boolean logic that is difficult to read and understand. This is *technical debt*: the implied cost of additional work caused by choosing a quick or suboptimal solution instead of a more thorough, maintainable approach.

The next step is to pay this technical debt down by refactoring your function into smaller, readable pieces. Once you've made any changes, you can re-run your tests to verify that you haven't broken anything. If everything passes, you're in the clear!

✅ **Checkpoint:** Run all previous tests — they should still pass!

### 💡 Hints
- Purpose and clarity:
    - Can I explain this function to someone in one sentence?
- Structure and flow:
    - Is there a simple "happy path" with early returns (guard clauses) to reduce nesting?
    - Are conditionals ordered from most decisive/common to least?
    - Could combining related checks (e.g. compound conditions) make the logic clearer?
- Readability of conditionals:
    - Are the boolean expressions easy to read (e.g. `>=`, `>`, `==`)?
    - Are boundary conditions (e.g. `>= 30` vs `> 30`) consistent and intentional?
- Data access and defaults:
    - Can repeated dictionary lookups be replaced with local variables or helper functions?
    - Are default values (`order.get("key", default))`) explicit and sensible?
    - Do missing keys produce safe outcomes rather than silent mistakes?
- Duplication and cohesion:
    - Is any logic duplicated that could be consolidated (e.g. multiple `True` returns for similar reasons)?
- Maintainability:
    - Would someone new to the code understand the rules quickly without comments?
    - Is the code resilient to future rule changes (e.g. adding another upsell condition)?