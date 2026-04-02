#!/bin/bash
set -e

python src/benchmark_repeated.py \
  --output results/tables/week7_repeated_benchmark_raw.csv \
  --repeats 5

python src/summarize_benchmarks.py \
  --input results/tables/week7_repeated_benchmark_raw.csv \
  --output results/tables/week7_benchmark_summary.csv

python src/plot_benchmark_summary.py \
  --input results/tables/week7_benchmark_summary.csv \
  --runtime-plot results/figures/week7_mean_runtime.png \
  --speedup-plot results/figures/week7_mean_speedup.png \
  --errorbar-plot results/figures/week7_runtime_errorbars.png
