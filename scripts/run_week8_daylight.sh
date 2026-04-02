#!/bin/bash
set -e

python src/evaluate_daylight.py \
  --input data/processed/combined_3site_202401_202403_features.csv \
  --metrics-out results/tables/week8_daylight_metrics.json \
  --plot-out results/figures/week8_daylight_rmse_comparison.png
