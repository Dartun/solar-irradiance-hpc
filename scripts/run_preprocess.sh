#!/bin/bash
set -e

python src/preprocess.py \
  --input data/raw/nasa_power/dallas_202401_power.csv \
  --output data/processed/dallas_202401_processed.csv \
  --plot results/figures/dallas_202401_ghi.png
