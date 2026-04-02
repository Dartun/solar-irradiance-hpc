from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize repeated benchmark results.")
    parser.add_argument("--input", required=True, help="Raw repeated benchmark CSV")
    parser.add_argument("--output", required=True, help="Summary CSV")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    df["speedup_vs_serial"] = pd.to_numeric(df["speedup_vs_serial"], errors="coerce")
    df["efficiency"] = pd.to_numeric(df["efficiency"], errors="coerce")

    summary = (
        df.groupby(["mode", "workers", "n_sites"], as_index=False)
        .agg(
            mean_runtime_seconds=("runtime_seconds", "mean"),
            std_runtime_seconds=("runtime_seconds", "std"),
            mean_speedup_vs_serial=("speedup_vs_serial", "mean"),
            std_speedup_vs_serial=("speedup_vs_serial", "std"),
            mean_efficiency=("efficiency", "mean"),
            std_efficiency=("efficiency", "std"),
            n_runs=("runtime_seconds", "count"),
        )
    )

    summary.to_csv(output_path, index=False)

    print(f"Saved benchmark summary to: {output_path}")
    print(summary)


if __name__ == "__main__":
    main()
