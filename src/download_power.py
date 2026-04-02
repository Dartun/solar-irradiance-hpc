from __future__ import annotations

import argparse
from pathlib import Path
import requests


SITE_COORDS = {
    "dallas": (32.7767, -96.7970),
    "phoenix": (33.4484, -112.0740),
    "seattle": (47.6062, -122.3321),
}


PARAMETERS = "ALLSKY_SFC_SW_DWN,T2M,RH2M,WS2M,PS"


def build_power_url(site: str, start: str, end: str) -> str:
    lat, lon = SITE_COORDS[site]
    url = (
        "https://power.larc.nasa.gov/api/temporal/hourly/point"
        f"?parameters={PARAMETERS}"
        f"&community=RE"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&start={start}"
        f"&end={end}"
        f"&format=CSV"
        f"&time-standard=UTC"
    )
    return url


def download_power_data(site: str, start: str, end: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    url = build_power_url(site, start, end)
    output_file = output_dir / f"{site}_{start}_{end}_power.csv"

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    output_file.write_bytes(response.content)
    return output_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Download NASA POWER hourly data for a site.")
    parser.add_argument("--site", required=True, choices=SITE_COORDS.keys())
    parser.add_argument("--start", required=True, help="Start date YYYYMMDD")
    parser.add_argument("--end", required=True, help="End date YYYYMMDD")
    parser.add_argument("--output-dir", required=True, help="Directory for downloaded file")
    args = parser.parse_args()

    output_path = download_power_data(
        site=args.site,
        start=args.start,
        end=args.end,
        output_dir=Path(args.output_dir),
    )

    print(f"Downloaded file: {output_path}")


if __name__ == "__main__":
    main()
