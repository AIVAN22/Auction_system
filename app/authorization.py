from getpass import getpass
from app.user import User
from .DataBaseManager import DataManager
from app.Verification import verify_password, verify_email, verify_username, valid_email
from random import randrange


def authenticate_user():
    username = input("Username: ")
    password = getpass("Password: ")
    data_manager = DataManager()
    user_data = data_manager.get_user_by_username(username)
    if user_data is not None:
        name = user_data.name
        email = user_data.email
        username = user_data.username
        password = user_data.password
        user_id = user_data.user_ID
        user = User(name, email, username, password, user_id)
        if password == user.password:
            print("Authentication successful!")
            print(user)
            return user
        else:
            print("Invalid password!")
    else:
        print("User not found!")

    return None


def register_user():
    name = input("Name: ")
    email = input("Email: ")
    username = input("Username: ")
    password = getpass("Password: ")
    password_again = getpass("Password (again): ")
    password = verify_password(password, password_again)
    email = verify_email(email)
    username = verify_username(username)
    email = valid_email(email)
    data_manager = DataManager()
    while True:
        user_id = randrange(100, 10000)
        if not data_manager.is_id_taken(user_id):
            break

    user = User(name, email, username, password, user_id)
    user.save_data()
    print("User created successfully!")
    print(user)
    return user


def authorize_user():
    while True:
        choice = input("1. Login\n2. Register\n3. Exit\nEnter your choice: ")

        if choice == "1":
            user = authenticate_user()
            if user:
                return user
        elif choice == "2":
            user = register_user()
            if user:
                return user
        elif choice == "3":
            return None
        else:
            print("Invalid choice. Please try again.")
