from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def find_data_start_line(filepath: Path) -> int:
    """
    Find the line number immediately after '-END HEADER-' in a NASA POWER CSV.
    Returns the 0-based line index to use as skiprows in pandas.
    """
    with filepath.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if line.strip() == "-END HEADER-":
                return i + 1
    raise ValueError(f"Could not find '-END HEADER-' in file: {filepath}")


def load_power_csv(filepath: Path) -> pd.DataFrame:
    """
    Load NASA POWER hourly CSV after skipping the metadata header.
    """
    skiprows = find_data_start_line(filepath)
    df = pd.read_csv(filepath, skiprows=skiprows)
    return df


def clean_power_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the NASA POWER dataframe.
    """
    # Rename columns for convenience
    rename_map = {
        "ALLSKY_SFC_SW_DWN": "ghi",
        "T2M": "temp_2m_c",
        "RH2M": "rh_2m_pct",
        "WS2M": "wind_2m_mps",
        "PS": "surface_pressure_kpa",
    }
    df = df.rename(columns=rename_map)

    # Create timestamp from YEAR, MO, DY, HR
    df["timestamp"] = pd.to_datetime(
        df[["YEAR", "MO", "DY", "HR"]].rename(
            columns={"YEAR": "year", "MO": "month", "DY": "day", "HR": "hour"}
        ),
        utc=True,
    )

    # Keep useful columns in a clean order
    keep_cols = [
        "timestamp",
        "ghi",
        "temp_2m_c",
        "rh_2m_pct",
        "wind_2m_mps",
        "surface_pressure_kpa",
    ]
    df = df[keep_cols].copy()

    # Replace NASA missing-value flag (-999) with NaN
    df = df.replace(-999, pd.NA)

    # Convert numeric columns
    numeric_cols = [
        "ghi",
        "temp_2m_c",
        "rh_2m_pct",
        "wind_2m_mps",
        "surface_pressure_kpa",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort by time and reset index
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Create 1-hour-ahead forecasting target
    df["ghi_tplus1"] = df["ghi"].shift(-1)

    # Drop final row with missing future target
    df = df.dropna(subset=["ghi_tplus1"]).reset_index(drop=True)

    return df


def make_quick_plot(df: pd.DataFrame, output_path: Path) -> None:
    """
    Make a quick time series plot of GHI.
    """
    plt.figure(figsize=(10, 4))
    plt.plot(df["timestamp"], df["ghi"])
    plt.xlabel("Timestamp")
    plt.ylabel("GHI (Wh/m^2)")
    plt.title("Hourly GHI")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess NASA POWER hourly CSV.")
    parser.add_argument("--site", required=True, help="Site name")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to raw NASA POWER CSV file",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to save processed CSV file",
    )
    parser.add_argument(
        "--plot",
        required=True,
        help="Path to save quick-look plot",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    plot_path = Path(args.plot)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plot_path.parent.mkdir(parents=True, exist_ok=True)

    df_raw = load_power_csv(input_path)
    df_clean = clean_power_dataframe(df_raw)
    df_clean["site"] = args.site
    df_clean = df_clean[
        [
            "site",
            "timestamp",
            "ghi",
            "temp_2m_c",
            "rh_2m_pct",
            "wind_2m_mps",
            "surface_pressure_kpa",
            "ghi_tplus1",
        ]
    ]

    df_clean.to_csv(output_path, index=False)
    make_quick_plot(df_clean, plot_path)

    print(f"Input file:      {input_path}")
    print(f"Processed rows:  {len(df_clean)}")
    print(f"Output CSV:      {output_path}")
    print(f"Output plot:     {plot_path}")
    print("\nColumns:")
    print(df_clean.columns.tolist())
    print("\nFirst 5 rows:")
    print(df_clean.head())


if __name__ == "__main__":
    main()

