from services import EmployeeService
from crud_operations import EmployeeCRUD

def main():
    crud = EmployeeCRUD()
    service = EmployeeService(crud)
    while True:
        try:
            service.display_menu()
            choice = input("Enter your choice (1-5): ").strip()
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
                service.readone_employee_service()
            elif choice == '7':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.\n")
        except Exception as e:
            print(f"Error: error occurred in main function. {e}")

if __name__ == "__main__":
    main()