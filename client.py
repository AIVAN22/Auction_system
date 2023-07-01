import websockets
import asyncio
import pickle
from app.Verification import Authorization


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.authorization = Authorization()

    async def connect(self):
        url = f"ws://{self.host}:{self.port}"
        self.websocket = await websockets.connect(url)
        print(f"Connected to server at {self.host}:{self.port}")

    async def receive_messages(self):
        while True:
            try:
                response = await self.websocket.recv()
                print(response)
            except ConnectionResetError:
                print("Server disconnected.")
                break

    async def run(self):
        await self.connect()
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
                await self.websocket.send(user_data)
                await self.menu()

            else:
                print("Authentication failed. Exiting the program.")

        await self.websocket.close()

    async def menu(self):
        while True:
            print(
                "Choose: \n1. Create room \n2. Choose room \n3. Change profile info \n4. Exit"
            )
            user_input = int(input("Enter your choice: "))
            if user_input == 1:
                await self.create_room()
            elif user_input == 2:
                await self.get_room()
            elif user_input == 3:
                await self.change_info()
            elif user_input == 4:
                response = "Exit"
                await self.websocket.send(response.encode())

                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

    def action(self, response):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print(response)

        while True:
            choice = input("Enter Choice:\n1. Bid\n2. Exit room\n:")

            if choice == "1":
                choice = "bid_place"
                amount = input("Amount: ")
                amount_list = [choice, amount]
                asyncio.get_event_loop().run_until_complete(
                    self.websocket.send(",".join(amount_list))
                )
            elif choice == "2":
                choice = "0"
                print("Exiting the room.")
                break
            else:
                print("Invalid choice. Please try again.")

            response = asyncio.get_event_loop().run_until_complete(
                self.websocket.recv()
            )
            print(response)

        print("Failed to join the room.")

    async def create_room(self):
        item_name = input("Enter the item name: ")
        item_price = input("Enter the item price: ")
        item_time = input("Enter the item time: ")
        create_room_command = f"room_creator,{item_name},{item_price},{item_time}"
        await self.websocket.send(create_room_command.encode())
        response = await self.websocket.recv()
        self.action(response)

    async def get_room(self):
        join_room_command = "get_rooms"
        await self.websocket.send(join_room_command.encode())
        response = await self.websocket.recv()
        print("List of rooms:")
        print(response)
        room_id = input("Enter room ID (press 0 to go back): ")
        await self.websocket.send(room_id.encode())
        response = await self.websocket.recv()
        print(response)

        if response != "Back to menu":
            if response == "Room not found.":
                print(response)
            else:
                self.action(response)

    async def change_info(self):
        change_profile_command = "change_profile_info"
        await self.websocket.send(change_profile_command.encode())
        response = await self.websocket.recv()
        print(response)


if __name__ == "__main__":
    client = Client("localhost", 8080)
    asyncio.run(client.run())
