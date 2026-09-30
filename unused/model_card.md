# Model Card — Hotdog Upsell Predictor

## 1. Overview
The **Hotdog Upsell Predictor** is a simple rule-based ML logic used for teaching disciplined Python development in Workshop 3W.  
It demonstrates **Test-Driven Development (TDD)**, **refactoring**, and **safe experiment logging** using MLflow.

Although the current version is rule-based, the same engineering habits apply to statistical or ML models.

---

## 2. Intended Use
**Purpose:**  
To simulate the decision logic used by a point-of-sale (POS) system to decide whether to offer customers a drink.

**Intended users:**  
Junior AI/ML engineers learning software-engineering best practices.

**Context of use:**  
Educational environments (e.g. Corndel Level 6 Applied AI Engineering).

---

## 3. Model / Logic Description
### Input Fields
| Field | Type | Example | Notes |
|--------|------|----------|-------|
| `time_of_day` | string | `"lunch"` | Normalised to lowercase |
| `loyalty_member` | string/bool | `"yes"` or `True` | Parsed safely via `_to_bool_yes()` |
| `temperature` | int/str | `32` or `"32C"` | Parsed safely via `_parse_temperature()` |
| `order_size` | int | `2` | Defaults to 0 if missing |

### Core Rules (final implementation)
1. **Busy lunch heatwave override** – if temp > 30 and time == "lunch" and not loyalty → `False`
2. **Promo override** – if `promo_lunch_heatwave=True` and (loyalty and lunch and temp > 30) → `True`
3. **Heatwave rule** – if temp > 30 → `True`
4. **Large order rule** – if order_size ≥ 4 → `True`
5. **Loyalty at lunch rule** – if loyalty and lunch → `True`
6. **Default** → `False`

---

## 4. Performance / Verification
There is no predictive accuracy metric (rule-based).  
Verification is via **pytest** unit tests confirming all expected cases pass.  

## 5. Limitations and Ethical Considerations
- Educational only — not trained on real customer data.  
- Does not account for real-world pricing, demographics, or fairness metrics.  
- Rules are deterministic; no learning or bias mitigation applied.

---

## 6. Responsible AI Considerations
| Dimension | Example Control |
|------------|----------------|
| **Transparency** | Model card shared openly with learners. |
| **Accountability** | Behaviour defined through explicit tests. |
| **Reproducibility** | MLflow logging + pinned dependencies ensure reproducibility. |
| **Sustainability** | Lightweight logic; minimal compute impact. |

---

## 7. Versioning and Maintenance
| Version | Date | Notes |
|----------|------|-------|
| v1.0 | 2025-10-03 | Initial implementation during Workshop 3W |
| v1.1 | 2025-11-03 | Curveball extension — promo policy + messy-input parsing |

Maintainer: **Dr Michael Robert Hoffman**  
Location: `src/rules.py`
