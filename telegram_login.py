#!/usr/bin/env python
"""
Telegram Login

Create Telegram Session for app.
"""
from telethon import TelegramClient, sync
from utils import Settings


settings = Settings()

with TelegramClient(
            session='sessions/app.session',
            api_id=settings.telegram.api_id,
            api_hash=settings.telegram.api_hash
        ) as client:
    client.start()
