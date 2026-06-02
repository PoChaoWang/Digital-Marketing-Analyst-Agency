#!/usr/bin/env python3

import argparse
import datetime as dt
import sys
from pathlib import Path
import duckdb


REPO_ROOT = Path.cwd()
DEFAULT_SQL = "sql/build_360_table.sql"
DEFAULT_OUT = "exports/360_table.csv"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Combine paid media and GA4 CSV exports into exports/360_table.csv using DuckDB."
    )
    # 這裡保留參數是為了相容性
    parser.add_argument("--google-ads-csv", action="append", default=[], help="Google Ads CSV export.")
    parser.add_argument("--meta-ads-csv", action="append", default=[], help="Meta Ads CSV export.")
    parser.add_argument("--ga4-csv", action="append", default=[], help="GA4 CSV export.")
    parser.add_argument("--sql", default=DEFAULT_SQL, help="SQL file to build the 360 table.")
    parser.add_argument("--out", default=DEFAULT_OUT, help="Output CSV path.")
    return parser.parse_args()


def main():
    args = parse_args()

    # 確認原始資料路徑
    google_ads_path = args.google_ads_csv[0] if args.google_ads_csv else "data/google_ads_raw.csv"
    meta_ads_path = args.meta_ads_csv[0] if args.meta_ads_csv else "data/meta_ads_raw.csv"
    ga4_path = args.ga4_csv[0] if args.ga4_csv else "data/ga4_raw.csv"

    # 檢查必要檔案是否存在
    missing_files = []
    for label, path in [
        ("Google Ads CSV", google_ads_path),
        ("Meta Ads CSV", meta_ads_path),
        ("GA4 CSV", ga4_path),
        ("SQL Script", args.sql)
    ]:
        if not Path(path).exists():
            missing_files.append(f"- {label}: {path}")

    if missing_files:
        print("Error: Missing required files for aggregation:")
        print("\n".join(missing_files))
        print("\nBecause MCP connections are not yet configured, please ensure the raw CSV files exist in the 'data/' directory.")
        sys.exit(1)

    con = duckdb.connect(database=":memory:")
    print(f"Using DuckDB to process data...")

    try:
        # 註冊為 View
        con.execute(f"CREATE VIEW google_ads_raw AS SELECT * FROM read_csv_auto('{google_ads_path}')")
        con.execute(f"CREATE VIEW meta_ads_raw AS SELECT * FROM read_csv_auto('{meta_ads_path}')")
        con.execute(f"CREATE VIEW ga4_raw AS SELECT * FROM read_csv_auto('{ga4_path}')")

        # 執行 SQL 轉換邏輯
        with open(args.sql, encoding="utf-8") as f:
            sql_script = f.read()
            con.execute(sql_script)

        # 匯出結果到 CSV
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        con.execute(f"COPY (SELECT * FROM table_360) TO '{args.out}' (HEADER, DELIMITER ',')")

        count = con.execute("SELECT COUNT(*) FROM table_360").fetchone()[0]
        print(f"Successfully wrote {count} rows to {args.out}")
    except Exception as e:
        print(f"Error during DuckDB processing: {e}")
        sys.exit(1)



if __name__ == "__main__":
    main()
