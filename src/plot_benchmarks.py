from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot benchmark results.")
    parser.add_argument("--input", required=True, help="Benchmark CSV")
    parser.add_argument("--runtime-plot", required=True, help="Output runtime plot")
    parser.add_argument("--speedup-plot", required=True, help="Output speedup plot")
    args = parser.parse_args()

    input_path = Path(args.input)
    runtime_plot = Path(args.runtime_plot)
    speedup_plot = Path(args.speedup_plot)

    runtime_plot.parent.mkdir(parents=True, exist_ok=True)
    speedup_plot.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    # Runtime plot
    plt.figure(figsize=(7, 4))
    x_labels = [f"{row['mode']}-{int(row['workers'])}" for _, row in df.iterrows()]
    plt.bar(x_labels, df["runtime_seconds"])
    plt.xlabel("Configuration")
    plt.ylabel("Runtime (seconds)")
    plt.title("Serial vs Parallel Runtime")
    plt.tight_layout()
    plt.savefig(runtime_plot, dpi=150)
    plt.close()

    # Speedup plot
    parallel_df = df[df["mode"] == "parallel"].copy()

    plt.figure(figsize=(7, 4))
    plt.plot(parallel_df["workers"], parallel_df["speedup_vs_serial"], marker="o")
    plt.xlabel("Workers")
    plt.ylabel("Speedup vs Serial")
    plt.title("Parallel Speedup")
    plt.tight_layout()
    plt.savefig(speedup_plot, dpi=150)
    plt.close()

    print(f"Saved runtime plot to: {runtime_plot}")
    print(f"Saved speedup plot to: {speedup_plot}")


if __name__ == "__main__":
    main()
