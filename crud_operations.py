from connection import DatabaseConnection
from employee_entity import Employee

class EmployeeCRUD:
    def __init__(self):
        db = DatabaseConnection()
        self.db_connection = db.get_db_connection()

    def create_employee(self, employee):
        cursor = self.db_connection.cursor()
        query = "INSERT INTO employees (first_name, last_name, email, phone, designation) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (employee.first_name, employee.last_name, employee.email, employee.phone, employee.designation))
        self.db_connection.commit()
        cursor.close()

    def read_employees(self):
        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        cursor.close()
        return employees
    
    def read_one_employees(self, first_name):
        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees WHERE first_name = %s", first_name )
        employees = cursor.fetchall()
        cursor.close()
        return employees

    def update_employee(self, first_name, updated_employee):
        cursor = self.db_connection.cursor()
        query = """ UPDATE employees SET first_name = %s, last_name = %s, email = %s, phone = %s, designation = %s WHERE first_name = %s """
        cursor.execute(query, (updated_employee.first_name, updated_employee.last_name, updated_employee.email, updated_employee.phone, updated_employee.designation, first_name))
        self.db_connection.commit()
        cursor.close()

    def delete_employee(self, first_name):
        cursor = self.db_connection.cursor()
        query = "DELETE FROM employees WHERE first_name = %s"
        cursor.execute(query, (first_name,))
        self.db_connection.commit()
        cursor.close()