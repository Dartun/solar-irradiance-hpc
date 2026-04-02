#!/bin/bash
set -e

python src/train_models.py \
  --input data/processed/combined_3site_202401_202403_features.csv \
  --metrics-out results/tables/combined_3site_202401_202403_model_metrics.json \
  --plot-out results/figures/combined_3site_202401_202403_model_comparison.png \
  --importance-out results/figures/combined_3site_202401_202403_rf_feature_importance.png
