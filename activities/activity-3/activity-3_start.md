## 📋 Expected Outputs
Our current code is too simple. It would offer a drink to a loyalty member at midnight. We want to expand our functionality *by writing a test first* so that a loyalty member should *not* be offered a drink in the evening. (It's not as hot in the evening; the drink isn't as desirable!)

Because the logic is now a little more complex, we may want to log it. We can consider this to be an "experiment" from an ML perspective. You'll also add some logging code and explore the JupyterLab file browser to find the logs.

By the end of this activity, you will have:
- modified the Python code of the `should_upsell()` method so that *all* tests (old and new) pass;
- added logging code with MLflow;
- explored the `mlruns` directory to see your "experiment" results.

## 📝 Step 3 – TDD Cycle 2 (🔴 Red → 🟢 Green + Intro to MLflow)

**💻 Cell 4 – Add a new test**

```python
# Evening loyalty → should NOT be upsold
order_2 = {"time_of_day": "evening", "loyalty_member": "yes"}
assert should_upsell(order_2) is False, "FAIL: Evening loyalty should NOT be upsold."
print("PASS: Test 2")
```

Now your logic must consider both `time_of_day` and `loyalty_member` to make all tests green.

⚠️ **Warning:** When you modify the `should_upsell()` function, make sure you re-run that cell, too, to both save the changes to the function and make sure the old tests continue to pass! ***All* tests must continue to pass as you practice TDD.**

**💻 Cell 5 – Log experiment with MLflow**

Add this to a new Code cell and run:

```python
try:
    import mlflow
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("hotdog-upsell")
    with mlflow.start_run(run_name="Initial Loyalty Rule"):
        order = {"time_of_day": "lunch", "loyalty_member": "yes"}
        prediction = should_upsell(order)
        mlflow.log_params(order)
        mlflow.log_metric("prediction", int(bool(prediction)))
        mlflow.set_tag("rule_version", "v1")
    print("Experiment logged successfully ✅")
except Exception:
    print("[INFO] MLflow not installed — skipping logging safely.")
```

✅ **Checkpoint:** You should see `Experiment logged successfully ✅` printed.

- You can now  explore the `mlruns` directory in the VS Code file browser to find the files MLflow created.
- Or browse the same files in the ML Flow UI. If you've not done this already, as a reminder, you would run `mlflow ui --port 5000 --backend-store-uri file:./mlruns` then open http://localhost:5000