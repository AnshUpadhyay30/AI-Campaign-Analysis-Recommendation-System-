from __future__ import annotations

import smtplib
from email.message import EmailMessage
from pathlib import Path

from src.common.config import Settings


def send_weekly_email(settings: Settings, subject: str, body: str, attachment_paths: list[Path]) -> str:
    if not all([settings.email_smtp_host, settings.email_from, settings.email_to]):
        return "skipped: email settings not configured"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.email_from
    msg["To"] = settings.email_to
    msg.set_content(body)

    for path in attachment_paths:
        if not path.exists():
            continue
        data = path.read_bytes()
        msg.add_attachment(data, maintype="text", subtype="plain", filename=path.name)

    with smtplib.SMTP(settings.email_smtp_host, settings.email_smtp_port) as server:
        server.starttls()
        if settings.email_smtp_username:
            server.login(settings.email_smtp_username, settings.email_smtp_password)
        server.send_message(msg)

    return "sent"
