from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency fallback
    def load_dotenv() -> None:
        return None


@dataclass(frozen=True)
class Settings:
    meta_access_token: str
    meta_ad_account_id: str
    meta_api_version: str
    anthropic_api_key: str
    claude_model: str
    llm_max_tokens: int
    llm_temperature: float
    db_path: Path
    vector_db_path: Path
    report_output_dir: Path
    log_dir: Path
    timezone: str
    weekly_cron: str
    email_smtp_host: str
    email_smtp_port: int
    email_smtp_username: str
    email_smtp_password: str
    email_from: str
    email_to: str
    whatsapp_provider: str
    whatsapp_account_sid: str
    whatsapp_auth_token: str
    whatsapp_from: str
    whatsapp_to: str


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        meta_access_token=os.getenv("META_ACCESS_TOKEN", ""),
        meta_ad_account_id=os.getenv("META_AD_ACCOUNT_ID", ""),
        meta_api_version=os.getenv("META_API_VERSION", "v23.0"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        claude_model=os.getenv("CLAUDE_MODEL", "claude-3-7-sonnet-latest"),
        llm_max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1600")),
        llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
        db_path=Path(os.getenv("DB_PATH", "data/db/perf_marketing.sqlite3")),
        vector_db_path=Path(os.getenv("VECTOR_DB_PATH", "data/vector/chroma")),
        report_output_dir=Path(os.getenv("REPORT_OUTPUT_DIR", "output/reports")),
        log_dir=Path(os.getenv("LOG_DIR", "logs")),
        timezone=os.getenv("TIMEZONE", "Asia/Kolkata"),
        weekly_cron=os.getenv("WEEKLY_CRON", "0 8 * * MON"),
        email_smtp_host=os.getenv("EMAIL_SMTP_HOST", ""),
        email_smtp_port=int(os.getenv("EMAIL_SMTP_PORT", "587")),
        email_smtp_username=os.getenv("EMAIL_SMTP_USERNAME", ""),
        email_smtp_password=os.getenv("EMAIL_SMTP_PASSWORD", ""),
        email_from=os.getenv("EMAIL_FROM", ""),
        email_to=os.getenv("EMAIL_TO", ""),
        whatsapp_provider=os.getenv("WHATSAPP_PROVIDER", "twilio"),
        whatsapp_account_sid=os.getenv("WHATSAPP_ACCOUNT_SID", ""),
        whatsapp_auth_token=os.getenv("WHATSAPP_AUTH_TOKEN", ""),
        whatsapp_from=os.getenv("WHATSAPP_FROM", ""),
        whatsapp_to=os.getenv("WHATSAPP_TO", ""),
    )
