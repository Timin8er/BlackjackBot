import mysql.connector


class dbConnector():


    query_session_insert = "INSERT INTO sessions (name) VALUES ($(name)s)"
    query_session_find = "SELECT FROM sessions WHERE name = $(name)s"


    def __init__(self):

        self.connection = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="T!min8er",
          autocommit=True
        )

        self.curser = self.connection.curser()

        self.session_name = ''
        self.session_id = None



    def set_session(selfm name:str):
        self.session_name = name

        exists = self.curser.execute(self.query_session_find, {'name'=name})
        if not exists:
            self.new_session(name)


    def new_session(self, name:str):
        self.curser.execute(self.query_insert_session, {'name'=name})
