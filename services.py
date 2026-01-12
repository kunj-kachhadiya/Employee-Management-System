
import re
from tabulate import tabulate 
from connection import DatabaseConnection
from employee_entity import Employee
from crud_operations import EmployeeCRUD

class EmployeeService:
    def __init__(self, crud):
        self.crud = crud

    def trimip(self, text):
        return text.split(" ")[0]

    def validate_name(self, name):
        pattern = r'^[A-Za-z\s\'-]+$'
        return re.match(pattern, name) and self.trimip(name.strip())

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
            value = self.trimip(value.strip())
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
        try:
            employees = self.crud.read_employees()
            if not employees:
                print("\nNo employees found.\n")
                return
            print("\n--- Employee List ---")
            print(tabulate(employees, headers="keys", tablefmt="grid"))
        except Exception as e:
            print(f"Error: unable to read employee. {e}")

    def update_employee_service(self):
        print("\n--- Update Employee ---")
        try:
            first_name = input("Enter the first name of the employee to update: ").strip()
            employees = self.crud.read_employees()
            for emp in employees:
                if emp['first_name'] == first_name:
                    print(f"Updating employee: {emp['first_name']} {emp['last_name']}")

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
        except Exception as e:
            print(f"Error: unable to update employee. {e}")

    def delete_employee_service(self):
        print("\n--- Delete Employee ---")
        try:
            first_name = input("Enter the first name of the employee to delete: ").strip()
            employees = self.crud.read_employees()
            for emp in employees:
                if emp['first_name'] == first_name:
                    print(f"Deleting employee: {emp['first_name']} {emp['last_name']}")
                    self.crud.delete_employee(first_name)
                    print("Employee deleted successfully.\n")
                    return
            print("Error: Employee not found.\n")
        except Exception as e:
            print(f"Error: unable to delete employee. {e}")

    def readone_employee_service(self):
        print("\n--- Search Employee ---")
        try:
            first_name = input("Enter the first name of the employee to search: ").strip()
            employees = self.crud.read_employees()
            for emp in employees:
                if emp['first_name'] == first_name:
                    print(f"Found: {emp['first_name']} {emp['last_name']}, Email: {emp['email']}, Phone: {emp['phone']}, Designation: {emp['designation']}")
                    return
            print("Error: Employee not found.\n")
        except Exception as e:
            print(f"Error: unable to delete employee. {e}")

    def search_employee_service(self):
        print("\n--- Search Employee ---")
        try:
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
        except Exception as e:
            print(f"Error: unable to search employee. {e}")
    
    def display_menu(self):
        print("\n--- Employee Management System ---")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Search Employee")
        print("6. read one employee")
        print("6. Exit")

