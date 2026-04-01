from __future__ import annotations

import argparse
from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


FEATURE_COLUMNS = [
    "ghi",
    "temp_2m_c",
    "rh_2m_pct",
    "wind_2m_mps",
    "surface_pressure_kpa",
    "hour_sin",
    "hour_cos",
    "doy_sin",
    "doy_cos",
    "ghi_lag_1",
    "ghi_lag_2",
    "ghi_lag_3",
    "ghi_roll3",
]

TARGET_COLUMN = "ghi_tplus1"


def time_split(df: pd.DataFrame, train_frac: float = 0.8) -> tuple[pd.DataFrame, pd.DataFrame]:
    n = len(df)
    split_idx = int(train_frac * n)
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()
    return train_df, test_df


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    return {"rmse": rmse, "mae": mae, "r2": r2}


def persistence_forecast(df: pd.DataFrame) -> np.ndarray:
    return df["ghi"].to_numpy()


def linear_regression_forecast(train_df: pd.DataFrame, test_df: pd.DataFrame) -> np.ndarray:
    model = LinearRegression()
    X_train = train_df[FEATURE_COLUMNS].to_numpy()
    y_train = train_df[TARGET_COLUMN].to_numpy()

    X_test = test_df[FEATURE_COLUMNS].to_numpy()

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred


def make_comparison_plot(test_df: pd.DataFrame, y_persist: np.ndarray, y_lr: np.ndarray, output_path: Path) -> None:
    y_true = test_df[TARGET_COLUMN].to_numpy()

    plt.figure(figsize=(10, 4))
    plt.plot(test_df["timestamp"], y_true, label="True GHI(t+1)")
    plt.plot(test_df["timestamp"], y_persist, label="Persistence", alpha=0.8)
    plt.plot(test_df["timestamp"], y_lr, label="Linear Regression", alpha=0.8)
    plt.xlabel("Timestamp")
    plt.ylabel("GHI (Wh/m^2)")
    plt.title("Baseline Forecast Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Train baseline solar irradiance forecasting models.")
    parser.add_argument("--input", required=True, help="Path to feature CSV")
    parser.add_argument("--metrics-out", required=True, help="Path to save metrics JSON")
    parser.add_argument("--plot-out", required=True, help="Path to save comparison plot")
    args = parser.parse_args()

    input_path = Path(args.input)
    metrics_path = Path(args.metrics_out)
    plot_path = Path(args.plot_out)

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    plot_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, parse_dates=["timestamp"])
    train_df, test_df = time_split(df, train_frac=0.8)

    y_true = test_df[TARGET_COLUMN].to_numpy()

    y_persist = persistence_forecast(test_df)
    persist_metrics = compute_metrics(y_true, y_persist)

    y_lr = linear_regression_forecast(train_df, test_df)
    lr_metrics = compute_metrics(y_true, y_lr)

    all_metrics = {
        "persistence": persist_metrics,
        "linear_regression": lr_metrics,
        "n_train": len(train_df),
        "n_test": len(test_df),
    }

    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(all_metrics, f, indent=2)

    make_comparison_plot(test_df, y_persist, y_lr, plot_path)

    print("Train size:", len(train_df))
    print("Test size:", len(test_df))
    print("\nPersistence metrics:")
    print(persist_metrics)
    print("\nLinear regression metrics:")
    print(lr_metrics)
    print(f"\nSaved metrics to: {metrics_path}")
    print(f"Saved plot to:    {plot_path}")


if __name__ == "__main__":
    main()
