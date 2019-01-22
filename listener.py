#!/usr/bin/env python
"""
Telegram Client

Listens to Telegram Events.
"""
from telethon import TelegramClient, events
from utils import Settings, get_chats
import logging


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
settings = Settings()
CHATS = []


client = TelegramClient(
    session='sessions/app.session',
    api_id=settings.telegram.api_id,
    api_hash=settings.telegram.api_hash
)


@client.on(events.userupdate.UserUpdate(chats=CHATS))
def user_update(event):
    if not isinstance(event.online, bool):
        # no status info
        return
    if event.online:
        # online user
        # id: event.chat.id
        pass
    elif event.last_seen:
        # offline user
        # id: event.chat.id
        # last_seen: datetime
        pass


if __name__ == '__main__':
    CHATS = get_chats(settings)
    client.start()
    client.run_until_disconnected()
