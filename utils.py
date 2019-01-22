import json
import psycopg2


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


def get_chats(settings: Settings):
    """Get list of users' Telegram ids from db."""
    users = []
    with psycopg2.connect(settings.database.uri) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT chat_id FROM users WHERE active = TRUE")
            for user in cursor.fetchall():
                users.append(user[0])
    return users
