import configparser
import psycopg2

from meeting_scheduler import MeetingScheduler


def db_connect():
    config = configparser.RawConfigParser()
    config.read('Database.properties')

    conn = psycopg2.connect(host=config.get('DatabaseSection', 'host'),
                            database=config.get('DatabaseSection', 'database'),
                            user=config.get('DatabaseSection', 'user'),
                            password=config.get('DatabaseSection', 'password'))
    return conn


def main():
    print(db_connect())
    MeetingScheduler()


if __name__ == '__main__':
    main()
