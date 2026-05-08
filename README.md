# Solar Irradiance HPC Project

Performance-aware one-hour-ahead solar irradiance forecasting using public meteorological data, developed as a graduate HPC course project. This project develops a reproducible, performance-aware workflow for **1-hour-ahead solar irradiance forecasting** using public meteorological data and evaluates both **forecasting accuracy** and **computational performance** on the **Ganymede HPC system**. It focuses on forecasting **Global Horizontal Irradiance (GHI)** using hourly NASA POWER data from multiple U.S. sites and compares both simple and more advanced machine learning models. In addition to the scientific forecasting task, the project includes an explicit HPC component through **serial vs parallel benchmarking**, **speedup analysis**, **efficiency analysis**, and **repeated-run performance evaluation**.

## Project summary
This repository implements a clean, reproducible workflow for forecasting **global horizontal irradiance (GHI)** from hourly meteorological predictors. The project combines:

- public **NASA POWER** hourly Renewable Energy data
- reproducible preprocessing and feature engineering
- baseline and nonlinear models
- **multi-site** experiments across different US climates
- **serial vs parallel** benchmarking on an HPC system
- **daylight-only** evaluation for a more realistic scientific assessment

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

## Research motivation
Accurate short-horizon irradiance forecasts matter for:

- solar resource assessment
- operational planning for solar energy systems
- understanding how meteorological variability affects near-term surface radiation
- demonstrating how performance-aware workflows improve scientific computing pipelines

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

## Study design
### Sites Used
Three climatically distinct U.S. sites were used:

- **Dallas, Texas** — warm continental / convective regime
  - Latitude: 32.7767
  - Longitude: -96.7970

- **Phoenix, Arizona** — sunny arid regime
  - Latitude: 33.4484
  - Longitude: -112.0740

- **Seattle, Washington** — cloudier marine regime
  - Latitude: 47.6062
  - Longitude: -122.3321

### Time Range
- **January 1, 2024 to March 31, 2024**
- Hourly temporal resolution
- UTC time standard
### Time period
- **2024-01-01 to 2024-03-31**

### Variables downloaded from NASA POWER
- `ALLSKY_SFC_SW_DWN` → surface shortwave downward irradiance (used as GHI-like target)
- `T2M` → temperature at 2 m
- `RH2M` → relative humidity at 2 m
- `WS2M` → wind speed at 2 m
- `PS` → surface pressure
### Forecast target
- **1-hour-ahead GHI** (`ghi_tplus1`)

## Repository structure
```text
solar-irradiance-hpc/
├── README.md
├── requirements.txt
├── src/
│   ├── download_power.py
│   ├── preprocess.py
│   ├── features.py
│   ├── combine_features.py
│   ├── train_baseline.py
│   ├── train_models.py
│   ├── benchmark_pipeline.py
│   ├── benchmark_repeated.py
│   ├── summarize_benchmarks.py
│   ├── plot_benchmarks.py
│   ├── plot_benchmark_summary.py
│   └── evaluate_daylight.py
├── slurm/
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
├── data/
│   ├── raw/
│   └── processed/
├── results/
│   ├── figures/
│   └── tables/
└── reports/
└── tests/
```

## Workflow
### 1. Download
Pull hourly NASA POWER point data for each site.

### 2. Preprocess
- skip metadata header
- parse timestamps
- standardize variables
- create `ghi_tplus1`

### 3. Feature engineering
Add:
- hour-of-day and day-of-year features
- cyclic encodings (`sin`, `cos`)
- lagged irradiance features
- rolling mean irradiance

### 4. Modeling
Compare:
- **Persistence**
- **Linear Regression**
- **Random Forest**

### 5. HPC benchmarking
Benchmark:
- serial preprocessing + feature generation
- parallel preprocessing + feature generation
- repeated runs for runtime mean and standard deviation

### 6. Scientific evaluation
Evaluate on:
- **all hours**
- **daylight-only hours** (`ghi_tplus1 > 0`)

## Main findings
### Multi-site all-hours forecasting
On the combined 3-site dataset:

| Model | RMSE | MAE | R² |
|---|---:|---:|---:|
| Persistence | 54.73 | 32.75 | 0.883 |
| Linear Regression | 35.00 | 23.34 | 0.952 |
| Random Forest | 35.10 | 19.89 | 0.952 |

### Daylight-only evaluation
Removing nighttime hours makes the forecasting problem harder, but learned models still clearly outperform persistence:

| Model | RMSE (Daylight) | MAE (Daylight) | R² (Daylight) |
|---|---:|---:|---:|
| Persistence | 77.93 | 65.58 | 0.793 |
| Linear Regression | 45.31 | 31.47 | 0.930 |
| Random Forest | 44.96 | 33.01 | 0.931 |

### Repeated benchmark summary
Mean runtime across 5 runs:

| Configuration | Mean runtime (s) | Std dev (s) | Mean speedup |
|---|---:|---:|---:|
| Serial (1 worker) | 21.70 | 2.32 | — |
| Parallel (2 workers) | 13.97 | 0.27 | 1.55 |
| Parallel (3 workers) | 6.89 | 0.13 | 3.15 |

## Reproducibility
This project was developed to run cleanly on an HPC environment such as **Ganymede**.

Typical workflow:
1. Clone the repository
2. Create and activate a Python virtual environment
3. Install dependencies
4. Run the stage-specific shell scripts in `scripts/`

Example:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/run_week5_download.sh
./scripts/run_week5_process.sh
./scripts/run_week5_train.sh
./scripts/run_week7_benchmark.sh
./scripts/run_week8_daylight.sh
```

## Data management
Large raw data files and generated outputs should stay **out of GitHub**. Track:
- source code
- scripts
- requirements
- README
- final lightweight documentation

Ignore:
- `data/raw/`
- `data/processed/`
- `results/figures/`
- `results/tables/`

## Future work
- extend to a longer seasonal record
- add NSRDB or ERA5 as complementary datasets
- test GPU-based or distributed model workflows
- run larger-scale Slurm parameter sweeps
- add uncertainty quantification and site-aware modeling

## Data source
NASA POWER Renewable Energy API  
https://power.larc.nasa.gov/

## License / academic note
This repository was created as an academic course project. Please cite the data source appropriately and adapt the workflow responsibly for any downstream use.
