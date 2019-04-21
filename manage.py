import argparse
from utils import Settings, db_setup, populate_dummy_history


settings = Settings()


parser = argparse.ArgumentParser(description='Manage Telesherlock')
parser.add_argument(
    'command', metavar='command', type=str, help='Management command: setup_db, populate_data',
    choices=['setup_db', 'populate_data']
)
parser.add_argument(
    '--range', type=int, default=7, help='number of dates for dummy data'
)


if __name__ == '__main__':
    args = parser.parse_args()
    if args.command == 'setup_db':
        db_setup(settings)
    elif args.command == 'populate_data':
        populate_dummy_history(settings, date_range=args.range)
