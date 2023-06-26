import socket
import pickle
from app.Verification import Authorization


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.authorization = Authorization()

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

    def run(self):
        self.connect()
        user = self.authorization.authorize_user()

        if user is None:
            print("Exiting the program.")
        else:
            print(f"Welcome, {user.name}!")
            response = True
            print()
            print()

            if response:
                print("Authentication successful.")

                user_data = pickle.dumps(user)

                self.client_socket.send(user_data)

                while True:
                    print(
                        "Choose: \n1. Create room \n2. Choose room \n3. Change profile info \n4. Exit"
                    )
                    user_input = int(input("Enter your choice: "))
                    if user_input == 1:
                        item_name = input("Enter the item name: ")
                        item_price = input("Enter the item price: ")
                        item_time = input("Enter the item time: ")
                        create_room_command = (
                            f"room_creator,{item_name},{item_price},{item_time}"
                        )
                        self.client_socket.send(create_room_command.encode())
                        response = self.client_socket.recv(5048).decode()
                        print(response)
                        while True:
                            choice = input("Enter Choice:\n1. Bid\n2. Exit room\n:")
                            if choice == "1":
                                pass
                            elif choice == "2":
                                print("Exiting the room.")
                                break
                            else:
                                print("Invalid choice. Please try again.")

                    elif user_input == 2:
                        join_room_command = "get_rooms"
                        self.client_socket.send(join_room_command.encode())
                        response = self.client_socket.recv(5048).decode()
                        print("List of rooms:")
                        print(response)

                        room_id = int(input("Enter room ID (press 0 to go back): "))
                        self.client_socket.send(str(room_id).encode())
                        response = self.client_socket.recv(5048).decode()
                        print(response)

                        if response != "Back to menu":
                            if response == "Room not found.":
                                print(response)
                            else:
                                while True:
                                    choice = input(
                                        "Enter Choice:\n1. Bid\n2. Exit room\n:"
                                    )
                                    if choice == "1":
                                        pass
                                    elif choice == "2":
                                        print("Exiting the room.")
                                        break
                                    else:
                                        print("Invalid choice. Please try again.")

                                print("Failed to join the room.")
                        else:
                            continue

                    elif user_input == 3:
                        change_profile_command = "change_profile_info"
                        self.client_socket.send(change_profile_command.encode())
                        response = self.client_socket.recv(5048).decode()
                        print(response)
                    elif user_input == 4:
                        print("Exiting the program.")
                        break
                    else:
                        print("Invalid choice. Please try again.")

            else:
                print("Authentication failed. Exiting the program.")

        self.client_socket.close()


if __name__ == "__main__":
    client = Client("localhost", 8080)
    client.run()
