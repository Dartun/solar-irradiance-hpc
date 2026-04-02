from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Combine multiple feature CSV files.")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input feature CSV files")
    parser.add_argument("--output", required=True, help="Output combined CSV file")
    args = parser.parse_args()

    dfs = []
    for path_str in args.inputs:
        path = Path(path_str)
        df = pd.read_csv(path, parse_dates=["timestamp"])
        dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)
    combined = combined.sort_values(["site", "timestamp"]).reset_index(drop=True)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output_path, index=False)

    print(f"Combined rows: {len(combined)}")
    print(f"Saved to: {output_path}")
    print("Sites:", combined["site"].unique().tolist())


if __name__ == "__main__":
    main()
