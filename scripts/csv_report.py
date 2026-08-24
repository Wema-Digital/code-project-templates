"""Summarise a CSV file: row count and per-column stats, written as a JSON report.

Usage:
    python scripts/csv_report.py --input data.csv
    python scripts/csv_report.py --input data.csv --output report.json
"""

import argparse
import json
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def summarize_csv(path: str) -> dict:
    """Return a JSON-serialisable summary of the CSV at `path`.

    Isolated from the CLI wrapper so it can be tested directly against a
    small fixture file, without going through argparse or stdout.
    """
    df = pd.read_csv(path)

    columns = {}
    for name in df.columns:
        series = df[name]
        column_summary = {"dtype": str(series.dtype), "non_null": int(series.count())}
        if pd.api.types.is_numeric_dtype(series):
            column_summary["mean"] = float(series.mean())
            column_summary["min"] = float(series.min())
            column_summary["max"] = float(series.max())
        columns[name] = column_summary

    return {"rows": len(df), "columns": columns}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv_report", description="Summarise a CSV file as a JSON report"
    )
    parser.add_argument("--input", required=True, help="Path to the CSV file to summarise")
    parser.add_argument("--output", help="Path to write the JSON report (default: stdout)")
    return parser


def main(argv=None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = build_parser().parse_args(argv)

    logger.info("Summarising %s", args.input)
    summary = summarize_csv(args.input)

    output = json.dumps(summary, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        logger.info("Wrote report to %s", args.output)
    else:
        print(output)


if __name__ == "__main__":
    main()
