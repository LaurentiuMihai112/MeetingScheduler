import configparser
import psycopg2


def db_connect():
    """
    Function used to connect to the database
    :return: The connection to the database
    """
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
        """
        Method to add a new person to the database
        :param firstname: Person's firstname
        :param lastname: Person's lastname
        :return: True on successfully adding a person to database, False otherwise
        """
        try:
            sql = "INSERT INTO Persons (firstname, lastname) VALUES (%s, %s)"
            val = (firstname, lastname)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            Utils.connection.commit()
        except Exception as e:
            print(str(e))
            return False
        return True

    @staticmethod
    def get_person(firstname, lastname):
        """
        Method to check the existence of a person
        :param firstname: Person's firstname
        :param lastname: Person's lastname
        :return: True if the person exists, False otherwise
        """
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
            print(str(e))
            return False

    @staticmethod
    def get_person_id(firstname, lastname):
        """
        Method to get the id of a person from database
        :param firstname: Person's firstname
        :param lastname: Person's lastname
        :return: id of the person for the name provided, None if no person was found
        """
        try:
            sql = "SELECT person_id FROM Persons WHERE firstname=%s and lastname=%s"
            val = (firstname, lastname)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            id = cursor.fetchone()
            cursor.close()
            return id
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def add_meeting(start_date, end_date):
        """
        Method to schedule a new meeting
        :param start_date: start date of the meeting
        :param end_date: end date of the meeting
        :return: True if the meeting was created, False otherwise
        """
        try:
            sql = "INSERT INTO Meetings (startdate, enddate) VALUES (%s, %s)"
            val = (start_date, end_date)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            Utils.connection.commit()
            cursor.close()
        except Exception as e:
            print(str(e))
            return False
        return True

    @staticmethod
    def add_participants(meeting_id, person_id):
        """
        Method to add a participant to a meeting
        :param meeting_id: the meeting id
        :param person_id: the person id
        :return: True if the participants was added, False otherwise
        """
        try:
            sql = "INSERT INTO MeetingParticipants VALUES (%s, %s)"
            val = (meeting_id, person_id)
            cursor = Utils.connection.cursor()
            cursor.execute(sql, val)
            Utils.connection.commit()
            cursor.close()
        except Exception as e:
            print(str(e))
            return False
        return True

    @staticmethod
    def get_participants(meeting_id: str):
        """
        Method to get all the participants to a meeting
        :param meeting_id: the meeting id
        :return: List of integers (participants id), None if an exception occurred
        """
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
        """

        :param start_date:
        :param end_date:
        :return:
        """
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
        """

        :param start_date:
        :param end_date:
        :return:
        """
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
        """
        shall retrieve all persons from database
        :return: List of lists
        """
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
        """
        Shall retrieve a specified person from the database
        :param id: the id of a person
        :return: the person with the specified id, None otherwise
        """
        try:
            sql = "SELECT CONCAT(lastname,' ',firstname) FROM Persons WHERE person_id=%s"
            cursor = Utils.connection.cursor()
            cursor.execute(sql, id)
            person = cursor.fetchone()
            cursor.close()
            return person
        except Exception as e:
            print(str(e))
            return None
