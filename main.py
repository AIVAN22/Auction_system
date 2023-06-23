from getpass import getpass
from app.user import User, DataManager
from app.authorization import authorize_user


def main():
    authorize_user()


if __name__ == "__main__":
    main()
