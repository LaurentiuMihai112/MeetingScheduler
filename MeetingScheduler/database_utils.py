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
        try:
            sql = "INSERT INTO Persons (firstname, lastname) VALUES (%s, %s)"
            val = (firstname, lastname)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            Utils.connection.commit()
        except Exception as e:
            return str(e)
        return True

    @staticmethod
    def get_person(firstname, lastname):
        try:
            sql = "SELECT firstname, lastname FROM Persons WHERE firstname=%s and lastname=%s"
            val = (firstname, lastname)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            person = cursor.fetchone()
            cursor.close()
            if person is not None:
                return True
            return False
        except Exception as e:
            return str(e)

    @staticmethod
    def get_person_id(firstname, lastname):
        try:
            sql = "SELECT person_id FROM Persons WHERE firstname=%s and lastname=%s"
            val = (firstname, lastname)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            id = cursor.fetchone()
            cursor.close()
            return id
        except Exception as e:
            return str(e)

    @staticmethod
    def add_meeting(start_date, end_date):
        try:
            sql = "INSERT INTO Meetings (startdate, enddate) VALUES (%s, %s)"
            val = (start_date, end_date)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            Utils.connection.commit()
            cursor.close()
        except Exception as e:
            return str(e)
        return True

    @staticmethod
    def add_participants(meeting_id, person_id):
        try:
            sql = "INSERT INTO MeetingParticipants VALUES (%s, %s)"
            val = (meeting_id, person_id)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            Utils.connection.commit()
            cursor.close()
        except Exception as e:
            return str(e)
        return True

    @staticmethod
    def get_participants(meeting_id: str):
        try:
            sql = "SELECT person_id FROM MeetingParticipants WHERE meeting_id='{0}'".format(meeting_id)
            cursor = Utils.connection.cursor()
            cursor.execute(sql)
            ids = cursor.fetchall()
            cursor.close()
            return ids
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_meeting_id(start_date, end_date):
        try:
            sql = "SELECT meeting_id FROM Meetings WHERE startdate=%s AND enddate=%s"
            val = (start_date, end_date)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            id = cursor.fetchone()
            cursor.close()
            return id
        except Exception as e:
            return str(e)

    @staticmethod
    def get_all_meetings(start_date, end_date):
        try:
            sql = "SELECT * FROM Meetings WHERE startdate>=%s AND enddate<=%s"
            val = (start_date, end_date)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            return cursor.fetchall()
        except Exception as e:
            return str(e)

    @staticmethod
    def get_all_persons():
        try:
            sql = "SELECT CONCAT(lastname,' ',firstname) FROM Persons"
            cursor = Utils.connection.cursor()
            cursor.execute(sql)
            persons = cursor.fetchall()
            cursor.close()
            return persons
        except Exception as e:
            return str(e)

    @staticmethod
    def get_person_by_id(id: str):
        try:
            sql = "SELECT CONCAT(lastname,' ',firstname) FROM Persons WHERE person_id=%s"
            cursor = Utils.connection.cursor()
            cursor.execute(sql, id)
            person = cursor.fetchone()
            cursor.close()
            return person
        except Exception as e:
            return str(e)
