from random import randrange
from .DataBaseManager import RoomManager, ItemManager


class Room:
    def __init__(self, item_name, price, auction_time_spend):
        self.item_name = item_name
        self.room_id = self.generating_room_id()
        self.room_name = self.generating_room_name()
        self.starting_price = price
        self.auction_time_spend = auction_time_spend
        self.users = []
        self.highest_bid = price
        self.highest_bidder = None
        self.status = "Open"
        self.room_manager = RoomManager()
        self.item_manager = ItemManager()

    def add_user(self, user):
        if len(self.users) < 5:
            self.users.append(user)
            print(f"{user.name} has joined Room {self.room_id}.")
        else:
            print("The room is already full. Cannot add more users.")

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)

    def get_users(self):
        users = []
        for user in self.users:
            users.append(user)
        return users

    def create_room(self):
        if not self.room_manager.is_room_exists(self.room_name):
            self.room_manager.create_room(
                self.room_id,
                self.room_name,
                self.item_name,
                self.starting_price,
                self.auction_time_spend,
                self.status,
            )
            print(f"Room '{self.room_name}' created.")
        else:
            print(f"Room '{self.room_name}' already exists.")
        self.item_manager.add_item_to_database(self.item_name, self.starting_price)

    def place_bid(self, user, bid_amount):
        if bid_amount > self.highest_bid:
            self.highest_bid = bid_amount
            self.highest_bidder = user
            print(f"{user.name} placed a bid of {bid_amount} on {self.item_name}.")
        else:
            print("Bid amount is not higher than the current highest bid.")

    def end_auction(self):
        if self.highest_bidder:
            print(f"The auction for {self.item_name} in Room {self.room_id} has ended.")
            print(
                f"The highest bidder is {self.highest_bidder.name} with a bid of {self.highest_bid}."
            )
        else:
            print(f"The auction for {self.item_name} in Room {self.room_id} has ended.")
            print("No bids were placed.")

    def generating_room_name(self):
        name_room = self.item_name + str(self.room_id)
        return name_room

    def generating_room_id(self):
        id_num = randrange(10, 100)
        return id_num

    def __str__(self):
        return f"{self.room_name} with {self.room_id}"
