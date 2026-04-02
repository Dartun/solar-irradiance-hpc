#!/bin/bash
set -e

START=20240101
END=20240331
OUTDIR=data/raw/nasa_power

python src/download_power.py --site dallas  --start $START --end $END --output-dir $OUTDIR
python src/download_power.py --site phoenix --start $START --end $END --output-dir $OUTDIR
python src/download_power.py --site seattle --start $START --end $END --output-dir $OUTDIR
