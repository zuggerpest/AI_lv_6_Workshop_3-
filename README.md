# Welcome to Workshop 3 - Upsell Like an Engineer!

Hands-on workshop moving from exploratory notebooks to disciplined, professional Python for machine learning. You can read more about this scenario in [`user_brief.md`](./user_brief.md).

---

## 🔑 KEY — Emoji Guide

Throughout this workshop, emojis help you quickly identify different types of content:

| Emoji | Meaning |
|-------|---------|
| 🎯 | **Learning Objective** - What you'll achieve |
| 📋 | **Expected Outputs** - End result to aim for |
| 📝 | **Task/Step** - Something to do |
| 💻 | **Code Cell** - Python code to add |
| ⌨️ | **Terminal** - Shell command to run |
| 🔴 | **RED** - Write failing test first (TDD) |
| 🟢 | **GREEN** - Make the test pass (TDD) |
| 🔄 | **Refactor** - Clean up the code (TDD) |
| 💡 | **Tip/Hint** - Helpful suggestion |
| ⚠️ | **Warning** - Don't miss this |
| ✅ | **Checkpoint** - Verify your progress |
| 🤔 | **Reflect** - Think deeply about this |
| 📖 | **Explanation** - Background theory |
| 🚀 | **Extension** - Optional challenge |
| 🎓 | **Complete** - Activity finished |

---

## 🎯 Learning Intent

By the end of this workshop you will:

- Write code that is **testable**, **maintainable**, and **reproducible**  
- Practise **TDD** (Red → Green → Refactor) on a simple upsell predictor  
- **Log experiments** locally with MLflow  
- **Refactor** safely using tests as a safety net  
- Connect these habits to **risk reduction** and **technical debt**

## 📖 Notebook Guide (single notebook flow)

We’ll work in **one Jupyter notebook** for the whole day.  
Follow the activities in order below and add one code cell at a time.

> 💡 **Tip:** Use Markdown headings inside your notebook to mirror these steps.

## 📝 Activities

You will work through activities in the [`activities` folder](/activities/) in order:
- [Activity 1: Environment Setup and Verification](/activities/activity-1/activity-1_start.md)
- [Activity 2: The First TDD Cycle (Red -> Green)](/activities/activity-2/activity-2_start.md)
- [Activity 3: The Second TDD Cycle & MLflow Logging](/activities/activity-3/activity-3_start.md)
- [Activity 4: The Refactoring Cycle](/activities/activity-4/activity-4_start.md)
- [Activity 5: The Debugging Challenge](/activities/activity-5/activity-5_start.md)
- [Activity 6: Git Simulation and Final Reflection](/activities/activity-6/activity-6_start.md)

## 💡 Help
### Solutions
This repo contains *one possible* solution for each activity. These are there to ensure that you're able to continue making progress throughout the workshop in the event that you become stuck or have technical difficulties at any stage. Please use them responsibly to supplement your learning, not to replace it. **These are not the only possible solution to each activity.** If you have logic that is passing the tests, it is a correct solution to the problem and you can proceed.

### Running tests locally

After completing the notebook, the final function lives in `src/rules.py`.  
You can test it outside Jupyter like a real module (from an activated venv).

Run from the terminal:

    pytest -v

This executes `tests/test_rules.py` and prints concise results (e.g. `6 passed in 0.04s`).

## 🚀 Going Further (optional)

Move on to Activity 7 to bridge these habits into a small ML pipeline. Read `activities/activity-7/activity-7__start.md` for the overview: it maps pipeline stages to their tests and gives two focused exercises to harden preprocessing and keep accuracy guardrails. Apply the same TDD + defensive + observability mindset you used here. You’ll fork and open a Codespace on the testing mini-project repo you used in Aptem Module 3.1 (https://github.com/corndel-ai/testing-mini-project); if you’ve done it before, you can repeat the core tasks or jump to the further exercises.
