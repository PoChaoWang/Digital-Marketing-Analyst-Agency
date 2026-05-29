#!/usr/bin/env python3

import argparse
import csv
import datetime as dt
import os
import sqlite3
from pathlib import Path


REPO_ROOT = Path.cwd()
DEFAULT_SQL = "sql/build_360_table.sql"
DEFAULT_OUT = "exports/360_table.csv"

OUTPUT_COLUMNS = [
    "date",
    "source",
    "platform",
    "campaign_name",
    "ad_group_name",
    "ad_name",
    "impressions",
    "clicks",
    "spend",
    "conversions",
    "revenue",
    "ga4_users",
    "ga4_new_users",
    "ga4_conversions",
    "ga4_revenue",
    "source_type",
    "platform_name",
    "source_file",
    "source_priority",
    "loaded_at",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Combine paid media and GA4 CSV exports into exports/360_table.csv using SQL."
    )
    parser.add_argument("--google-ads-csv", action="append", default=[], help="Google Ads CSV export.")
    parser.add_argument("--meta-ads-csv", action="append", default=[], help="Meta Ads CSV export.")
    parser.add_argument("--ga4-csv", action="append", default=[], help="GA4 CSV export.")
    parser.add_argument("--google-ads-mcp", action="append", default=[], help="Google Ads MCP-staged CSV.")
    parser.add_argument("--meta-ads-mcp", action="append", default=[], help="Meta Ads MCP-staged CSV.")
    parser.add_argument("--ga4-mcp", action="append", default=[], help="GA4 MCP-staged CSV.")
    parser.add_argument("--priority-overrides", help="Optional simple YAML file with priority_overrides.")
    parser.add_argument("--sql", default=DEFAULT_SQL, help="SQL file to build the 360 table.")
    parser.add_argument("--out", default=DEFAULT_OUT, help="Output CSV path.")
    return parser.parse_args()


def first_value(row, names, default=""):
    for name in names:
        if name in row and row[name] not in (None, ""):
            return row[name]
    return default


def number(value):
    if value in (None, ""):
        return 0
    return float(str(value).replace(",", ""))


def normalized_paid_rows(path, platform, source_type, platform_name, loaded_at):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield {
                "date": first_value(row, ["date", "day"]),
                "platform": first_value(row, ["platform"], platform),
                "campaign_name": first_value(row, ["campaign_name", "campaign", "utm_campaign"], "unknown"),
                "ad_group_name": first_value(row, ["ad_group_name", "ad_group", "ad_set", "adset_name", "utm_id"], "unknown"),
                "ad_name": first_value(row, ["ad_name", "creative_name", "creative", "utm_content"], "unknown"),
                "impressions": number(first_value(row, ["impressions"], 0)),
                "clicks": number(first_value(row, ["clicks"], 0)),
                "spend": number(first_value(row, ["spend", "cost"], 0)),
                "conversions": number(first_value(row, ["conversions", "orders"], 0)),
                "revenue": number(first_value(row, ["revenue", "conversion_value", "purchase_value"], 0)),
                "source_type": source_type,
                "platform_name": platform_name,
                "source_file": path if source_type == "csv" else "",
                "loaded_at": loaded_at,
            }


def normalized_ga4_rows(path, source_type, platform_name, loaded_at):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield {
                "date": first_value(row, ["date", "day"]),
                "source": first_value(row, ["source"], ""),
                "platform_source": first_value(row, ["platform_source"], ""),
                "campaign": first_value(row, ["campaign"], ""),
                "utm_source": first_value(row, ["utm_source"], ""),
                "utm_campaign": first_value(row, ["utm_campaign"], ""),
                "utm_id": first_value(row, ["utm_id"], ""),
                "utm_content": first_value(row, ["utm_content"], ""),
                "users": number(first_value(row, ["users"], 0)),
                "new_users": number(first_value(row, ["new_users", "new users", "newUsers"], 0)),
                "conversions": number(first_value(row, ["conversions", "key_events", "key events"], 0)),
                "revenue": number(first_value(row, ["revenue", "purchase_revenue"], 0)),
                "source_type": source_type,
                "platform_name": platform_name,
                "source_file": path if source_type == "csv" else "",
                "loaded_at": loaded_at,
            }


def parse_priority_overrides(path):
    if not path:
        return []
    rows = []
    current = {}
    with open(path, encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or line == "priority_overrides:":
                continue
            if line.startswith("- "):
                if current:
                    rows.append(current)
                current = {}
                line = line[2:].strip()
                if ":" in line:
                    key, value = line.split(":", 1)
                    current[key.strip()] = value.strip().strip('"')
            elif ":" in line and current is not None:
                key, value = line.split(":", 1)
                current[key.strip()] = value.strip().strip('"')
    if current:
        rows.append(current)
    return [
        {
            "date": item.get("date", ""),
            "platform": item.get("platform", ""),
            "prefer": item.get("prefer", ""),
            "reason": item.get("reason", ""),
        }
        for item in rows
        if item.get("date") and item.get("platform") and item.get("prefer")
    ]


def create_tables(connection):
    connection.executescript(
        """
        CREATE TABLE paid_raw (
          date TEXT,
          platform TEXT,
          campaign_name TEXT,
          ad_group_name TEXT,
          ad_name TEXT,
          impressions REAL,
          clicks REAL,
          spend REAL,
          conversions REAL,
          revenue REAL,
          source_type TEXT,
          platform_name TEXT,
          source_file TEXT,
          loaded_at TEXT
        );

        CREATE TABLE ga4_raw (
          date TEXT,
          source TEXT,
          platform_source TEXT,
          campaign TEXT,
          utm_source TEXT,
          utm_campaign TEXT,
          utm_id TEXT,
          utm_content TEXT,
          users REAL,
          new_users REAL,
          conversions REAL,
          revenue REAL,
          source_type TEXT,
          platform_name TEXT,
          source_file TEXT,
          loaded_at TEXT
        );

        CREATE TABLE priority_overrides (
          date TEXT,
          platform TEXT,
          prefer TEXT,
          reason TEXT
        );
        """
    )


def insert_rows(connection, table, rows):
    rows = list(rows)
    if not rows:
        return
    columns = list(rows[0].keys())
    placeholders = ", ".join(["?"] * len(columns))
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    connection.executemany(sql, [[row[column] for column in columns] for row in rows])


def write_output(connection, out_path):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    cursor = connection.execute(f"SELECT {', '.join(OUTPUT_COLUMNS)} FROM table_360")
    with open(out_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(OUTPUT_COLUMNS)
        writer.writerows(cursor.fetchall())


def main():
    args = parse_args()
    loaded_at = dt.datetime.now(dt.timezone.utc).isoformat()
    connection = sqlite3.connect(":memory:")
    create_tables(connection)

    for path in args.google_ads_csv:
        insert_rows(
            connection,
            "paid_raw",
            normalized_paid_rows(path, "google_ads", "csv", "manual_csv_fallback", loaded_at),
        )
    for path in args.meta_ads_csv:
        insert_rows(
            connection,
            "paid_raw",
            normalized_paid_rows(path, "meta_ads", "csv", "manual_csv_fallback", loaded_at),
        )
    for path in args.google_ads_mcp:
        insert_rows(
            connection,
            "paid_raw",
            normalized_paid_rows(path, "google_ads", "mcp", "google_ads_mcp_production", loaded_at),
        )
    for path in args.meta_ads_mcp:
        insert_rows(
            connection,
            "paid_raw",
            normalized_paid_rows(path, "meta_ads", "mcp", "meta_ads_mcp_production", loaded_at),
        )
    for path in args.ga4_csv:
        insert_rows(connection, "ga4_raw", normalized_ga4_rows(path, "csv", "manual_csv_fallback", loaded_at))
    for path in args.ga4_mcp:
        insert_rows(connection, "ga4_raw", normalized_ga4_rows(path, "mcp", "ga4_mcp_production", loaded_at))

    insert_rows(connection, "priority_overrides", parse_priority_overrides(args.priority_overrides))

    with open(args.sql, encoding="utf-8") as handle:
        connection.executescript(handle.read())

    write_output(connection, args.out)
    count = connection.execute("SELECT COUNT(*) FROM table_360").fetchone()[0]
    print(f"Wrote {count} rows to {args.out}")


if __name__ == "__main__":
    main()
