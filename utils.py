import json
import psycopg2
from random import randint
from datetime import datetime, timedelta
from typing import List
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(object):
    """Parse settings file."""
    def __init__(self, filename='credentials.json', data=None):
        if data:
            self.settings = data
        else:
            with open(filename, 'r') as session_file:
                self.settings = json.load(session_file)

    def __getattr__(self, name: str):
        if isinstance(self.settings[name], dict):
            return Settings(data=self.settings[name])
        return self.settings[name]


# noinspection SqlNoDataSourceInspection
def get_chats(settings: Settings) -> List[int]:
    """Get list of users' Telegram ids from db."""
    users = []
    with psycopg2.connect(settings.database.uri) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT chat_id FROM users;")
            for user in cursor.fetchall():
                users.append(user[0])
    return users


# noinspection SqlNoDataSourceInspection
def save_activity(settings: Settings, user_id: int, duration: int, online_at: datetime, offline_at: datetime) -> bool:
    """Save activity for a user."""
    data = {
        'user_id': user_id,
        'duration': duration,
        'online_at': online_at,
        'offline_at': offline_at

    }
    with psycopg2.connect(settings.database.uri) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO user_activity (user_id, online_at, offline_at, duration)"
                    "VALUES (%(user_id)s, %(online_at)s, %(offline_at)s, %(duration)s);",
                    data
                )
                conn.commit()
            except psycopg2.IntegrityError:
                logger.warning("User id {} is not registered.".format(data['user_id']))


# noinspection SqlNoDataSourceInspection
def db_setup(settings: Settings) -> None:
    """Setup database for the app."""
    with psycopg2.connect(settings.database.uri) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE users (
                    chat_id integer PRIMARY KEY,
                    username varchar(150) not null,
                    email varchar(150)
                );"""
            )
            cursor.execute(
                """CREATE TABLE user_activity (
                    user_id integer not null references users(chat_id),
                    online_at timestamp without time zone not null,
                    offline_at timestamp without time zone not null,
                    duration float not null
                    
                );"""
            )
            conn.commit()


# noinspection SqlNoDataSourceInspection
def get_users(settings: Settings) -> List[dict]:
    users = []
    with psycopg2.connect(settings.database.uri) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT chat_id, username, email FROM users;"
            )
            for user in cursor.fetchall():
                users.append({
                    'username': user[1],
                    'user_id': user[0],
                    'email': user[2]
                })
    return users


# noinspection SqlNoDataSourceInspection
def populate_dummy_history(settings: Settings, date_range: int = 7) -> None:
    now = datetime.now()
    users = get_users(settings)
    for user in users:
        for i in range(date_range):
            online_at = now - timedelta(days=i)
            duration = randint(1, 120)
            offline_at = online_at + timedelta(seconds=duration)
            save_activity(settings, user['user_id'], duration, online_at, offline_at)
