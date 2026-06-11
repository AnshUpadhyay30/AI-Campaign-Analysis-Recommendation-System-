from __future__ import annotations

from flask import Flask, jsonify, request

from src.common.config import load_settings
from src.common.db import connect
from src.orchestrator.pipeline import set_recommendation_status

app = Flask(__name__)
settings = load_settings()


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "performance-intelligence-ui"}


@app.get("/runs")
def list_runs() -> object:
    conn = connect(settings.db_path)
    rows = conn.execute("SELECT run_id, status, started_at, ended_at, error_summary FROM runs ORDER BY started_at DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.get("/recommendations")
def list_recommendations() -> object:
    run_id = request.args.get("run_id", "")
    conn = connect(settings.db_path)
    if run_id:
        rows = conn.execute(
            "SELECT rec_id, run_id, scope_id, action, rationale, confidence, status FROM recommendations WHERE run_id=? ORDER BY confidence DESC",
            (run_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT rec_id, run_id, scope_id, action, rationale, confidence, status FROM recommendations ORDER BY rowid DESC LIMIT 200"
        ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.post("/recommendations/<rec_id>/status")
def update_recommendation(rec_id: str) -> object:
    payload = request.get_json(force=True, silent=True) or {}
    status = str(payload.get("status", "")).upper()
    set_recommendation_status(settings, rec_id, status)
    return jsonify({"rec_id": rec_id, "status": status})


if __name__ == "__main__":
    app.run(port=8080, debug=False)
