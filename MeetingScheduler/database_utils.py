import configparser
import psycopg2


def db_connect():
    config = configparser.RawConfigParser()
    config.read('Database.properties')

    conn = psycopg2.connect(host=config.get('DatabaseSection', 'host'),
                            database=config.get('DatabaseSection', 'database'),
                            user=config.get('DatabaseSection', 'user'),
                            password=config.get('DatabaseSection', 'password'))
    return conn


class Utils:
    connection = db_connect()

    @staticmethod
    def add_person(firstname, lastname):
        sql = "INSERT INTO Persons (firstname, lastname) VALUES (%s, %s)"
        val = (firstname, lastname)
        cursor = Utils.connection.cursor()
        print(cursor.execute(sql, val))
        Utils.connection.commit()

    @staticmethod
    def add_meeting(start_date, end_date):
        pass

    @staticmethod
    def get_all_meetings(start_date, end_date):
        pass
