from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

from benchmark_pipeline import benchmark_serial, benchmark_parallel, SITES


def main() -> None:
    parser = argparse.ArgumentParser(description="Run repeated serial/parallel benchmarks.")
    parser.add_argument("--output", required=True, help="CSV file for raw repeated timing results")
    parser.add_argument("--repeats", type=int, default=5, help="Number of repeated runs per configuration")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for repeat in range(1, args.repeats + 1):
        serial_time = benchmark_serial(SITES)
        rows.append(
            {
                "mode": "serial",
                "workers": 1,
                "repeat": repeat,
                "n_sites": len(SITES),
                "runtime_seconds": serial_time,
            }
        )

        for workers in [2, 3]:
            parallel_time = benchmark_parallel(SITES, max_workers=workers)
            speedup = serial_time / parallel_time
            efficiency = speedup / workers

            rows.append(
                {
                    "mode": "parallel",
                    "workers": workers,
                    "repeat": repeat,
                    "n_sites": len(SITES),
                    "runtime_seconds": parallel_time,
                    "speedup_vs_serial": speedup,
                    "efficiency": efficiency,
                }
            )

    fieldnames = [
        "mode",
        "workers",
        "repeat",
        "n_sites",
        "runtime_seconds",
        "speedup_vs_serial",
        "efficiency",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if "speedup_vs_serial" not in row:
                row["speedup_vs_serial"] = ""
            if "efficiency" not in row:
                row["efficiency"] = ""
            writer.writerow(row)

    print(f"Saved repeated benchmark raw results to: {output_path}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
