from __future__ import annotations

import argparse
import json
import logging

from src.common.config import load_settings
from src.common.db import connect, init_db
from src.common.logging_utils import configure_logging


LOGGER = logging.getLogger(__name__)


def _cmd_init_db() -> None:
    settings = load_settings()
    configure_logging(settings.log_dir)
    init_db(settings.db_path)
    print(f"Initialized DB at {settings.db_path}")


def _cmd_run_weekly(dry_run: bool, rerun: bool) -> None:
    from src.orchestrator.pipeline import initialize, run_weekly

    settings = load_settings()
    configure_logging(settings.log_dir)
    initialize(settings)
    artifacts = run_weekly(settings, rerun=rerun, dry_run=dry_run)
    print(json.dumps(artifacts.__dict__, indent=2))


def _cmd_list_runs() -> None:
    settings = load_settings()
    init_db(settings.db_path)
    conn = connect(settings.db_path)
    rows = conn.execute(
        "SELECT run_id, status, started_at, ended_at, error_summary FROM runs ORDER BY started_at DESC LIMIT 20"
    ).fetchall()
    conn.close()
    print(json.dumps([dict(r) for r in rows], indent=2))


def _cmd_approve(rec_id: str, status: str) -> None:
    from src.orchestrator.pipeline import set_recommendation_status

    settings = load_settings()
    set_recommendation_status(settings, rec_id, status.upper())
    print(f"Updated {rec_id} to {status.upper()}")


def _cmd_scheduler() -> None:
    from src.orchestrator.scheduler import start_scheduler

    settings = load_settings()
    configure_logging(settings.log_dir)
    start_scheduler(settings)


def _cmd_ui() -> None:
    from ui.app import app

    app.run(host="127.0.0.1", port=8080, debug=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local Performance Intelligence CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db")

    run_p = sub.add_parser("run-weekly")
    run_p.add_argument("--dry-run", action="store_true")
    run_p.add_argument("--rerun", action="store_true")

    sub.add_parser("list-runs")

    approve_p = sub.add_parser("set-rec-status")
    approve_p.add_argument("--rec-id", required=True)
    approve_p.add_argument("--status", required=True, choices=["PROPOSED", "APPROVED", "DEFERRED", "REJECTED"])

    sub.add_parser("start-scheduler")
    sub.add_parser("serve-ui")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init-db":
        _cmd_init_db()
    elif args.command == "run-weekly":
        _cmd_run_weekly(dry_run=args.dry_run, rerun=args.rerun)
    elif args.command == "list-runs":
        _cmd_list_runs()
    elif args.command == "set-rec-status":
        _cmd_approve(args.rec_id, args.status)
    elif args.command == "start-scheduler":
        _cmd_scheduler()
    elif args.command == "serve-ui":
        _cmd_ui()
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
