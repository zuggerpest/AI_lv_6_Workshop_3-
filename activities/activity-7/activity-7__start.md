# 🚀 Bridging Workshop 3 and the Mini Testing Project in Aptem

This bridge keeps one idea front and centre, TDD, defensive, and observability habits you practiced on a pure function now apply to an pipeline. Below: (1) the pipeline stages mapped to the exact tests that cover them, and (2) two focused exercises to extend the project.

In the Aptem module *3.1 Python Essentials for AI enginers* e-learning, if you compelted this you saw how `.py` modules and automated tests underpin long-term maintainability. Here, we can reinforce that with automated tests and version control act as living documentation of what last worked, and TDD is how you keep that truth current.

> 💡 **Note:** This exercise builds directly on the Aptem e-learning "31. Python Essentials for AI Engineers". You were given a worked solution in that module; use it as your baseline here.

---

## Prerequisites

Before starting these exercises, ensure you have:

- ✅ **Completed Workshop 3W exercises** (TDD basics, pure functions, red-green-refactor cycle)
- ✅ **Forked and opened a Codespace on the testing mini-project repo** you used in Aptem Module 3.1: https://github.com/corndel-ai/testing-mini-project (if you’ve done it before, you can repeat or jump to the further exercises)
- ✅ **Virtual environment activated** and dependencies installed in that repo (use your venv name; `.venv` shown here):
  ```bash
  python -m venv .venv
  # Activate
  source .venv/bin/activate  # macOS/Linux
  # Windows: .\.venv\Scripts\activate
  pip install -r requirements.txt
  ```
- ✅ **All tests currently passing**:
  ```bash
  pytest tests/ -v
  # Expected output: All tests pass (should see 4 passed)
  ```
- ✅ **Familiarity with project structure** (review `README.md` if needed)

---

## 📖 Pipeline → Tests Map: Understanding the Architecture

This section maps the **data flow** through the pipeline to the **tests that verify each stage**. Understanding this helps you extend the project systematically.

### 🔄 Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Text Classification Pipeline                    │
└─────────────────────────────────────────────────────────────────────────┘

   Raw Text Input
        │
        ├─────────────────────────────────────────────────────────────────┐
        │ STAGE 1: Preprocess (preprocess_text)                           │
        │ • Lowercase text                                                │
        │ • Remove non-alphabetic chars (keep spaces)                     │
        │ • Collapse multiple spaces                                      │
        │                                                                  │
        │ 🧪 TESTED BY: tests/test_TextClassifier_unit.py                 │
        │    - 2 unit tests (basic, empty)                                │
        └──────────────────────────────────────────────────────────────────┘
        │
   Clean Text
        │
        ├─────────────────────────────────────────────────────────────────┐
        │ STAGE 2: Vectorize (CountVectorizer.fit_transform)              │
        │ • Convert text to numerical features (word counts)              │
        │ • Build vocabulary from training data                           │
        │                                                                  │
        │ 🧪 TESTED BY: tests/conftest.py (fixture setup)                 │
        │    - Session-scoped trained_classifier fixture                  │
        └──────────────────────────────────────────────────────────────────┘
        │
   Feature Matrix (X)
        │
        ├─────────────────────────────────────────────────────────────────┐
        │ STAGE 3: Train (LogisticRegression.fit)                         │
        │ • Learn patterns from features + labels                         │
        │                                                                  │
        │ 🧪 TESTED BY: tests/conftest.py (fixture setup)                 │
        │    - Trains once per test session                               │
        └──────────────────────────────────────────────────────────────────┘
        │
   Trained Model
        │
        ├─────────────────────────────────────────────────────────────────┐
        │ STAGE 4: Predict (predict)                                      │
        │ • Preprocess new text                                           │
        │ • Transform using EXISTING vocabulary (no fitting!)             │
        │ • Generate predictions                                          │
        │                                                                  │
        │ 🧪 TESTED BY:                                                    │
        │    - tests/test_TextClassifier_integration.py                   │
        │    - tests/test_TextClassifier_regression.py                    │
        └──────────────────────────────────────────────────────────────────┘
        │
   Predictions
        │
        ├─────────────────────────────────────────────────────────────────┐
        │ STAGE 5: Evaluate (evaluate)                                    │
        │ • Compare predictions to true labels                            │
        │ • Calculate accuracy score                                      │
        │                                                                  │
        │ 🧪 TESTED BY: tests/test_TextClassifier_regression.py           │
        └──────────────────────────────────────────────────────────────────┘
        │
   Accuracy Metrics
```

### 🎯 What You'll Build

- **Exercise 1**: Replace the unit test file with a complete version that tests basic preprocessing (2 tests → 2 tests)
- **Exercise 1b**: Practice TDD by adding 3 new failing tests (HTML, URLs, accents), then implement the features to make them pass (2 tests → 5 tests)
- **Exercise 2**: Add MLflow experiment tracking to `train()` to log hyperparameters and metrics

---

## 📝 Exercise 1: Complete the TODO Tests (TDD Foundation)

🎯 **Goal**: Reuse the Aptem e-learning test suite (from "31. Python Essentials for AI Engineers") by dropping it into [tests/test_TextClassifier_unit.py](../tests/test_TextClassifier_unit.py). This is the same suite you were given; use it as your baseline.

⏱️ **Time**: 20-30 minutes

**Why this matters**: The current `preprocess_text` implementation ([src/TextClassifier.py](../src/TextClassifier.py#L25-L37)) is intentionally basic. Production text preprocessing must handle edge cases: punctuation, multiple spaces, numbers, symbols. These TODOs guide you to harden it systematically using the TDD approach from Workshop 3W.

---

### 📝 Step 1: Replace the test file with complete tests

💻 Replace the entire contents of `tests/test_TextClassifier_unit.py` with the following code:

```python
from src.TextClassifier import TextClassifier


def test_preprocess_text_basic():
    """Unit test for basic text preprocessing."""
    classifier = TextClassifier()
    assert classifier.preprocess_text("HELLO WORLD") == "hello world"
    # Test case for mixed case text
    assert classifier.preprocess_text("PYthon is FUN") == "python is fun"
    # Test case for punctuation removal
    assert classifier.preprocess_text("Hello, World!") == "hello world"
    # Test case for numbers and symbols
    assert (
        classifier.preprocess_text("Numbers 123 and symbols!@#")
        == "numbers and symbols"
    )
    # Test case for leading/trailing spaces and multiple spaces
    assert (
        classifier.preprocess_text("  leading and trailing spaces  ")
        == "leading and trailing spaces"
    )
    # Test case for multiple spaces between words
    assert (
        classifier.preprocess_text("text with    multiple   spaces")
        == "text with multiple spaces"
    )


def test_preprocess_text_empty():
    """Unit test for empty string preprocessing."""
    classifier = TextClassifier()
    assert classifier.preprocess_text("") == ""
```

🔑 **TDD Principle**: Keep tests as your source of truth. If they fail, fix the implementation; if they pass, you've documented the behavior.

---

### 📝 Step 2: Save the file

💾 Save `tests/test_TextClassifier_unit.py` (Ctrl+S on Windows/Linux, Cmd+S on macOS).

---

### 📝 Step 3: Run just the unit tests and observe results (🔴 RED)

⌨️ Run the tests:

```bash
pytest tests/test_TextClassifier_unit.py -v
```

**Expected output**: If your `preprocess_text` matches the e-learning solution, many or all tests may already pass. If any fail, that’s your cue to tighten `preprocess_text()` in [src/TextClassifier.py](../src/TextClassifier.py) until they’re green.

---

### 📝 Step 4: Verify implementation (🟢 GREEN PHASE)

💻 The current implementation should take care of all these cases:

```python
def preprocess_text(self, text: str) -> str:
    """Cleans and normalizes a single text string."""
    text = text.lower()  # Handles mixed case ✓
    non_alphabetical_characters = r"[^a-z\s]"
    text = re.sub(non_alphabetical_characters, "", text)  # Removes punctuation, numbers ✓
    text = " ".join(text.split())  # Collapses spaces ✓
    return text
```

**Analysis**:
- `text.lower()` → Handles **mixed case** ✓
- `re.sub(r"[^a-z\s]", "", text)` → Removes **punctuation, numbers, symbols** ✓
- `" ".join(text.split())` → Removes **leading/trailing spaces** and **collapses multiple spaces** ✓

If any test fails, debug which assertion failed and adjust the implementation.

---

### 📝 Step 5: Ensure full test suite still passes

Your changes to unit tests shouldn't break integration or regression tests:

⌨️ Run all tests:

```bash
pytest tests/ -v
```

**Expected output**:
```
tests/test_TextClassifier_integration.py::test_end_to_end_pipeline_integration PASSED                                                                                   [ 25%]
tests/test_TextClassifier_regression.py::test_model_regression_accuracy PASSED                                                                                          [ 50%]
tests/test_TextClassifier_unit.py::test_preprocess_text_basic PASSED                                                                                                    [ 75%]
tests/test_TextClassifier_unit.py::test_preprocess_text_empty PASSED                                                                                                    [100%]
```

✅ **Checkpoint**: 100% of tests pass.

---

🎓 **Exercise 1 Complete!** You've successfully:
- ✅ Verified the e-learning tests work with the current implementation
- ✅ Confirmed unit tests in isolation
- ✅ Confirmed integration/regression tests still pass (system-level health check)

**This confirms the baseline works. Now let's practice real TDD by adding tests that FAIL first.**

---

## 📝 Exercise 1b: TDD in Action — Write Failing Tests First (🔴 RED → 🟢 GREEN)

🎯 **Goal**: Experience true TDD by adding tests for features the current `preprocess_text` does NOT handle. You'll see tests fail (RED), then update the implementation to make them pass (GREEN).

⏱️ **Time**: 25-35 minutes

**Why this matters**: The current implementation is intentionally limited. Real-world text data contains HTML tags, URLs, and accented characters. This exercise shows how TDD drives feature development—you write the test first, watch it fail, then implement the fix.

---

### 📝 Step 1: Add the failing tests (🔴 RED PHASE)

💻 Add these new test functions to the **end** of `tests/test_TextClassifier_unit.py`:

```python
# =============================================================================
# TDD EXERCISE: The following tests will FAIL with the current implementation.
# Students must update src/TextClassifier.py to make them pass.
# =============================================================================


def test_preprocess_text_html_tags():
    """TDD Exercise: HTML tags should be removed from text."""
    classifier = TextClassifier()
    assert classifier.preprocess_text("<p>Hello</p>") == "hello"
    assert classifier.preprocess_text("<div>Some <b>bold</b> text</div>") == "some bold text"
    assert classifier.preprocess_text("No tags here") == "no tags here"


def test_preprocess_text_urls():
    """TDD Exercise: URLs should be removed from text."""
    classifier = TextClassifier()
    assert classifier.preprocess_text("Visit https://example.com today") == "visit today"
    assert classifier.preprocess_text("Check http://test.org for info") == "check for info"
    assert classifier.preprocess_text("No URLs here") == "no urls here"


def test_preprocess_text_accented_characters():
    """TDD Exercise: Accented characters should be normalized to ASCII."""
    classifier = TextClassifier()
    assert classifier.preprocess_text("café") == "cafe"
    assert classifier.preprocess_text("résumé") == "resume"
    assert classifier.preprocess_text("naïve") == "naive"
    assert classifier.preprocess_text("El Niño") == "el nino"
```

💾 Save the file.

---

### 📝 Step 2: Run tests and confirm they fail (🔴 RED)

⌨️ Run the tests:

```bash
pytest tests/test_TextClassifier_unit.py -v
```

**Expected output**: You should see **3 failing tests** (out of 5 total unit tests):

```
tests/test_TextClassifier_unit.py::test_preprocess_text_basic PASSED
tests/test_TextClassifier_unit.py::test_preprocess_text_empty PASSED
tests/test_TextClassifier_unit.py::test_preprocess_text_html_tags FAILED
tests/test_TextClassifier_unit.py::test_preprocess_text_urls FAILED
tests/test_TextClassifier_unit.py::test_preprocess_text_accented_characters FAILED

========================= 3 failed, 2 passed in 0.12s =========================
```

**Why do they fail?** Let's analyze:

| Test | Input | Current Output | Expected | Problem |
|------|-------|---------------|----------|----------|
| HTML tags | `<p>Hello</p>` | `phellop` | `hello` | Tags treated as letters |
| URLs | `Visit https://example.com` | `visit httpsexamplecom` | `visit` | URL not removed |
| Accents | `café` | `caf` | `cafe` | Accented `é` removed entirely |

**This is TDD in action!** The tests define the behavior we want. Now we implement it.

---

### 📝 Step 3: Update `preprocess_text` to pass all tests (🟢 GREEN PHASE)

💻 Open `src/TextClassifier.py` and replace the `preprocess_text` method with this enhanced version:

```python
def preprocess_text(self, text: str) -> str:
    """
    Cleans and normalizes a single text string.
    - Removes HTML tags
    - Removes URLs
    - Normalizes accented characters to ASCII
    - Lowercases text
    - Removes non-alphabetic characters (keeping spaces)
    - Collapses multiple spaces
    """
    import unicodedata

    logging.debug(f"Preprocessing text: '{text}'")

    # Step 1: Remove HTML tags (before lowercasing to handle <P> vs <p>)
    text = re.sub(r"<[^>]+>", "", text)

    # Step 2: Remove URLs (http, https, www)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Step 3: Lowercase
    text = text.lower()

    # Step 4: Normalize accented characters to ASCII (é → e, ñ → n)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")

    # Step 5: Remove non-alphabetical characters (keeping spaces)
    non_alphabetical_characters = r"[^a-z\s]"
    text = re.sub(non_alphabetical_characters, "", text)

    # Step 6: Collapse multiple spaces and trim
    text = " ".join(text.split())

    logging.debug(f"Preprocessed text: '{text}'")
    return text
```

💾 Save the file.

**Key additions explained**:

1. **HTML removal**: `re.sub(r"<[^>]+>", "", text)` matches anything between `<` and `>`
2. **URL removal**: `re.sub(r"https?://\S+|www\.\S+", "", text)` matches http/https URLs
3. **Accent normalization**: `unicodedata.normalize("NFKD", ...)` decomposes `é` into `e` + combining accent, then `encode("ascii", "ignore")` drops the accent

---

### 📝 Step 4: Run tests again — all should pass (🟢 GREEN)

⌨️ Run the tests:

```bash
pytest tests/test_TextClassifier_unit.py -v
```

**Expected output**: All 5 unit tests should now pass:

```
tests/test_TextClassifier_unit.py::test_preprocess_text_basic PASSED
tests/test_TextClassifier_unit.py::test_preprocess_text_empty PASSED
tests/test_TextClassifier_unit.py::test_preprocess_text_html_tags PASSED
tests/test_TextClassifier_unit.py::test_preprocess_text_urls PASSED
tests/test_TextClassifier_unit.py::test_preprocess_text_accented_characters PASSED

========================= 5 passed in 0.02s =========================
```

🎉 **All tests pass!**

---

### 📝 Step 5: Verify full test suite still passes

Ensure your changes don't break integration or regression tests:

⌨️ Run all tests:

```bash
pytest tests/ -v
```

**Expected**: All 7 tests pass (5 unit + 1 integration + 1 regression).

---

### 🤔 Puzzler: Does Accent Normalization Actually Help?

We just implemented `café` → `cafe`. But pause and think:

> **Would normalising accents actually improve classification accuracy?**

Consider:
- If your training data contains `"café"` and test data contains `"cafe"`, they'd be treated as different words without normalization. So normalization **helps** by unifying them.
- But if your training data is mostly English and rarely contains accented words, does it matter?
- What if you're classifying French or Spanish text where accents carry meaning? (`"résumé"` vs `"resume"` mean different things!)

**The lesson**: Text preprocessing isn't about "cleaning" for its own sake—it's about making your model more accurate. Every preprocessing step should be justified by asking: *"Does this help the model generalize better?"*

This is why we test—if normalisation hurts accuracy on your specific dataset, your regression tests will catch it.

---

## 📝 Exercise 2: Add Experiment Tracking with MLflow

🎯 **Goal**: Instrument your training pipeline with MLflow to track experiments, then make a change and compare results.

⏱️ **Time**: 15-20 minutes

**Why this matters**: In Workshop 3 you have logged function calls to observe behaviour. In ML, you log *experiments*—each model training run with its hyperparameters and results. This lets you answer questions like "Did changing max_iter from 1000 to 2000 improve accuracy?"

---

### 📝 Step 1: Add MLflow to dependencies

💻 Edit [requirements.txt](../requirements.txt) and add:

```
mlflow==2.15.1
setuptools
```

⌨️ Then install (make sure your venv is activated):

```bash
source .venv/bin/activate  # if not already activated
pip install -r requirements.txt
```

---

### 📝 Step 2: Instrument the `train` method with MLflow logging

💻 Open [src/TextClassifier.py](../src/TextClassifier.py) and replace the `train` method with this version that tracks both **hyperparameters** and **accuracy**:

```python
def train(self, texts: list[str], labels: list[str]):
    """Trains the classification model with MLflow experiment tracking."""
    logging.info("Starting model training.")

    # Preprocess and vectorize
    processed_texts = [self.preprocess_text(text) for text in texts]
    X = self.vectorizer.fit_transform(processed_texts)
    y = labels

    # Train the model
    self.model.fit(X, y)

    # Calculate training accuracy
    train_accuracy = self.model.score(X, y)

    # ---- MLflow experiment tracking ----
    try:
        import mlflow
        mlflow.set_tracking_uri("file:./mlruns")
        mlflow.set_experiment("text-classifier")

        with mlflow.start_run():
            # Log hyperparameters (what we configured)
            mlflow.log_param("max_iter", self.model.max_iter)
            mlflow.log_param("model_type", type(self.model).__name__)
            mlflow.log_param("vectorizer_type", type(self.vectorizer).__name__)

            # Log metrics (what resulted)
            mlflow.log_metric("train_samples", len(texts))
            mlflow.log_metric("vocab_size", len(self.vectorizer.vocabulary_))
            mlflow.log_metric("train_accuracy", train_accuracy)

    except Exception as e:
        logging.info(f"MLflow logging skipped: {e}")

    logging.info(f"Model training completed. Training accuracy: {train_accuracy:.4f}")
```

💾 Save the file.

**What we're logging**:
- **Parameters**: `max_iter`, model type, vectorizer type (the choices we made)
- **Metrics**: Training samples, vocabulary size, and **training accuracy** (the results)

Now when you compare runs in MLflow UI, you'll see how accuracy changes with different hyperparameters!

---

### 📝 Step 3: Run the baseline experiment

⌨️ Run the app:

```bash
python app.py
```

This trains the model and logs the first experiment to MLflow. Note the output accuracy.

> ⚠️ **Note on accuracy**: You'll likely see `train_accuracy: 1.0` (100%) in your MLflow runs. This is because our toy dataset is very small (16 samples) with clearly distinct positive/negative examples—the model easily memorizes it perfectly. Don't worry! The value of this exercise isn't seeing accuracy change—it's **learning the MLflow workflow**: tracking parameters, logging metrics, and comparing runs. In a real project with hundreds or thousands of samples, you'd see meaningful differences when tuning hyperparameters.

---

### 📝 Step 4: Make a change to the model

💻 Open [src/TextClassifier.py](../src/TextClassifier.py) and modify the `__init__` method:

**Change this**:
```python
self.model = LogisticRegression(max_iter=1000)
```

**To this**:
```python
self.model = LogisticRegression(max_iter=2000)  # Increased iterations
```

💾 Save the file.

---

### 📝 Step 5: Run the modified experiment

⌨️ Run the app again:

```bash
python app.py
```

This trains the model again with the new hyperparameter and logs a second experiment. Note if accuracy changed.

---

### 📝 Step 6: Launch MLflow UI and compare runs

⌨️ First, make sure your venv is activated, then launch the UI:

```bash
source .venv/bin/activate  # if not already activated
mlflow ui --port 5000 --backend-store-uri file:./mlruns
```

**Open your browser**: http://localhost:5000

> 💡 **GitHub Codespaces users**: Your Codespace will automatically forward port 5000. Look for the "Ports" tab in VS Code and click the globe icon next to port 5000, or check the notification popup to open the forwarded URL (it will look like `https://<codespace-name>-5000.app.github.dev`).

You should see:
- **Experiments table**: Two runs with different `max_iter` values
- **Columns**: Start time, parameters (max_iter: 1000 vs 2000), metrics (accuracy, vocab_size)

**To compare**:
1. Select both runs (checkboxes)
2. Click **"Compare"** button
3. See side-by-side differences in parameters and metrics

🤔 **Questions to explore**:
- Did increasing `max_iter` change accuracy?
- Is vocabulary size the same? (It should be—vocab doesn't depend on model training)
- How long did each run take?

> 💡 **Tip**: You can also explore the `mlruns/` directory directly to see how MLflow stores data:
> ```bash
> tree mlruns/ -L 3
> ```
> Each run is stored as a folder with `params/`, `metrics/`, and `tags/` subdirectories containing plain text files. This makes MLflow data easy to inspect, version control, or back up.

---

### 🚀 Step 7: Experiment freely (optional)

Try other changes and observe in MLflow:

**A. Change regularization**:
```python
self.model = LogisticRegression(max_iter=1000, C=0.5)  # Stronger regularization
```

**B. Try a different model**:
```python
from sklearn.svm import LinearSVC
self.model = LinearSVC(max_iter=1000)
```

Each change creates a new run in MLflow. You can compare all of them to see what works best for your data.

---

**🎓 Exercise 2 Complete!** You've:
- ✅ Instrumented code with MLflow experiment tracking
- ✅ Run multiple experiments with different configurations
- ✅ Used MLflow UI to compare results visually
- ✅ Applied Workshop 3's observability habit to ML experimentation

**This shows how logging in ML differs from logging function calls—you log entire experiments, not individual operations.**

**Congratulations!** You've bridged pure-function TDD to *stateful* ML pipelines (pipelines that keep and transform data across multiple steps). The habits you practiced in Workshop 3, writing tests first, then observing behaviour, now apply to machine learning systems.

---

## 🚀 Going Further: Ideas for Exploration

You've completed the core bridge exercises. Here are directions you could explore next:

### Feature Engineering

- **Try TF-IDF**: Replace `CountVectorizer()` with `TfidfVectorizer()`
  - Downweights common words like "the", "is"
  - Often improves accuracy by 5-15%

- **Add bigrams**: `CountVectorizer(ngram_range=(1, 2))`
  - Captures phrases like "not good" (different from "good")
  - Compare with/without using MLflow

**Why not test these?** You'd be testing sklearn's implementation, not your code. Instead, use MLflow to compare performance—that's the ML way of validation.

### Model Improvements

- **Try different classifiers**: `LinearSVC`, `RandomForestClassifier`, `MultinomialNB`
- **Tune hyperparameters**: Vary `C` in LogisticRegression, try different solvers
- **Cross-validation**: Use `cross_val_score` for more robust accuracy estimates

Track everything in MLflow and compare which combinations work best!
