import socket
import pymongo
import hashlib
import encrypt_decrypt

connection = pymongo.MongoClient("localhost", 27017)
db = connection['auction']
users_collection = db['users']
bids_collection = db['bids']
items_collection = db['items']

class Auction_server():
    def __init__(self):
        self.server_ip = "localhost"
        self.server_port = 8080
        self.key = "Htet"
        self.encrypter = encrypt_decrypt.Htet_Encryption()

    def request_from_client(self, sock):
        try:
            request = sock.recv(4096).decode("utf-8")
            decrypted_request = self.encrypter.start_decryption(request, self.key)
            return decrypted_request
        except Exception as e:
            print(f"Error receiving from client: {e}")
            return ""

    def response_to_client(self, response, sock):
        try:
            encrypted_message = self.encrypter.start_encryption(response, self.key)
            sock.send(bytes(encrypted_message, "utf-8"))
        except Exception as e:
            print(f"Error sending to client: {e}")

    def main(self):
        auction_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        auction_server.bind((self.server_ip, self.server_port))
        auction_server.listen()
        print(f"Server listening on port: {self.server_port} and IP: {self.server_ip}")
        try:
            while True:
                client, address = auction_server.accept()
                print(f"Accepted connection from {address[0]}:{address[1]}")
                self.client_control(client)
        except Exception as err:
            print(f"Error in main loop: {err}")

    def client_control(self, client_socket):
        with client_socket as sock:
            self.response_to_client("Successfully Connected!!", sock)
            while True:
                request = self.request_from_client(sock)
                if not request:
                    print("No request received or connection closed.")
                    break

                print(f"Request received: {request}")

                if request.startswith("register"):
                    self.register(sock, request)
                elif request.startswith("login"):
                    self.login(sock, request)
                elif request.startswith("add_item"):
                    self.add_item(sock, request)
                elif request.startswith("view_items"):
                    self.view_items(sock)
                elif request.startswith("bid"):
                    self.place_bid(sock, request)
                else:
                    self.response_to_client("Unknown command", sock)

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def register(self, sock, request):
        try:
            _, username, password = request.split("|")
            if users_collection.find_one({"username": username}):
                self.response_to_client("User already exists. Please try again.", sock)
                return

            hashed_pw = self.hash_password(password)
            users_collection.insert_one({"username": username, "password": hashed_pw})
            self.response_to_client("Registration successful.", sock)
        except Exception as err:
            self.response_to_client(f"Registration failed: {err}", sock)

    def login(self, sock, request):
        try:
            _, username, password = request.split("|")
            user = users_collection.find_one({"username": username})
            if not user:
                self.response_to_client("User does not exist. Please register.", sock)
                return

            hashed_pw = self.hash_password(password)
            if user["password"] == hashed_pw:
                self.response_to_client("Login successful", sock)
            else:
                self.response_to_client("Invalid credentials. Please try again.", sock)
        except Exception as err:
            self.response_to_client(f"Login failed: {err}", sock)

    def add_item(self, sock, request):
        try:
            _, item_name, item_description, starting_bid = request.split("|")
            starting_bid = float(starting_bid)
            items_collection.insert_one({
                "name": item_name,
                "description": item_description,
                "starting_bid": starting_bid,
                "current_bid": starting_bid,
            })
            self.response_to_client("Item added successfully.", sock)
        except Exception as err:
            self.response_to_client(f"Failed to add item: {err}", sock)

    def view_items(self, sock):
        try:
            items = items_collection.find()
            item_list = "\n".join([f"{item['name']} - {item['description']} - Starting Bid: ${item['starting_bid']} - Current Bid: ${item['current_bid']}" for item in items])
            if not item_list:
                item_list = "No items available."
            self.response_to_client(item_list, sock)
        except Exception as err:
            self.response_to_client(f"Failed to retrieve items: {err}", sock)

    def place_bid(self, sock, request):
        try:
            _, username, item_name, bid_amount = request.split("|")
            bid_amount = float(bid_amount)

            user = users_collection.find_one({"username": username})
            if not user:
                self.response_to_client("User does not exist. Please login.", sock)
                return

            item = items_collection.find_one({"name": item_name})
            if not item:
                self.response_to_client("Item does not exist. Please try again.", sock)
                return

            if bid_amount <= item["current_bid"]:
                self.response_to_client("Bid must be higher than the current highest bid.", sock)
                return

            bids_collection.insert_one({"username": username, "item_id": item["_id"], "bid_amount": bid_amount})
            items_collection.update_one({"_id": item["_id"]}, {"$set": {"current_bid": bid_amount}})
            self.response_to_client(f"Bid placed successfully. Current highest bid for {item_name} is now ${bid_amount}.", sock)
        except Exception as err:
            self.response_to_client(f"Failed to place bid: {err}", sock)

if __name__ == "__main__":
    auction_server = Auction_server()
    auction_server.main()