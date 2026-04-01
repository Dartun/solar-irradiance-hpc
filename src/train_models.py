from __future__ import annotations

import argparse
from pathlib import Path
import json

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


def random_forest_forecast(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
) -> tuple[np.ndarray, RandomForestRegressor]:
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1,
    )

    X_train = train_df[FEATURE_COLUMNS].to_numpy()
    y_train = train_df[TARGET_COLUMN].to_numpy()
    X_test = test_df[FEATURE_COLUMNS].to_numpy()

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred, model


def make_comparison_plot(
    test_df: pd.DataFrame,
    y_persist: np.ndarray,
    y_lr: np.ndarray,
    y_rf: np.ndarray,
    output_path: Path,
) -> None:
    y_true = test_df[TARGET_COLUMN].to_numpy()

    plt.figure(figsize=(11, 4))
    plt.plot(test_df["timestamp"], y_true, label="True GHI(t+1)")
    plt.plot(test_df["timestamp"], y_persist, label="Persistence", alpha=0.8)
    plt.plot(test_df["timestamp"], y_lr, label="Linear Regression", alpha=0.8)
    plt.plot(test_df["timestamp"], y_rf, label="Random Forest", alpha=0.8)
    plt.xlabel("Timestamp")
    plt.ylabel("GHI (Wh/m^2)")
    plt.title("Forecast Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def make_feature_importance_plot(model: RandomForestRegressor, output_path: Path) -> None:
    importances = model.feature_importances_
    order = np.argsort(importances)[::-1]

    sorted_features = [FEATURE_COLUMNS[i] for i in order]
    sorted_importances = importances[order]

    plt.figure(figsize=(9, 5))
    plt.bar(sorted_features, sorted_importances)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Feature")
    plt.ylabel("Importance")
    plt.title("Random Forest Feature Importances")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Train multiple solar irradiance forecasting models.")
    parser.add_argument("--input", required=True, help="Path to feature CSV")
    parser.add_argument("--metrics-out", required=True, help="Path to save metrics JSON")
    parser.add_argument("--plot-out", required=True, help="Path to save forecast comparison plot")
    parser.add_argument(
        "--importance-out",
        required=True,
        help="Path to save random forest feature importance plot",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    metrics_path = Path(args.metrics_out)
    plot_path = Path(args.plot_out)
    importance_path = Path(args.importance_out)

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    importance_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, parse_dates=["timestamp"])
    train_df, test_df = time_split(df, train_frac=0.8)

    y_true = test_df[TARGET_COLUMN].to_numpy()

    y_persist = persistence_forecast(test_df)
    persist_metrics = compute_metrics(y_true, y_persist)

    y_lr = linear_regression_forecast(train_df, test_df)
    lr_metrics = compute_metrics(y_true, y_lr)

    y_rf, rf_model = random_forest_forecast(train_df, test_df)
    rf_metrics = compute_metrics(y_true, y_rf)

    all_metrics = {
        "persistence": persist_metrics,
        "linear_regression": lr_metrics,
        "random_forest": rf_metrics,
        "n_train": len(train_df),
        "n_test": len(test_df),
        "random_forest_config": {
            "n_estimators": 200,
            "random_state": 42,
            "n_jobs": -1,
        },
    }

    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(all_metrics, f, indent=2)

    make_comparison_plot(test_df, y_persist, y_lr, y_rf, plot_path)
    make_feature_importance_plot(rf_model, importance_path)

    print("Train size:", len(train_df))
    print("Test size:", len(test_df))

    print("\nPersistence metrics:")
    print(persist_metrics)

    print("\nLinear regression metrics:")
    print(lr_metrics)

    print("\nRandom forest metrics:")
    print(rf_metrics)

    print(f"\nSaved metrics to: {metrics_path}")
    print(f"Saved comparison plot to: {plot_path}")
    print(f"Saved importance plot to: {importance_path}")


if __name__ == "__main__":
    main()

