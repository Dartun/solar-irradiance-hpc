# Solar Irradiance HPC Project

## Performance-Aware Solar Irradiance Forecasting Using Public Meteorological Data on HPC Systems

This project develops a reproducible, performance-aware workflow for **1-hour-ahead solar irradiance forecasting** using public meteorological data and evaluates both **forecasting accuracy** and **computational performance** on the **Ganymede HPC system**.

The project focuses on forecasting **Global Horizontal Irradiance (GHI)** using hourly NASA POWER data from multiple U.S. sites and compares both simple and more advanced machine learning models. In addition to the scientific forecasting task, the project includes an explicit HPC component through **serial vs parallel benchmarking**, **speedup analysis**, **efficiency analysis**, and **repeated-run performance evaluation**.

---

## Project Overview

Solar irradiance forecasting is important for:

- solar energy system planning
- photovoltaic performance estimation
- short-term grid integration
- renewable energy operations

This project addresses the problem of **1-hour-ahead GHI forecasting** using publicly available meteorological and solar-resource variables. The workflow was designed not only to produce useful predictions, but also to demonstrate HPC-oriented ideas such as:

- reproducible data pipelines
- performance-aware workflow design
- serial vs parallel execution
- runtime benchmarking
- repeated-run timing analysis
- scaling interpretation

---

## Project Objectives

The main objectives of this project are:

1. Build a clean and reproducible workflow for hourly solar irradiance forecasting.
2. Use public meteorological data to predict **1-hour-ahead GHI**.
3. Compare forecasting models of increasing complexity:
   - persistence baseline
   - linear regression
   - random forest regression
4. Expand the study from a single site to a multi-site dataset.
5. Evaluate model performance under:
   - all-hours conditions
   - daylight-only conditions
6. Benchmark the preprocessing and feature-generation pipeline under:
   - serial execution
   - parallel execution
7. Quantify HPC performance using:
   - wall-clock runtime
   - speedup
   - efficiency
   - repeated-run timing statistics

---

## Datasets Used

### NASA POWER Hourly Data
This project uses **NASA POWER hourly point data** for the Renewable Energy community.

Variables used:

- `ALLSKY_SFC_SW_DWN` → surface shortwave downward irradiance (used as GHI-like target)
- `T2M` → temperature at 2 m
- `RH2M` → relative humidity at 2 m
- `WS2M` → wind speed at 2 m
- `PS` → surface pressure

### Sites Used
Three climatically distinct U.S. sites were used:

- **Dallas, Texas**
  - Latitude: 32.7767
  - Longitude: -96.7970

- **Phoenix, Arizona**
  - Latitude: 33.4484
  - Longitude: -112.0740

- **Seattle, Washington**
  - Latitude: 47.6062
  - Longitude: -122.3321

### Time Range
- **January 1, 2024 to March 31, 2024**
- Hourly temporal resolution
- UTC time standard

---

## Forecasting Task

### Target
Predict **1-hour-ahead Global Horizontal Irradiance (GHI)**.

### Target definition
For each time step `t`, the model predicts:

- `GHI(t+1)`

### Why this target?
This gives a realistic short-term forecasting problem and is directly relevant to solar-energy applications.

---

## Repository Structure

```text
solar-irradiance-hpc/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── results/
│   ├── figures/
│   └── tables/
├── reports/
├── scripts/
│   ├── run_preprocess.sh
│   ├── run_week3.sh
│   ├── run_week4.sh
│   ├── run_week5_download.sh
│   ├── run_week5_process.sh
│   ├── run_week5_train.sh
│   ├── run_week6_benchmark.sh
│   ├── run_week7_benchmark.sh
│   └── run_week8_daylight.sh
├── slurm/
├── src/
│   ├── __init__.py
│   ├── preprocess.py
│   ├── features.py
│   ├── train_baseline.py
│   ├── train_models.py
│   ├── download_power.py
│   ├── combine_features.py
│   ├── benchmark_pipeline.py
│   ├── plot_benchmarks.py
│   ├── benchmark_repeated.py
│   ├── summarize_benchmarks.py
│   ├── plot_benchmark_summary.py
│   └── evaluate_daylight.py
└── tests/
