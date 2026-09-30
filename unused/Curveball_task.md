# Curveball Extension – Policy Overrides, Messy Inputs, and Safe Logging
**Estimated Time:** 45–60 minutes (including debrief)  
**Prereqs:** Completed Steps 1–6 in the Master Notebook (README);  
`src/rules.py` and `src/logging_utils.py` present

---

## Why this curveball?

Real systems change mid-sprint. Product introduces a **promotional rule** that partially contradicts the earlier “busy heatwave” override. You must:

1. **Capture the new rule in tests first**  
2. **Evolve** production code with minimal, explicit changes  
3. Keep behaviour **policy-gated** (feature flag)  
4. **Defensively parse** messy inputs  
5. **Log safely** even when MLflow may be missing

---

## Scenario

A new **Q4 promotion**:

> During **lunch** and **heatwave** (> 30 °C), **loyalty members** *should be upsold* despite the “busy lunch heatwave” rule for non-loyalty customers.

This is an **override to an override**, but only when a policy flag `promo_lunch_heatwave=True` is enabled.

Constraints that remain:

- Non-loyalty @ lunch + heatwave → **False**  
- Non-loyalty @ evening + heatwave → **True**  
- Large order (≥ 4) → **True**  
- Loyalty @ lunch → **True**

New complications:

- `temperature` may arrive as `"32C"` or `" 31.5 °c "`  
- `time_of_day` may have mixed case or spaces (`" Lunch "`)  
- `loyalty_member` may already be boolean  
- MLflow may not be installed → must **no-op gracefully**

---

## Task 1 – Write failing tests first (TDD)

Add these tests to `tests/test_rules.py`:

    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
    from rules import should_upsell

    # Existing behaviour controls
    def test_control_evening_heatwave_non_loyalty_true():
        assert should_upsell({"time_of_day": "evening", "loyalty_member": "no", "temperature": 32}) is True

    def test_control_busy_lunch_heatwave_non_loyalty_false():
        assert should_upsell({"time_of_day": "lunch", "loyalty_member": "no", "temperature": 32}) is False

    # --- New curveball tests ---
    def test_curveball_loyalty_lunch_heatwave_true_when_promo_enabled():
        policy = {"promo_lunch_heatwave": True}
        order = {"time_of_day": "lunch", "loyalty_member": "yes", "temperature": 32}
        assert should_upsell(order, policy=policy) is True

    def test_curveball_loyalty_lunch_heatwave_back_compat_true_when_promo_disabled():
        order = {"time_of_day": "lunch", "loyalty_member": "yes", "temperature": 32}
        assert should_upsell(order, policy={"promo_lunch_heatwave": False}) is True

    def test_curveball_messy_inputs_parsed_correctly():
        policy = {"promo_lunch_heatwave": True}
        order = {"time_of_day": "  LUNCH  ", "loyalty_member": True, "temperature": " 31.5 °C "}
        assert should_upsell(order, policy=policy) is True

    def test_curveball_temperature_string_without_unit():
        policy = {"promo_lunch_heatwave": True}
        order = {"time_of_day": "Lunch", "loyalty_member": "YES", "temperature": "33"}
        assert should_upsell(order, policy=policy) is True

Run:

    PYTHONPATH=src pytest -q

You should now see **failing tests** — that’s your cue to extend the function.

---

## Task 2 – Evolve `should_upsell` to accept a `policy` flag

Open `src/rules.py` and replace the function with this version:

    from typing import Any, Dict, Optional

    def _to_bool_yes(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            return value.strip().lower() in {"y", "yes", "true", "t", "1"}
        return False

    def _parse_temperature(value: Any, default: int = 0) -> int:
        \"\"\"Parse '31.5 °C', '32C', ' 30 ', etc. → integer °C\"\"\"
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return int(value)
        try:
            s = str(value).strip().lower()
            for tok in ["°c", "c", "degc", "degrees", "degree", "°"]:
                s = s.replace(tok, "")
            s = s.replace(" ", "")
            return int(float(s))
        except Exception:
            return default

    def _to_int(value: Any, default: int = 0) -> int:
        try:
            if value is None:
                return default
            if isinstance(value, bool):
                return int(value)
            return int(float(value))
        except Exception:
            return default

    def should_upsell(order: Dict[str, Any], policy: Optional[Dict[str, Any]] = None) -> bool:
        \"\"\"
        Decide upsell with rule precedence and optional policy overrides.

        Precedence (highest → lowest):
          A) Busy-lunch heatwave (non-loyalty) → False
          B) Promo override if enabled (lunch heatwave & loyalty) → True
          C) General heatwave (>30) → True
          D) Large order (≥4) → True
          E) Loyalty at lunch → True
          F) Else → False
        \"\"\"
        if order is None:
            order = {}
        if policy is None:
            policy = {}

        time_of_day = str(order.get("time_of_day", "")).strip().lower()
        loyalty_member = _to_bool_yes(order.get("loyalty_member"))
        temperature = _parse_temperature(order.get("temperature"), 0)
        order_size = _to_int(order.get("order_size"), 0)
        promo = bool(policy.get("promo_lunch_heatwave", False))

        # A) Busy lunch heatwave override
        if temperature > 30 and time_of_day == "lunch" and not loyalty_member:
            return False

        # B) Promo override (flagged)
        if promo and temperature > 30 and time_of_day == "lunch" and loyalty_member:
            return True

        # C) General heatwave
        if temperature > 30:
            return True

        # D) Large order
        if order_size >= 4:
            return True

        # E) Loyalty at lunch
        if loyalty_member and time_of_day == "lunch":
            return True

        # F) Default
        return False

Re-run:

    PYTHONPATH=src pytest -q

All curveball tests should now pass ✅

---

## Task 3 – Optional safe tagging when MLflow missing

Extend `src/logging_utils.py`:

    from typing import Dict, Any, Optional

    def log_experiment(order: Dict[str, Any], prediction: bool,
                       experiment_name: str = "hotdog-upsell",
                       run_name: str = "workshop-run",
                       tags: Optional[Dict[str, str]] = None) -> None:
        tags = tags or {}
        try:
            import mlflow  # type: ignore
        except Exception:
            print("[INFO] MLflow not installed — skipping logging.")
            return

        mlflow.set_tracking_uri("file:./mlruns")
        mlflow.set_experiment(experiment_name)
        with mlflow.start_run(run_name=run_name):
            mlflow.log_params(order)
            mlflow.log_metric("prediction", int(bool(prediction)))
            for k, v in tags.items():
                mlflow.set_tag(k, v)
            print("[MLflow] Run logged successfully.")

Usage example:

    from rules import should_upsell
    from logging_utils import log_experiment

    order = {"time_of_day": "lunch", "loyalty_member": "yes", "temperature": "32C"}
    policy = {"promo_lunch_heatwave": True}
    pred = should_upsell(order, policy=policy)
    log_experiment(order, pred, run_name="PromoCheck", tags={"promo_lunch_heatwave": "true"})

---

## Acceptance Criteria

- Tests for promo on/off + messy inputs pass  
- `policy` parameter defaults to backward-compatible behaviour  
- Lunch heatwave for non-loyalty remains **False**; loyalty @ lunch + heatwave is **True only if promo enabled**  
- Parsing handles `"32C"`, `" 31.5 °C "`, booleans, and casing  
- Logging skips gracefully when MLflow unavailable

---

## Debrief with Coach

- What did adding the **policy flag** teach about maintainability?  
- How did **defensive parsing** affect test design?  
- Where would you store these toggles in production (config, feature-flag service)?  
- How did tests serve as **safety rails** when modifying behaviour?  
- Optional: parameterise thresholds for easier A/B testing

---

**Deliverable:** All tests green; updated `rules.py` and `logging_utils.py` committed with messages:  
`feat: add promo_lunch_heatwave policy flag` and `chore: add defensive parsing for messy inputs`
