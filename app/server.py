import websockets
import asyncio
import pickle
import threading
from random import randrange
from app.DataBaseManager import ItemManager, RoomManager, DataManager
from app.room import Room


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.room_manager = RoomManager()
        self.user_manager = DataManager()
        self.item_manager = ItemManager()
        self.active_rooms = {}
        self.client_list = set()

    def get_user_room(self, user):
        for room_name, room in self.active_rooms.items():
            if user in room.get_users():
                return room_name
        return None

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

    def bid_place(self, user, amount, room_name):
        if room_name:
            room = self.active_rooms[room_name]
            bid_data = room.place_bid(user, amount)
            self.send_to_all(bid_data)
            return bid_data

        else:
            return "Invalid data"

    async def handle_client(self, websocket):
        self.client_list.add(websocket)
        user = None
        running = True
        while running:
            try:
                async for user_data in websocket:
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
                        if user_data_decode == "Exit":
                            running = False
                        if user_data_decode == "0":
                            response = "Back to menu"
                            await websocket.send(response)
                            continue

                        user_data_parts = user_data_decode.split(",")
                        if "room_creator" == user_data_parts[0]:
                            request = user_data_decode
                        elif "get_rooms" == user_data_parts[0]:
                            request = user_data_decode
                        elif "bid_place" == user_data_parts[0]:
                            bid_list = ["bid_place", user_data_parts[1]]
                            request = ",".join(bid_list)
                        else:
                            join_list = ["join_room", user_data_decode]
                            request = ",".join(join_list)

                        response = self.process_request(request, user)
                        await websocket.send(response)
                        continue
                    if running:
                        request = await websocket.recv()
                        request = request.decode()
                        print(request)
                        if not request or request == "Exit":
                            running = False
                        else:
                            response = self.process_request(request, user)
                            await websocket.send(response)
                            await self.send_to_all(response)
            except ConnectionResetError:
                break
        log_out = "Log out"
        if user is not None:
            self.user_manager.save_logs(user.username, log_out)
            print(f"Client disconnected: {websocket.remote_address}")
        else:
            print(f"Client disconnected")
        self.client_list.remove(websocket)

    async def send_to_all(self, response):
        for client in self.client_list:
            try:
                await client.send(response)
            except websockets.exceptions.ConnectionClosedError:
                continue

    def start(self):
        start_server = websockets.serve(self.handle_client, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        print(f"Server listening on {self.host}:{self.port}...")
        asyncio.get_event_loop().run_forever()

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

        elif request_parts[0] == "bid_place":
            return self.bid_place(user, int(request_parts[1]), self.get_user_room(user))


if __name__ == "__main__":
    server = Server("localhost", 8080)
    server.start()
