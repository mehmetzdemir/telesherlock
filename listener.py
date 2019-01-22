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
CHATS = get_chats(settings)


client = TelegramClient(
    session='sessions/app.session',
    api_id=settings.telegram.api_id,
    api_hash=settings.telegram.api_hash
)


@client.on(events.userupdate.UserUpdate(chats=CHATS))
async def user_update(event):
    if not isinstance(event.online, bool):
        # no status info
        return
    if event.online:
        # online user
        # id: event.user_id
        logger.info("{} is online".format(event.user_id))
    elif event.last_seen:
        # offline user
        # id: event.user_id
        # last_seen: datetime
        logger.info("{} is offline".format(event.user_id))


if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
