from __future__ import annotations

import csv
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

LOGGER = logging.getLogger(__name__)


@dataclass
class PullConfig:
    account_id: str
    access_token: str
    api_version: str
    level: str
    fields: str
    date_preset: Optional[str] = "last_7d"
    since: Optional[str] = None
    until: Optional[str] = None
    time_increment: Optional[str] = None
    breakdowns: Optional[str] = None
    limit: int = 250


def _flatten_metric_list(row: dict[str, object], key: str) -> dict[str, str]:
    values: dict[str, str] = {}
    items = row.get(key)
    if not isinstance(items, list):
        return values
    for item in items:
        if not isinstance(item, dict):
            continue
        action_type = item.get("action_type")
        value = item.get("value")
        if action_type and value not in (None, ""):
            values[f"{key}.{action_type}"] = str(value)
    return values


def flatten_row(row: dict[str, object]) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in row.items():
        if key in {"actions", "action_values"}:
            out.update(_flatten_metric_list(row, key))
            continue
        if isinstance(value, (dict, list)):
            out[key] = json.dumps(value, sort_keys=True)
        elif value is None:
            out[key] = ""
        else:
            out[key] = str(value)
    return out


def _build_params(config: PullConfig, after: Optional[str] = None) -> dict[str, str]:
    params = {
        "access_token": config.access_token,
        "fields": config.fields,
        "level": config.level,
        "limit": str(config.limit),
    }
    if config.date_preset:
        params["date_preset"] = config.date_preset
    if config.since and config.until:
        params["time_range"] = json.dumps({"since": config.since, "until": config.until})
    if config.time_increment:
        params["time_increment"] = config.time_increment
    if config.breakdowns:
        params["breakdowns"] = config.breakdowns
    if after:
        params["after"] = after
    return params


def pull_insights(config: PullConfig, max_retries: int = 3) -> list[dict[str, str]]:
    import requests

    base_url = f"https://graph.facebook.com/{config.api_version}/{config.account_id}/insights"
    rows: list[dict[str, str]] = []
    after: Optional[str] = None

    while True:
        params = _build_params(config, after)
        response = None
        for attempt in range(max_retries):
            response = requests.get(base_url, params=params, timeout=60)
            if response.status_code < 500:
                break
            time.sleep(2 ** attempt)

        if response is None:
            raise RuntimeError("No response from Meta API")

        payload = response.json()
        if response.status_code >= 400:
            raise RuntimeError(f"Meta API error {response.status_code}: {payload}")

        data = payload.get("data", [])
        if not isinstance(data, list):
            raise RuntimeError("Unexpected data payload from Meta API")

        rows.extend(flatten_row(item) for item in data if isinstance(item, dict))

        paging = payload.get("paging", {})
        cursors = paging.get("cursors", {}) if isinstance(paging, dict) else {}
        after = cursors.get("after") if isinstance(cursors, dict) else None
        if not after:
            break

    LOGGER.info("Pulled %s rows for level=%s", len(rows), config.level)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
