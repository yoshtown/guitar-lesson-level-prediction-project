"""
Evaluate the best run from MLflow and promote it to champion
if it beats the current baseline.

Usage:
    python scripts/evaluate_and_promote.py
"""

import os
import sys
import mlflow
import dagshub
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DAGSHUB_USERNAME = os.environ["DAGSHUB_USERNAME"]
DAGSHUB_REPO = "guitar-lesson-level-prediction-project"
EXPERIMENT_NAME = "guitar-lesson-difficulty-classifierv2"
PROMOTION_THRESHOLD = 0.01  # challenger must beat champion by this much to promote

# ---------------------------------------------------------------------------
# Connect to DagsHub MLflow
# ---------------------------------------------------------------------------

dagshub.init(repo_owner=DAGSHUB_USERNAME, repo_name=DAGSHUB_REPO, mlflow=True)

client = mlflow.tracking.MlflowClient()

# ---------------------------------------------------------------------------
# Get best challenger run by f1 score
# ---------------------------------------------------------------------------

experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
if experiment is None:
    raise ValueError(f"Experiment '{EXPERIMENT_NAME}' not found on DagsHub.")

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.f1 DESC"],
    max_results=1,
)

if not runs:
    raise ValueError("No runs found in experiment.")

best_run = runs[0]
challenger_f1 = best_run.data.metrics.get("f1")
run_id = best_run.info.run_id

print(f"Best challenger run: {best_run.info.run_name}")
print(f"Challenger F1:       {challenger_f1:.4f}")
print(f"Run ID:              {run_id}")

# ---------------------------------------------------------------------------
# Compare against current champion
# ---------------------------------------------------------------------------

champion_score_path = Path("api/champion_f1.txt")

if champion_score_path.exists():
    champion_f1 = float(champion_score_path.read_text().strip())
    print(f"Current champion F1: {champion_f1:.4f}")
else:
    champion_f1 = 0.0
    print("No champion found — first promotion.")

# ---------------------------------------------------------------------------
# Promote if challenger is better
# ---------------------------------------------------------------------------

if challenger_f1 > champion_f1 + PROMOTION_THRESHOLD:
    print(f"✅ Challenger beats champion by {challenger_f1 - champion_f1:.4f} — promoting.")

    # Record the winning run ID and F1 score
    champion_score_path.parent.mkdir(parents=True, exist_ok=True)
    champion_score_path.write_text(str(challenger_f1))

    run_id_path = Path("api/champion_run_id.txt")
    run_id_path.write_text(run_id)

    print(f"✅ Champion F1 updated to {challenger_f1:.4f}")
    print(f"✅ Champion run ID saved: {run_id}")
    print("ℹ️  Export pipeline.pkl from this run in your notebook to deploy.")

    # Exit with code 0 = promotion happened (used by CI to trigger redeploy)
    sys.exit(0)

else:
    print(f"❌ Challenger does not beat champion by threshold ({PROMOTION_THRESHOLD}) — no promotion.")

    # Exit with code 1 = no promotion (CI skips redeploy)
    sys.exit(1)