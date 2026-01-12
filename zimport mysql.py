

import re
from tabulate import tabulate
from employee_entity import Employee
from crud_operations import EmployeeCRUD

class EmployeeService:
    def __init__(self, crud):
        self.crud = crud

    def trim_input(self, text):
        return text.split(" ")[0]

    def validate_name(self, name):
        pattern = r'^[A-Za-z\s\'-]+$'
        return re.match(pattern, name) and self.trim_input(name.strip())

    def validate_designation(self, name):
        pattern = r'^[A-Za-z\s\'-]+$'
        return re.match(pattern, name) and name.strip()

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    def validate_phone(self, phone):
        pattern = r'^\d{10}$'
        return re.match(pattern, phone)

    def is_unique(self, field, value, current_employee=None):
        employees = self.crud.read_employees()
        for emp in employees:
            if emp == current_employee:
                continue
            if emp[field] == value:
                return False
        return True

    def get_valid_input(self, prompt, validation_func, error_message, unique_field=None, current_employee=None):
        while True:
            value = input(prompt).strip()
            value = self.trim_input(value.strip())
            if not validation_func(value):
                print(f"Error: {error_message}")
                continue
            if unique_field and not self.is_unique(unique_field, value, current_employee):
                print(f"Error: {unique_field.capitalize()} must be unique.")
                continue
            return value

    def create_employee_service(self):
        print("\n--- Add Employee ---")
        first_name = self.get_valid_input(
            "Enter First Name: ",
            self.validate_name,
            "First name must contain only letters, spaces, hyphens, or apostrophes.",
            unique_field='first_name'
        )
        last_name = self.get_valid_input(
            "Enter Last Name: ",
            self.validate_name,
            "Last name must contain only letters, spaces, hyphens, or apostrophes."
        )
        email = self.get_valid_input(
            "Enter Email: ",
            self.validate_email,
            "Invalid email format.",
            unique_field='email'
        )
        phone = self.get_valid_input(
            "Enter Phone (10 digits): ",
            self.validate_phone,
            "Invalid phone number. Must be 10 digits.",
            unique_field='phone'
        )
        designation = self.get_valid_input(
            "Enter Designation: ",
            self.validate_designation,
            "Designation must contain only letters, spaces, hyphens, or apostrophes."
        )

        new_emp = Employee(first_name, last_name, email, phone, designation)
        self.crud.create_employee(new_emp)
        print(f"Employee {first_name} {last_name} added successfully!")

    def read_employees_service(self):
        employees = self.crud.read_employees()
        if not employees:
            print("\nNo employees found.\n")
            return
        print("\n--- Employee List ---")
        print(tabulate(employees, headers="keys", tablefmt="grid"))

    def update_employee_service(self):
        print("\n--- Update Employee ---")
        first_name = input("Enter the first name of the employee to update: ").strip()
        employees = self.crud.read_employees()
        for emp in employees:
            if emp['first_name'] == first_name:
                updated_emp = Employee(
                    self.get_valid_input(
                        f"Enter new First Name (current: {emp['first_name']}): ",
                        self.validate_name,
                        "First name must contain only letters, spaces, hyphens, or apostrophes.",
                        unique_field='first_name',
                        current_employee=emp
                    ) or emp['first_name'],
                    self.get_valid_input(
                        f"Enter new Last Name (current: {emp['last_name']}): ",
                        self.validate_name,
                        "Last name must contain only letters, spaces, hyphens, or apostrophes.",
                        current_employee=emp
                    ) or emp['last_name'],
                    self.get_valid_input(
                        f"Enter new Email (current: {emp['email']}): ",
                        self.validate_email,
                        "Invalid email format.",
                        unique_field='email',
                        current_employee=emp
                    ) or emp['email'],
                    self.get_valid_input(
                        f"Enter new Phone (current: {emp['phone']}): ",
                        self.validate_phone,
                        "Invalid phone number. Must be 10 digits.",
                        unique_field='phone',
                        current_employee=emp
                    ) or emp['phone'],
                    input(f"Enter new Designation (current: {emp['designation']}): ").strip() or emp['designation']
                )
                self.crud.update_employee(first_name, updated_emp)
                print("Employee details updated successfully.\n")
                return
        print("Error: Employee not found.\n")

    def delete_employee_service(self):
        print("\n--- Delete Employee ---")
        first_name = input("Enter the first name of the employee to delete: ").strip()
        employees = self.crud.read_employees()
        for emp in employees:
            if emp['first_name'] == first_name:
                self.crud.delete_employee(first_name)
                print("Employee deleted successfully.\n")
                return
        print("Error: Employee not found.\n")

    def search_employee_service(self):
        print("\n--- Search Employee ---")
        keyword = input("Enter a keyword to search (name or email): ").strip().lower()
        employees = self.crud.read_employees()
        found = False
        for emp in employees:
            if (keyword in emp['first_name'].lower() or
                keyword in emp['last_name'].lower() or
                keyword in emp['email'].lower()):
                print(f"Found: {emp['first_name']} {emp['last_name']}, Email: {emp['email']}, Phone: {emp['phone']}, Designation: {emp['designation']}")
                found = True
        if not found:
            print("No matching employee found.\n")

    def display_menu(self):
        print("\n--- Employee Management System ---")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Search Employee")
        print("6. Exit")


from services import EmployeeService
from crud_operations import EmployeeCRUD

def main():
    crud = EmployeeCRUD()
    service = EmployeeService(crud)
    while True:
        try:
            service.display_menu()
            choice = input("Enter your choice (1-6): ").strip()
            if choice == '1':
                service.create_employee_service()
            elif choice == '2':
                service.read_employees_service()
            elif choice == '3':
                service.update_employee_service()
            elif choice == '4':
                service.delete_employee_service()
            elif choice == '5':
                service.search_employee_service()
            elif choice == '6':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.\n")
        except Exception as e:
            print(f"Error: An error occurred in the main function. {e}")

if __name__ == "__main__":
    main()

from connection import DatabaseConnection
from employee_entity import Employee

class EmployeeCRUD:
    def __init__(self):
        # Initialize the database connection once
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