#!/usr/bin/env python
"""
Telegram Client

Listens to Telegram Events.
"""
from telethon import TelegramClient, events
from utils import Settings, get_chats, save_activity
from redis import Redis
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = Settings()
CHATS = get_chats(settings)


client = TelegramClient(
    session='sessions/app.session',
    api_id=settings.telegram.api_id,
    api_hash=settings.telegram.api_hash
)
redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)


@client.on(events.userupdate.UserUpdate(chats=CHATS))
async def user_update(event):
    if not isinstance(event.online, bool):
        logger.warning("No event status")
        return
    if not event.user_id:
        logger.error("Event has no user id!")
        return
    if event.online:
        # online user
        # id: event.user_id
        logger.info("{} is online".format(event.user_id))
        redis.set(event.user_id, datetime.timestamp(datetime.now()))
    elif event.last_seen:
        # offline user
        # id: event.user_id
        # last_seen: datetime
        offline_at = datetime.now()
        logger.info("{} is offline".format(event.user_id))
        last_activity = redis.get(event.user_id)
        if not last_activity:
            logger.warning("No activity record for {}".format(event.user_id))
            return
        last_activity = datetime.fromtimestamp(float(last_activity))
        online_duration = (offline_at - last_activity).seconds
        logger.info("{} was active for {} seconds".format(
            event.user_id, online_duration
        ))
        save_activity(
            settings, event.user_id, online_duration, last_activity, offline_at
        )


if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
