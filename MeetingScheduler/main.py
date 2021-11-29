import ConfigParser
import psycopg2


def db_connect():
    config = ConfigParser.RawConfigParser()
    config.read('Database.properties')

    print(config.get('DatabaseSection', 'database.dbname'))
    conn = psycopg2.connect(host=config.get('DatabaseSection', 'host'),
                            database="config.get('DatabaseSection', 'database')",
                            user=config.get('DatabaseSection', 'user'),
                            password=config.get('DatabaseSection', 'password'))
    return conn


def main():
    pass


if __name__ == '__main__':
    main()
