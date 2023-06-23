import re
from .DataBaseManager import DataManager


def verify_password(password, password_again):
    numbers = False
    special_symbol = False
    len_11 = False
    upper_case = False
    count_up = 0

    if password != password_again:
        password = input("Passwords do not match: ")
        password_again = input("Enter the password again: ")
    else:
        while True:
            if len(password) >= 11:
                len_11 = True
                for element in password:
                    if element.isdigit():
                        numbers = True
                    if not element.isalnum():
                        special_symbol = True
                    if element.isupper():
                        count_up += 1
                        if count_up >= 2:
                            upper_case = True
                if not len_11:
                    print("Password length should be at least 11 characters.")
                    password = input("Enter a password with at least 11 characters: ")
                elif not numbers:
                    print("Password should contain at least one digit.")
                    password = input("Enter a password with at least one digit: ")
                elif not special_symbol:
                    print("Password should contain at least one special symbol.")
                    password = input(
                        "Enter a password with at least one special symbol: "
                    )
                elif not upper_case:
                    print("Password should contain at least two uppercase letters.")
                    password = input(
                        "Enter a password with at least 2 uppercase letters: "
                    )
                else:
                    print("Password is valid!")
                    break
            else:
                password = input("Password must be at least 11 characters: ")
    return password


def verify_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.fullmatch(regex, email):
        print("Valid Email")
        return email
    else:
        while True:
            print("Invalid Email")
            email = input("Enter valid email:")
            if re.fullmatch(regex, email):
                print("Valid Email")
                break
        return email


def verify_username(username):
    data_manager = DataManager()
    while data_manager.is_username_taken(username):
        print("Username is already taken. Please choose a different username.")
        username = input("Enter a valid username: ")
        if username == "":
            return None
    return username


def valid_email(email):
    data_manager = DataManager()
    while data_manager.is_email_taken(email):
        print("Email is already taken. Please choose a different email.")
        email = input("Enter a valid email: ")
    return email
