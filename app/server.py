import socket
import pickle
import threading
from random import randrange
from app.DataBaseManager import ItemManager, RoomManager, DataManager
from app.room import Room
import datetime


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.room_manager = RoomManager()
        self.user_manager = DataManager()
        self.item_manager = ItemManager()
        self.active_rooms = {}

    def room_creator(self, user):
        create_room = Room(
            input("Add item: "), input("Add price: "), input("Add time:")
        )
        create_room.create_room()
        create_room.add_user(user)
        create_room.inside_room()
        self.active_rooms[create_room.room_name] = create_room

    def join_room(self, room, user):
        room_name = room[1]
        room_data = f"Joining room: {room_name}\nTime: {room[4]}\nStarting Price: {room[3]}\nStatus: {room[5]}"

        if room_name in self.active_rooms:
            active_room = self.active_rooms[room_name]
            active_room.add_user(user)
            return room_data
        else:
            print("Room not found.")

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New client connected: {client_address}")
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket,)
            )
            client_thread.start()

    def handle_client(self, client_socket):
        user = None

        while True:
            try:
                request = ""
                user_data = client_socket.recv(5048)
                try:
                    user = pickle.loads(user_data)
                    print("Received user_data:", user)
                    log_in = "Log in"
                    self.user_manager.save_logs(user.username, log_in)
                except pickle.UnpicklingError:
                    print("Unpickling user_data:", user_data)
                    user_data_decode = user_data.decode()
                    if user_data_decode == "0":
                        response = self.process_request(request, user)
                        client_socket.send(response.encode())
                        continue
                    if "room_creator" != user_data_decode != "get_rooms":
                        request = "join_room," + user_data_decode
                    else:
                        request = "get_rooms"
                    response = self.process_request(request, user)
                    client_socket.send(response.encode())
                    continue

                request = client_socket.recv(5048).decode()
                print(request)
                if not request:
                    break
                else:
                    response = self.process_request(request, user)
                    client_socket.send(response.encode())

            except ConnectionResetError:
                break
        log_out = "Log out"
        self.user_manager.save_logs(user.username, log_out)
        client_address = client_socket.getpeername()
        print(f"Client disconnected: {client_address}")
        client_socket.close()

    def process_request(self, request, user):
        request_parts = request.split(",")
        if request_parts[0] == "room_creator":
            item_name = request_parts[1]
            item_price = request_parts[2]
            item_time = request_parts[3]
            self.room_manager.add_room(item_name, item_price, item_time)
            self.room_creator(user)
            return "Room created successfully."

        elif request_parts[0] == "join_room":
            room_id = int(request_parts[1])
            room = self.room_manager.get_room_by_id(room_id)
            if room is not None:
                print(room[0])
                print("Joined the room!")
                return self.join_room(room, user)
            else:
                return "Room not found."

        elif request_parts[0] == "get_rooms":
            room_list = self.room_manager.get_rooms()
            rooms_info = ""
            for room in room_list:
                rooms_info += f"\n-ID: {room[0]}\n\t-Room Name: {room[1]}\n\t-Time: {room[4]}\n\t-Status: {room[5]} \n\t-Price: {room[3]} "
            return rooms_info


if __name__ == "__main__":
    server = Server("localhost", 8080)
    server.start()
