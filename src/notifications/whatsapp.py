from __future__ import annotations

from src.common.config import Settings


def send_whatsapp_summary(settings: Settings, body: str) -> str:
    if settings.whatsapp_provider != "twilio":
        return "skipped: unsupported provider"
    if not all([settings.whatsapp_account_sid, settings.whatsapp_auth_token, settings.whatsapp_from, settings.whatsapp_to]):
        return "skipped: whatsapp settings not configured"

    from twilio.rest import Client

    client = Client(settings.whatsapp_account_sid, settings.whatsapp_auth_token)
    client.messages.create(from_=settings.whatsapp_from, to=settings.whatsapp_to, body=body)
    return "sent"
