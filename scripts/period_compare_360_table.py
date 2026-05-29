#!/usr/bin/env python3

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Compare two periods using exports/360_table.csv.")
    parser.add_argument("--input", default="exports/360_table.csv", help="360 table CSV path.")
    parser.add_argument("--current-start", required=True, help="Current period start date, inclusive.")
    parser.add_argument("--current-end", required=True, help="Current period end date, inclusive.")
    parser.add_argument("--previous-start", required=True, help="Previous period start date, inclusive.")
    parser.add_argument("--previous-end", required=True, help="Previous period end date, inclusive.")
    parser.add_argument("--out", help="Optional JSON output path.")
    return parser.parse_args()


def number(value):
    if value in (None, ""):
        return 0
    return float(str(value).replace(",", ""))


def ratio(numerator, denominator):
    return None if denominator == 0 else numerator / denominator


def rounded(value, digits=6):
    if value is None:
        return None
    return round(value, digits)


def percent_change(current, previous):
    if current is None or previous is None:
        return None
    if previous == 0:
        return None
    return rounded((current - previous) / previous)


def empty_totals():
    return {
        "impressions": 0,
        "clicks": 0,
        "spend": 0,
        "platform_conversions": 0,
        "platform_revenue": 0,
        "ga4_users": 0,
        "ga4_new_users": 0,
        "ga4_conversions": 0,
        "ga4_revenue": 0,
    }


def add_row(totals, row):
    totals["impressions"] += number(row.get("impressions"))
    totals["clicks"] += number(row.get("clicks"))
    totals["spend"] += number(row.get("spend"))
    totals["platform_conversions"] += number(row.get("conversions"))
    totals["platform_revenue"] += number(row.get("revenue"))
    totals["ga4_users"] += number(row.get("ga4_users"))
    totals["ga4_new_users"] += number(row.get("ga4_new_users"))
    totals["ga4_conversions"] += number(row.get("ga4_conversions"))
    totals["ga4_revenue"] += number(row.get("ga4_revenue"))


def metrics(totals):
    return {
        "ctr": rounded(ratio(totals["clicks"], totals["impressions"])),
        "cpc": rounded(ratio(totals["spend"], totals["clicks"]), 2),
        "cpm": rounded(ratio(totals["spend"] * 1000, totals["impressions"]), 2),
        "cvr": rounded(ratio(totals["ga4_conversions"], totals["clicks"])),
        "cpa": rounded(ratio(totals["spend"], totals["ga4_conversions"]), 2),
        "roas": rounded(ratio(totals["ga4_revenue"], totals["spend"]), 4),
        "roi": rounded(ratio(totals["ga4_revenue"] - totals["spend"], totals["spend"]), 4),
    }


def compare_dicts(current, previous):
    return {key: percent_change(current[key], previous[key]) for key in current.keys()}


def period_rows(rows, start, end):
    return [row for row in rows if start <= row["date"] <= end]


def summarize(rows):
    total = empty_totals()
    by_platform = defaultdict(empty_totals)
    by_campaign = defaultdict(empty_totals)
    source_mix = defaultdict(int)

    for row in rows:
        add_row(total, row)
        add_row(by_platform[row.get("platform", "unknown")], row)
        add_row(by_campaign[(row.get("platform", "unknown"), row.get("campaign_name", "unknown"))], row)
        source_mix[row.get("source_type", "unknown")] += 1

    campaign_summaries = []
    for (platform, campaign_name), totals in by_campaign.items():
        campaign_summaries.append(
            {
                "platform": platform,
                "campaign_name": campaign_name,
                "totals": totals,
                "metrics": metrics(totals),
            }
        )
    campaign_summaries.sort(key=lambda item: item["totals"]["spend"], reverse=True)

    return {
        "row_count": len(rows),
        "source_mix": dict(source_mix),
        "totals": total,
        "metrics": metrics(total),
        "platforms": {
            platform: {
                "totals": totals,
                "metrics": metrics(totals),
            }
            for platform, totals in by_platform.items()
        },
        "top_campaigns_by_spend": campaign_summaries[:10],
    }


def main():
    args = parse_args()
    with open(args.input, newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    current_rows = period_rows(rows, args.current_start, args.current_end)
    previous_rows = period_rows(rows, args.previous_start, args.previous_end)
    current = summarize(current_rows)
    previous = summarize(previous_rows)

    result = {
        "input": args.input,
        "metric_policy": "CVR, CPA, ROAS, ROI, conversion, and revenue calculations use GA4 fields.",
        "current_period": {
            "start_date": args.current_start,
            "end_date": args.current_end,
            **current,
        },
        "previous_period": {
            "start_date": args.previous_start,
            "end_date": args.previous_end,
            **previous,
        },
        "comparison": {
            "totals_change": compare_dicts(current["totals"], previous["totals"]),
            "metrics_change": compare_dicts(current["metrics"], previous["metrics"]),
        },
        "data_gaps": [],
    }

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
