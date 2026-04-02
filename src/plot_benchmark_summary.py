from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot repeated benchmark summary results.")
    parser.add_argument("--input", required=True, help="Summary CSV")
    parser.add_argument("--runtime-plot", required=True, help="Output mean runtime plot")
    parser.add_argument("--speedup-plot", required=True, help="Output mean speedup plot")
    parser.add_argument("--errorbar-plot", required=True, help="Output runtime errorbar plot")
    args = parser.parse_args()

    input_path = Path(args.input)
    runtime_plot = Path(args.runtime_plot)
    speedup_plot = Path(args.speedup_plot)
    errorbar_plot = Path(args.errorbar_plot)

    runtime_plot.parent.mkdir(parents=True, exist_ok=True)
    speedup_plot.parent.mkdir(parents=True, exist_ok=True)
    errorbar_plot.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    labels = [f"{row['mode']}-{int(row['workers'])}" for _, row in df.iterrows()]

    # Mean runtime bar plot
    plt.figure(figsize=(7, 4))
    plt.bar(labels, df["mean_runtime_seconds"])
    plt.xlabel("Configuration")
    plt.ylabel("Mean Runtime (s)")
    plt.title("Mean Runtime Across Repeated Runs")
    plt.tight_layout()
    plt.savefig(runtime_plot, dpi=150)
    plt.close()

    # Mean speedup plot
    parallel_df = df[df["mode"] == "parallel"].copy()

    plt.figure(figsize=(7, 4))
    plt.plot(parallel_df["workers"], parallel_df["mean_speedup_vs_serial"], marker="o")
    plt.xlabel("Workers")
    plt.ylabel("Mean Speedup vs Serial")
    plt.title("Mean Parallel Speedup")
    plt.tight_layout()
    plt.savefig(speedup_plot, dpi=150)
    plt.close()

    # Runtime errorbar plot
    plt.figure(figsize=(7, 4))
    plt.errorbar(
        labels,
        df["mean_runtime_seconds"],
        yerr=df["std_runtime_seconds"],
        fmt="o",
        capsize=5,
    )
    plt.xlabel("Configuration")
    plt.ylabel("Runtime (s)")
    plt.title("Runtime Mean ± Std Dev")
    plt.tight_layout()
    plt.savefig(errorbar_plot, dpi=150)
    plt.close()

    print(f"Saved runtime plot to: {runtime_plot}")
    print(f"Saved speedup plot to: {speedup_plot}")
    print(f"Saved errorbar plot to: {errorbar_plot}")


if __name__ == "__main__":
    main()
