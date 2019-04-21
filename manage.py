import argparse
import sys
from utils import Settings, db_setup, populate_dummy_history, save_user


settings = Settings()


parser = argparse.ArgumentParser(description='Manage Telesherlock')
parser.add_argument(
    'command', metavar='command', type=str, help='Management command: setup_db, populate_data, add_user',
    choices=['setup_db', 'populate_data', 'add_user']
)
parser.add_argument(
    '--range', type=int, default=7, help='number of dates for dummy data'
)
parser.add_argument(
    '--chat_id', type=int, default=None, help='Telegram chat id'
)
parser.add_argument(
    '--username', type=str, default=None, help='Telegram username'
)
parser.add_argument(
    '--email', type=str, default=None, help='Gravatar email address'
)


if __name__ == '__main__':
    args = parser.parse_args()
    if args.command == 'setup_db':
        db_setup(settings)
    elif args.command == 'populate_data':
        populate_dummy_history(settings, date_range=args.range)
    elif args.command == 'add_user':
        if not args.chat_id:
            print("Please, provide chat_id for the user!")
            sys.exit(1)
        if not args.username:
            print("Please, provide username for the user!")
            sys.exit(1)
        if not args.email:
            print("Please, provide email for the user!")
            sys.exit(1)
        if not save_user(settings, chat_id=args.chat_id, username=args.username, email=args.email):
            print("User {} already exists in database!".format(args.chat_id))
            sys.exit(1)
