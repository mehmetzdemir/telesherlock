import json
import psycopg2
from datetime import datetime, timedelta
from typing import List


class Settings(object):
    """Parse settings file."""
    def __init__(self, filename='../credentials.json', data=None):
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
def get_activities(settings: Settings, active_from: datetime = None):
    activity_data = {}
    sql = "SELECT users.username, user_activity.online_at::date, SUM(duration) " \
          "FROM user_activity " \
          "INNER JOIN users ON (users.chat_id = user_activity.user_id)" \
          "WHERE online_at > %(online_at)s GROUP BY 1, 2 ORDER BY 2"
    if not active_from:
        active_from = datetime.now() - timedelta(days=7)
    data = {'online_at': active_from}
    with psycopg2.connect(settings.database.uri) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, data)
            for activity in cursor.fetchall():
                if activity[1] not in activity_data:
                    activity_data[activity[1]] = []
                activity_data[activity[1]].append(
                    {'user': activity[0], 'duration': activity[2]}
                )
    return activity_data


# noinspection SqlNoDataSourceInspection
def get_users(settings: Settings) -> List[dict]:
    users = []
    with psycopg2.connect(settings.database.uri) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT username, email FROM users;"
            )
            for user in cursor.fetchall():
                users.append({
                    'username': user[0],
                    'email': user[1]
                })
    return users
