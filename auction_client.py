import socket
import encrypt_decrypt

class Auction_client():
    def __init__(self):
        self.target_ip = "localhost"
        self.target_port = 8080
        self.key = "Htet"
        self.encrypter = encrypt_decrypt.Htet_Encryption()

    def request_to_server(self, message, client_socket):
        encrypted_message = self.encrypter.start_encryption(message, self.key)
        client_socket.send(bytes(encrypted_message, "utf-8"))

    def response_from_server(self, client_socket):
        try:
            reply = client_socket.recv(4096).decode("utf-8")
            decrypted_reply = self.encrypter.start_decryption(reply, self.key)
            return decrypted_reply
        except ConnectionAbortedError:
            print("Connection was aborted by the server.")
            client_socket.close()
            return ""
        except Exception as e:
            print(f"Error receiving response from server: {e}")
            client_socket.close()
            return ""

    def client_runner(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.target_ip, self.target_port))
        return client_socket

    def client_menu(self):
        client_socket = self.client_runner()
        reply = self.response_from_server(client_socket)
        print(reply)

        choice = input("1:Register\n2:Login\n3:Exit\n")

        if choice == '1':
            self.register(client_socket)
        elif choice == '2':
            self.login(client_socket)
        elif choice == '3':
            print("Exiting...")
            client_socket.close()
            exit()

    def register(self, client_socket):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        message = f"register|{username}|{password}"
        self.request_to_server(message, client_socket)
        reply = self.response_from_server(client_socket)
        print(reply)

    def login(self, client_socket):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        message = f"login|{username}|{password}"
        self.request_to_server(message, client_socket)
        reply = self.response_from_server(client_socket)

        if "Login successful" in reply:
            print(f"Welcome, {username}. You are logged in.")
            self.auction_menu(client_socket)
        else:
            print(reply)

    def auction_menu(self, client_socket):
        while True:
            choice = input("1: Add Item\n2: Place Bid\n3: View Items\n4: Logout\n")

            if choice == '1':
                self.add_item(client_socket)
            elif choice == '2':
                self.place_bid(client_socket)
            elif choice == '3':
                self.view_items(client_socket)
            elif choice == '4':
                print("Logging out...")
                client_socket.close()
                break

    def add_item(self, client_socket):
        item_name = input("Enter the item name: ")
        item_description = input("Enter the item description: ")
        starting_bid = input("Enter the starting bid amount: ")
        auction_duration = input("Enter the auction duration in minutes: ")

        message = f"add_item|{item_name}|{item_description}|{starting_bid}|{auction_duration}"
        self.request_to_server(message, client_socket)
        reply = self.response_from_server(client_socket)
        print(reply)

    def place_bid(self, client_socket):
        username = input("Enter your username: ")
        item_name = input("Enter the item name to bid on: ")
        bid_amount = input("Enter your bid amount: ")

        message = f"bid|{username}|{item_name}|{bid_amount}"
        self.request_to_server(message, client_socket)
        reply = self.response_from_server(client_socket)
        print(reply)

    def view_items(self, client_socket):
        message = "view_items"
        self.request_to_server(message, client_socket)
        reply = self.response_from_server(client_socket)
        print(reply)


if __name__ == "__main__":
    auction_client = Auction_client()
    auction_client.client_menu()
