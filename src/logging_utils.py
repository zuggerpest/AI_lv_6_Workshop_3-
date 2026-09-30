"""
MLflow logging utilities for the workshop.
These functions are safe to import even if MLflow isn't installed; they will no-op with a friendly message.
"""
from typing import Dict, Any

def log_experiment(order: Dict[str, Any], prediction: bool, experiment_name: str = "hotdog-upsell", run_name: str = "workshop-run") -> None:
    try:
        import mlflow  # type: ignore
    except Exception as e:
        print("[INFO] MLflow not installed in this environment. Skipping logging.")
        print("       To enable logging, install MLflow (pin recommended): pip install mlflow==2.15.1")
        return

    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name):
        mlflow.log_params(order)
        mlflow.log_metric("prediction", int(bool(prediction)))
        mlflow.set_tag("rule_version", "v1")
        print("[MLflow] Experiment run logged successfully.")
