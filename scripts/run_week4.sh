#!/bin/bash
set -e

python src/train_models.py \
  --input data/processed/dallas_202401_features.csv \
  --metrics-out results/tables/dallas_202401_model_metrics.json \
  --plot-out results/figures/dallas_202401_model_comparison.png \
  --importance-out results/figures/dallas_202401_rf_feature_importance.png
