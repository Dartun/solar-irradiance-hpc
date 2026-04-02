#!/bin/bash
set -e

python src/preprocess.py \
  --site dallas \
  --input data/raw/nasa_power/dallas_20240101_20240331_power.csv \
  --output data/processed/dallas_202401_202403_processed.csv \
  --plot results/figures/dallas_202401_202403_ghi.png

python src/preprocess.py \
  --site phoenix \
  --input data/raw/nasa_power/phoenix_20240101_20240331_power.csv \
  --output data/processed/phoenix_202401_202403_processed.csv \
  --plot results/figures/phoenix_202401_202403_ghi.png

python src/preprocess.py \
  --site seattle \
  --input data/raw/nasa_power/seattle_20240101_20240331_power.csv \
  --output data/processed/seattle_202401_202403_processed.csv \
  --plot results/figures/seattle_202401_202403_ghi.png

python src/features.py \
  --input data/processed/dallas_202401_202403_processed.csv \
  --output data/processed/dallas_202401_202403_features.csv

python src/features.py \
  --input data/processed/phoenix_202401_202403_processed.csv \
  --output data/processed/phoenix_202401_202403_features.csv

python src/features.py \
  --input data/processed/seattle_202401_202403_processed.csv \
  --output data/processed/seattle_202401_202403_features.csv

python src/combine_features.py \
  --inputs \
    data/processed/dallas_202401_202403_features.csv \
    data/processed/phoenix_202401_202403_features.csv \
    data/processed/seattle_202401_202403_features.csv \
  --output data/processed/combined_3site_202401_202403_features.csv
