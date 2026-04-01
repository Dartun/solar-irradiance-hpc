#!/bin/bash
set -e

python src/features.py \
  --input data/processed/dallas_202401_processed.csv \
  --output data/processed/dallas_202401_features.csv

python src/train_baseline.py \
  --input data/processed/dallas_202401_features.csv \
  --metrics-out results/tables/dallas_202401_baseline_metrics.json \
  --plot-out results/figures/dallas_202401_baseline_comparison.png
