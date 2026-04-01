from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["hour"] = df["timestamp"].dt.hour
    df["day_of_year"] = df["timestamp"].dt.dayofyear

    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24.0)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24.0)

    df["doy_sin"] = np.sin(2 * np.pi * df["day_of_year"] / 365.0)
    df["doy_cos"] = np.cos(2 * np.pi * df["day_of_year"] / 365.0)

    return df


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ghi_lag_1"] = df["ghi"].shift(1)
    df["ghi_lag_2"] = df["ghi"].shift(2)
    df["ghi_lag_3"] = df["ghi"].shift(3)

    df["ghi_roll3"] = df["ghi"].rolling(window=3).mean()

    return df


def build_feature_table(df: pd.DataFrame) -> pd.DataFrame:
    df = add_time_features(df)
    df = add_lag_features(df)

    df = df.dropna().reset_index(drop=True)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Create features for solar irradiance forecasting.")
    parser.add_argument("--input", required=True, help="Path to processed CSV")
    parser.add_argument("--output", required=True, help="Path to save feature CSV")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, parse_dates=["timestamp"])
    df_feat = build_feature_table(df)

    df_feat.to_csv(output_path, index=False)

    print(f"Input file:     {input_path}")
    print(f"Output file:    {output_path}")
    print(f"Feature rows:   {len(df_feat)}")
    print("Columns:")
    print(df_feat.columns.tolist())
    print("\nFirst 5 rows:")
    print(df_feat.head())


if __name__ == "__main__":
    main()
