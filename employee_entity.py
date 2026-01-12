class Employee:
    def __init__(self, first_name, last_name, email, phone, designation):
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._phone = phone
        self._designation = designation

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    @property
    def designation(self):
        return self._designation

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @email.setter
    def email(self, value):
        self._email = value

    @phone.setter
    def phone(self, value):
        self._phone = value

    @designation.setter
    def designation(self, value):
        self._designation = value

    def __str__(self):
        return (f"First Name: {self._first_name}, Last Name: {self._last_name}, "
                f"Email: {self._email}, Phone: {self._phone}, Designation: {self._designation}")