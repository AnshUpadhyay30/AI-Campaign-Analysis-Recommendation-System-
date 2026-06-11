from __future__ import annotations

import csv
from pathlib import Path


HEADER_ALIASES = {
    "campaign name": "campaign_name",
    "ad set name": "adset_name",
    "ad name": "ad_name",
    "amount spent": "spend",
    "ctr (all)": "ctr",
    "cpc (all)": "cpc",
    "cpm (cost per 1,000 impressions)": "cpm",
    "link clicks": "link_clicks",
}


def normalize_header(name: str) -> str:
    key = " ".join(name.strip().lower().replace("_", " ").split())
    return HEADER_ALIASES.get(key, key.replace(" ", "_"))


def normalize_csv(input_csvs: list[Path], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    headers: list[str] = []
    seen = set()

    for csv_path in input_csvs:
        if not csv_path.exists():
            continue
        with csv_path.open("r", newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                normalized = {normalize_header(k): (v or "") for k, v in row.items() if k}
                rows.append(normalized)
                for key in normalized:
                    if key not in seen:
                        seen.add(key)
                        headers.append(key)

    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return output_path
