from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


def to_float(value: str) -> float:
    if value is None:
        return 0.0
    cleaned = str(value).replace(",", "").replace("%", "").strip()
    if not cleaned:
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def compute_kpi_summary(normalized_csv: Path, group_by: str = "campaign_name") -> dict[str, object]:
    aggregates: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    totals: dict[str, float] = defaultdict(float)
    row_count = 0

    with normalized_csv.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            row_count += 1
            entity = row.get(group_by) or "(unlabeled)"
            spend = to_float(row.get("spend", "0"))
            impressions = to_float(row.get("impressions", "0"))
            clicks = to_float(row.get("clicks", row.get("link_clicks", "0")))
            conversions = to_float(row.get("actions.purchase", row.get("actions.lead", "0")))
            conv_value = to_float(row.get("action_values.purchase", "0"))

            bucket = aggregates[entity]
            bucket["spend"] += spend
            bucket["impressions"] += impressions
            bucket["clicks"] += clicks
            bucket["conversions"] += conversions
            bucket["conversion_value"] += conv_value

            totals["spend"] += spend
            totals["impressions"] += impressions
            totals["clicks"] += clicks
            totals["conversions"] += conversions
            totals["conversion_value"] += conv_value

    def enrich(metrics: dict[str, float]) -> dict[str, float]:
        m = dict(metrics)
        m["ctr"] = (m["clicks"] / m["impressions"] * 100) if m.get("impressions") else 0.0
        m["cpc"] = (m["spend"] / m["clicks"]) if m.get("clicks") else 0.0
        m["cpm"] = (m["spend"] * 1000 / m["impressions"]) if m.get("impressions") else 0.0
        m["cpa"] = (m["spend"] / m["conversions"]) if m.get("conversions") else 0.0
        m["cvr"] = (m["conversions"] / m["clicks"] * 100) if m.get("clicks") else 0.0
        return m

    ranked_entities = []
    for entity, metrics in aggregates.items():
        enriched = enrich(metrics)
        enriched["entity"] = entity
        ranked_entities.append(enriched)

    ranked_entities.sort(key=lambda x: x.get("spend", 0.0), reverse=True)

    return {
        "row_count": row_count,
        "totals": enrich(totals),
        "entities": ranked_entities,
        "top": ranked_entities[:5],
        "bottom": sorted(ranked_entities, key=lambda x: x.get("cpa", 0.0), reverse=True)[:5],
    }
