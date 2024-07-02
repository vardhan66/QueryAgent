import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self, db_params):
        self.db_params = db_params
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.db_params)
            self.cursor = self.connection.cursor()
            print("Connection successful")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error connecting to database: {error}")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error executing query: {error}")
            self.connection.rollback()

    def fetch_results(self):
        try:
            return self.cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching results: {error}")
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed")

# Define your database connection parameters
db_params = {
    'dbname': 'vvit',
    'user': 'eswar',
    'password': '------',
    'host': 'localhost',
    'port': '5432'  # default is 5432
}

# Usage
db = Database(db_params)
db.connect()


def get_all_student_details():
    data=db.execute_query("Select * from mis_student;")
    return data

db.close()
