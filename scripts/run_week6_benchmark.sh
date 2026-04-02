#!/bin/bash
set -e

python src/benchmark_pipeline.py \
  --output results/tables/week6_benchmark_results.csv

python src/plot_benchmarks.py \
  --input results/tables/week6_benchmark_results.csv \
  --runtime-plot results/figures/week6_runtime_comparison.png \
  --speedup-plot results/figures/week6_speedup.png
