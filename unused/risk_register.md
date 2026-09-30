# Risk Register — Hotdog Upsell Predictor

| ID | Risk Description | Category | Likelihood | Impact | Mitigation / Control |
|----|------------------|-----------|-------------|---------|----------------------|
| R1 | Learners forget to restart kernel after installing packages. | Operational | Medium | Medium | Emphasise restart in setup step; coach monitors early stage. |
| R2 | MLflow not installed in learner environment. | Technical | High | Low | Add `try/except` guard; code prints friendly message instead of failing. |
| R3 | Learners hard-code `return True` to pass first test. | Pedagogical | High | Low | Add negative test to block trivial solution. |
| R4 | String-case errors in keys (`Lunch`, `YES`, etc.). | Data quality | Medium | Medium | Use `.strip().lower()` and parsing helpers (`_to_bool_yes`, `_parse_temperature`). |
| R5 | Temperature parsing fails on messy strings (“31.5 °C”). | Data quality | Medium | Low | Defensive parser with safe fallback. |
| R6 | MLflow folder (`mlruns`) accidentally committed to Git. | Compliance | Low | Medium | Add `.gitignore` entry for `/mlruns/`. |
| R7 | Learners misinterpret MLflow logs as real model training. | Educational | Medium | Low | Clarify MLflow used only as tracking demo; no personal data logged. |
| R8 | Dependency drift (MLflow version mismatch). | Technical | Medium | Medium | Pin version 2.15.1; reinstall in setup cell if needed. |
| R9 | Confusion about production vs. notebook code. | Pedagogical | Medium | Low | README explains difference between notebook & `src/` modules. |

**Review cycle:** at each workshop iteration.  
**Owner:** Workshop coach.  
