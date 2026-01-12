import mysql.connector
class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def get_db_connection(self):
        """Create and return a MySQL database connection."""
        try:
            if not self.connection:
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="kunj@1234",
                    database="EmployeeDB"
            )
            return self.connection
        except mysql.connector.Error as err:
            print(f"error : error while connecting database. {err}")

    def close_db_connection(self):
        """Close the database connection."""
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
        except mysql.connector.Error as err:
            print(f"error : error while disconnecting database. {err}")
