#!/usr/bin/env python3
"""
將 360 Table CSV 寫入 Google Sheets 指定 tab。
由 AI Agent 調度執行，不直接與 combine_to_360_table.py 耦合。
"""

import argparse
import csv
import yaml
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

import gspread
from google.oauth2.service_account import Credentials

# 載入 .env 檔案
load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Push 360 Table CSV to Google Sheets.")
    parser.add_argument(
        "--config",
        default="config/sheets-output.yml",
        help="YAML config specifying target sheet and tabs.",
    )
    parser.add_argument(
        "--csv",
        default="exports/360_table.csv",
        help="Path to 360 table CSV.",
    )
    parser.add_argument(
        "--credentials",
        default=os.getenv("GCP_SERVICE_ACCOUNT_FILE", "config/gcp-credentials.json"),
        help="GCP service account JSON path (defaults to GCP_SERVICE_ACCOUNT_FILE env var).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be written without actually writing.",
    )
    return parser.parse_args()


def load_config(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)


def get_or_create_tab(spreadsheet, tab_name):
    try:
        return spreadsheet.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=tab_name, rows=1000, cols=30)


def push(config, csv_path, credentials_path, dry_run):
    path_obj = Path(csv_path)
    
    # 檢查 CSV 檔案是否存在
    if not path_obj.exists():
        print(f"Error: CSV file not found at {csv_path}")
        print("Please ensure the data is generated before running this script.")
        sys.exit(1)

    rows = read_csv(csv_path)
    if not rows:
        print("CSV is empty, nothing to push.")
        return

    tab_config = config["output"]["tabs"]["raw_data"]
    spreadsheet_id = config["output"]["spreadsheet_id"]
    tab_name = tab_config["name"]

    print(f"Target: {spreadsheet_id} → tab '{tab_name}'")
    print(f"Rows to write: {len(rows)} (including header)")

    if dry_run:
        print("[dry-run] No data written.")
        return

    creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = get_or_create_tab(spreadsheet, tab_name)

    if tab_config.get("overwrite", True):
        worksheet.clear()

    # Batch writing to handle large datasets
    chunk_size = 10000
    for i in range(0, len(rows), chunk_size):
        chunk = rows[i : i + chunk_size]
        range_label = f"A{i + 1}"
        worksheet.update(range_label, chunk)
        print(f"  - Written rows {i + 1} to {i + len(chunk)}")
        if i + chunk_size < len(rows):
            time.sleep(1)

    if tab_config.get("freeze_header", True):
        spreadsheet.batch_update(
            {
                "requests": [
                    {
                        "updateSheetProperties": {
                            "properties": {
                                "sheetId": worksheet.id,
                                "gridProperties": {"frozenRowCount": 1},
                            },
                            "fields": "gridProperties.frozenRowCount",
                        }
                    }
                ]
            }
        )

    print(f"Done. {len(rows) - 1} data rows written to '{tab_name}'.")


def main():
    args = parse_args()
    config = load_config(args.config)
    push(config, args.csv, args.credentials, args.dry_run)


if __name__ == "__main__":
    main()
