from __future__ import annotations

import argparse
import csv
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


SITES = ["dallas", "phoenix", "seattle"]


def run_site_pipeline(site: str) -> None:
    raw_input = f"data/raw/nasa_power/{site}_20240101_20240331_power.csv"
    processed_output = f"data/processed/{site}_202401_202403_processed.csv"
    feature_output = f"data/processed/{site}_202401_202403_features.csv"
    plot_output = f"results/figures/{site}_202401_202403_ghi.png"

    subprocess.run(
        [
            "python",
            "src/preprocess.py",
            "--site",
            site,
            "--input",
            raw_input,
            "--output",
            processed_output,
            "--plot",
            plot_output,
        ],
        check=True,
    )

    subprocess.run(
        [
            "python",
            "src/features.py",
            "--input",
            processed_output,
            "--output",
            feature_output,
        ],
        check=True,
    )


def benchmark_serial(sites: list[str]) -> float:
    start = time.perf_counter()
    for site in sites:
        run_site_pipeline(site)
    end = time.perf_counter()
    return end - start


def benchmark_parallel(sites: list[str], max_workers: int) -> float:
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        list(executor.map(run_site_pipeline, sites))
    end = time.perf_counter()
    return end - start


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark serial vs parallel site processing.")
    parser.add_argument("--output", required=True, help="CSV file for timing results")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results = []

    serial_time = benchmark_serial(SITES)
    results.append(
        {
            "mode": "serial",
            "workers": 1,
            "n_sites": len(SITES),
            "runtime_seconds": serial_time,
        }
    )

    for workers in [2, 3]:
        parallel_time = benchmark_parallel(SITES, max_workers=workers)
        speedup = serial_time / parallel_time
        efficiency = speedup / workers

        results.append(
            {
                "mode": "parallel",
                "workers": workers,
                "n_sites": len(SITES),
                "runtime_seconds": parallel_time,
                "speedup_vs_serial": speedup,
                "efficiency": efficiency,
            }
        )

    fieldnames = [
        "mode",
        "workers",
        "n_sites",
        "runtime_seconds",
        "speedup_vs_serial",
        "efficiency",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            if "speedup_vs_serial" not in row:
                row["speedup_vs_serial"] = ""
            if "efficiency" not in row:
                row["efficiency"] = ""
            writer.writerow(row)

    print(f"Saved benchmark results to: {output_path}")
    for row in results:
        print(row)


if __name__ == "__main__":
    main()
