import socket
import pickle
import threading
from random import randrange
from app.DataBaseManager import ItemManager, RoomManager, DataManager
from app.room import Room


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.room_manager = RoomManager()
        self.user_manager = DataManager()
        self.item_manager = ItemManager()
        self.active_rooms = {}
        self.client_list = []

    def room_creator(self, user, item_name, price, time):
        create_room = Room(item_name, price, time)
        create_room.create_room()
        create_room.add_user(user)
        self.active_rooms[create_room.room_name] = create_room
        users_list = create_room.get_users()
        user_info = "\n".join(str(user) for user in users_list)
        room_data = f"\nUsers: \n{user_info} \nCreate room: {create_room.room_name}\nTime: {create_room.auction_time_spend}\nStarting Price: {create_room.starting_price}\nStatus: {create_room.status}"
        return room_data

    def join_room(self, room, user):
        room_name = room[1]
        if room_name in self.active_rooms:
            active_room = self.active_rooms[room_name]
            active_room.add_user(user)
            users_list = active_room.get_users()
            user_info = "\n".join(str(user) for user in users_list)
            room_data = f"\nUsers: \n{user_info} \nJoined room: {active_room.room_name}\nTime: {active_room.auction_time_spend}\nStarting Price: {active_room.starting_price}\nStatus: {active_room.status}"
            self.send_to_all(room_data)
            return room_data
        else:
            return "Room not found."

    def bid_place(self, user, item_name, price, time, amount):
        room = Room(user, item_name, price, time)
        room.place_bid(user, amount)

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

    def send_to_all(self, response):
        for client_socket in self.client_list:
            client_socket.send(response.encode())

    def handle_client(self, client_socket):
        self.client_list.append(client_socket)
        user = None
        while True:
            try:
                user_data = client_socket.recv(5048)
                if not user_data:
                    break
                try:
                    request = ""
                    user = pickle.loads(user_data)
                    print("Received user_data:", user)
                    log_in = "Log in"
                    self.room_manager.create_room_table()
                    self.user_manager.create_users_table()
                    self.item_manager.create_items_table()
                    self.user_manager.save_logs(user.username, log_in)
                except pickle.UnpicklingError:
                    print("Unpickling user_data:", user_data)
                    user_data_decode = user_data.decode()
                    if user_data_decode == "0":
                        response = "Back to menu"
                        client_socket.send(response.encode())
                        continue
                    if user_data_decode == "1":
                        request = "bid_place"
                    user_data_parts = user_data_decode.split(",")
                    if "room_creator" == user_data_parts[0]:
                        request = user_data_decode
                    elif "get_rooms" == user_data_parts[0]:
                        request = user_data_decode
                    else:
                        join_list = ["join_room", user_data_decode]
                        request = ",".join(join_list)

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
        if user is not None:
            self.user_manager.save_logs(user.username, log_out)
            client_address = client_socket.getpeername()
            print(f"Client disconnected: {client_address}")
            client_socket.close()
        else:
            print(f"Client disconnected")
            client_socket.close()

    def process_request(self, request, user):
        request_parts = request.split(",")
        if request_parts[0] == "room_creator":
            item_name = request_parts[1]
            item_price = request_parts[2]
            item_time = request_parts[3]
            room_data = self.room_creator(user, item_name, item_price, item_time)
            return room_data

        elif request_parts[0] == "join_room":
            room_id = int(request_parts[1])
            room = self.room_manager.get_room_by_id(room_id)
            if room is not None:
                print(room[0])
                print("Joined the room!")
                join_the_room = self.join_room(room, user)
                return join_the_room
            else:
                return "Room not found."

        elif request_parts[0] == "get_rooms":
            room_list = self.room_manager.get_rooms()
            rooms_info = ""
            for room in room_list:
                rooms_info += f"\n-ID: {room[0]}\n\t-Room Name: {room[1]}\n\t-Time: {room[4]}\n\t-Status: {room[5]} \n\t-Price: {room[3]} "
            if rooms_info == "":
                return "No Rooms"
            return rooms_info

        elif request_parts == "bid_place":
            return self.bid_place()


if __name__ == "__main__":
    server = Server("localhost", 8080)
    server.start()
