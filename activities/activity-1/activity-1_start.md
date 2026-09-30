## 📋 Expected Outputs
You'll create a Jupyter Notebook in your Codespace (or local environment, if you prefer) using a venv. You'll verify the environment so you're ready to progress with the rest of the workshop. By the end, you'll have:
- setup your environment for the rest of the workshop;
- one Markdown cell in a Jupyter notebook;
- two Code cells in a Jupyter notebook that you've successfully run.

## 📝 Step 0 – Setup your environment and create your notebook
### 1. Setup environment
#### Work on your own copy (Codespace recommended)
- **Preferred:** Fork this repository (or accept the GitHub Classroom link if provided), then create a Codespace from your fork. A Codespace gives you a ready-to-code cloud dev environment; learn more in the GitHub docs: https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces
- **Local option:** Clone the repo and work on your machine if you prefer.

![GitHub Codespaces diagram](https://docs.github.com/assets/cb-68851/mw-1440/images/help/codespaces/codespaces-diagram.webp)

- **How to create your CodeSpace in GitHub**

1. Go to **your** version of the repository in your GitHub account (either forked or created from a GitHub Classroom link).
2. Select **Code** (green button near the top right).  
3. Choose the **Codespaces** tab.  
4. Select **Create codespace on main**.
5. Wait while GitHub prepares the environment; it will open in a new browser window. 
6. Once it loads, you can start working in VS Code within your browser.

#### Python environment (venv)
We recommend running all workshop exercises in a Python virtual environment, just as you did in Aptem Module 3.1 (automated tests) and the testing-mini-project (https://github.com/corndel-ai/testing-mini-project).

⌨️ Create and activate a venv (macOS/Linux, including Codespaces):
  - `python -m venv .venv`
  - `source .venv/bin/activate`

⌨️ OR on Windows:
  - `python -m venv .venv`
  - `.\.venv\Scripts\activate`


⌨️ Then upgrade pip and install dependencies:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`

> “A virtual environment is a directory that contains a Python installation for a particular version of Python, plus a number of additional packages.” — [Real Python: Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)

#### Requirements
Dependencies live in `requirements.txt` and match what you installed in the venv:
- mlflow==2.15.1
- pandas>=2.0.0
- scikit-learn>=1.3.0
- numpy>=1.24.0
- jupyter>=1.0.0
- ipykernel>=6.0.0
- pytest>=7.0.0

#### MLflow (from an activated venv)
MLflow is commonly used to track model-training experiments, but here we use it early to show how it can log any action we choose in a clear, auditable way.

⌨️ You can run MLFlow by either:
- Run the UI in the foreground (defaults to local paths like `./mlruns`):
  - `mlflow ui --port 5000 --backend-store-uri file:./mlruns`
  - Open http://localhost:5000
  - You can stop it with `Ctrl+c`
- OR run in the background with logs:
  - `nohup mlflow ui --port 5000 --backend-store-uri file:./mlruns > mlflow.log 2>&1 &`
  - `echo $! > mlflow.pid`
  - Tail logs: `tail -f mlflow.log`

You can then additionally:
- Stop/inspect:
  - `kill $(cat mlflow.pid)` (or `pkill -f "mlflow ui"` if needed)
  - `lsof -i :5000` to confirm it stopped
- Run the sample script from the repo root:
  - `PYTHONPATH=src python scripts/run_mlflow_example.py`

### 2. Create notebook
1. Make sure you’ve created and activated the venv per the section above, and installed dependencies with `pip install -r requirements.txt`.
2. In your GitHub Codespace in VS Code, from the hamgeruger menu top left, click **File → New → Jupter Notebook**.  
3. Top right in your notebook click **Select Kernel** button then **Browse marketplace for kernel extensions**. Install the top extension in the list called **Jupyter**.
4. Click the button top right now be called **Python 3 (ipykernel)**, then click **Python Environments...**, then select the kernel that is our virtual python enviroment that is called **.venv...**.
5. Rename the notebook to **Workshop3W_Master.ipynb** by right-clicking it in the explorer on the left and selecting "Rename".
6. Modify the first cell in your notebook so that it's a Markdown cell. You can do this by clicking on the word "python" in the bottom right of the cell and selecting "markdown" from the drop-down list in the command menu that opens.

**Add this as your first Markdown cell:**

    # Workshop 3W — Upsell Like an Engineer
    Unit 3 — Programming for Intelligent Products

    Today we’ll practise TDD (Red → Green → Refactor), experiment logging, and debugging discipline.

---

## 📝 Step 1 – Verify your environment (then restart kernel)

You should already have the venv activated and dependencies installed (per the README). Ensure your notebook is using that venv's kernel, then verify:

**💻 Cell 1 – Verify**

Create a new Code cell:

```python
import sys, platform
print("Python:", sys.version)
print("Platform:", platform.platform())
import mlflow, pandas as pd
print("MLflow:", mlflow.__version__)
print("Environment ready ✅")
```

Run this and ignore any warnings about deprecated packages. (In production code, you should pay attention to these and take action, but it's not vital today.)

✅ **Checkpoint:** Ensure that the MLflow version is 2.15.1 and you see `Environment ready ✅`.

---

## 🗺️ Overview of activities 2 to 5
This diagram shows the full rule-based logic for deciding when to upsell a drink, and in Activities 2, 3, 4, and 5 you’ll build it up step by step: starting with a simple “loyalty at lunch” rule, extending it to other times of day, then adding heatwave and large-order rules, and finally introducing a special override for busy lunch heatwaves.


                           ┌──────────────────────────────┐
                           │ Start: Evaluate order input   │
                           └───────────────┬──────────────┘
                                           │
                                           ▼
        ┌───────────────────────────────────────────────────────────────┐
        │ Rule from Cycle 1: Is loyalty_member "yes" AND time_of_day    │
        │ == "lunch"?                                                    │
        └───────────────────────────────┬───────────────────────────────┘
                                        │ Yes
                                        ▼
                                 ┌────────────┐
                                 │  RETURN    │
                                 │   TRUE     │ (Loyal customer at lunch)
                                 └────────────┘
                                        │
                                        │ No
                                        ▼
        ┌───────────────────────────────────────────────────────────────┐
        │ Rule from Cycle 2: Is time_of_day NOT "lunch"?                │
        │ (e.g., evening loyalty → no upsell)                           │
        └───────────────────────────────┬───────────────────────────────┘
                                        │ Yes
                                        ▼
                                 ┌────────────┐
                                 │  RETURN    │
                                 │   FALSE    │ (Outside lunch → no upsell)
                                 └────────────┘
                                        │
                                        │ No (still lunch)
                                        ▼
                    ┌────────────────────────────────────────────┐
                    │ Refactor rules: Is temperature > 30?       │
                    └───────────────────────┬────────────────────┘
                                            │ Yes
                                            ▼
                                     ┌────────────┐
                                     │  RETURN    │
                                     │   TRUE     │ (Heatwave upsell)
                                     └────────────┘
                                            │
                                            │ No
                                            ▼
                  ┌───────────────────────────────────────────┐
                  │ Refactor rules: Is order_size ≥ 4?        │
                  └─────────────────────┬─────────────────────┘
                                        │ Yes
                                        ▼
                                 ┌────────────┐
                                 │  RETURN    │
                                 │   TRUE     │ (Large order upsell)
                                 └────────────┘
                                        │
                                        │ No
                                        ▼
                     ┌────────────────────────────────────────────┐
                     │ Debugging challenge override: Is           │
                     │ temperature > 30 AND time_of_day == lunch  │
                     │ AND NOT loyalty_member?                     │
                     └───────────────────────┬────────────────────┘
                                             │ Yes
                                             ▼
                                      ┌────────────┐
                                      │  RETURN    │
                                      │   FALSE    │ (Busy lunch heatwave override)
                                      └────────────┘
                                             │
                                             │ No
                                             ▼
                         ┌───────────────────────────┐
                         │        RETURN FALSE        │
                         │     (Default – no upsell) │
                         └───────────────────────────┘
