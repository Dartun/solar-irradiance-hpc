from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
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


def persistence_forecast(test_df: pd.DataFrame) -> np.ndarray:
    return test_df["ghi"].to_numpy()


def linear_regression_forecast(train_df: pd.DataFrame, test_df: pd.DataFrame) -> np.ndarray:
    model = LinearRegression()
    X_train = train_df[FEATURE_COLUMNS].to_numpy()
    y_train = train_df[TARGET_COLUMN].to_numpy()
    X_test = test_df[FEATURE_COLUMNS].to_numpy()
    model.fit(X_train, y_train)
    return model.predict(X_test)


def random_forest_forecast(train_df: pd.DataFrame, test_df: pd.DataFrame) -> np.ndarray:
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    )
    X_train = train_df[FEATURE_COLUMNS].to_numpy()
    y_train = train_df[TARGET_COLUMN].to_numpy()
    X_test = test_df[FEATURE_COLUMNS].to_numpy()
    model.fit(X_train, y_train)
    return model.predict(X_test)


def evaluate_subset(y_true: np.ndarray, preds: dict[str, np.ndarray], mask: np.ndarray) -> dict[str, dict[str, float]]:
    out = {}
    for model_name, y_pred in preds.items():
        out[model_name] = compute_metrics(y_true[mask], y_pred[mask])
    return out


def make_bar_plot(metrics: dict, output_path: Path) -> None:
    model_names = ["persistence", "linear_regression", "random_forest"]

    all_rmse = [metrics["all_hours"][m]["rmse"] for m in model_names]
    day_rmse = [metrics["daylight_only"][m]["rmse"] for m in model_names]

    x = np.arange(len(model_names))
    width = 0.35

    plt.figure(figsize=(8, 4))
    plt.bar(x - width / 2, all_rmse, width, label="All hours")
    plt.bar(x + width / 2, day_rmse, width, label="Daylight only")
    plt.xticks(x, model_names, rotation=20)
    plt.ylabel("RMSE")
    plt.title("All-hours vs Daylight-only RMSE")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate solar forecasting models on all hours and daylight-only hours.")
    parser.add_argument("--input", required=True, help="Path to combined feature CSV")
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

    preds = {
        "persistence": persistence_forecast(test_df),
        "linear_regression": linear_regression_forecast(train_df, test_df),
        "random_forest": random_forest_forecast(train_df, test_df),
    }

    all_mask = np.ones(len(test_df), dtype=bool)
    daylight_mask = y_true > 0

    results = {
        "n_test_all_hours": int(all_mask.sum()),
        "n_test_daylight_only": int(daylight_mask.sum()),
        "all_hours": evaluate_subset(y_true, preds, all_mask),
        "daylight_only": evaluate_subset(y_true, preds, daylight_mask),
    }

    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    make_bar_plot(results, plot_path)

    print(f"Saved metrics to: {metrics_path}")
    print(f"Saved plot to:    {plot_path}")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
