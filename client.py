import socket  # import for socket
import re  # import for regular expressions
from datetime import datetime
import json


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect_to_server(self):
        try:
            client_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip, self.port))
            client_socket.send(bytes("Hello!!", "utf-8"))
            recv = client_socket.recv(1024).decode()
            print(recv)
            # program started
            program: Program = Program(client_socket)
            program.menu()
        except Exception as err:
            print(err)


def validate_email(email: str):
    # Validate email format
    email_pattern = r'^\S+@\S+\.\S+$'
    if re.match(email_pattern, email):
        return email
    else:
        return -1


def validate_phone(phone: str):
    # Validate phone number format (numeric characters only)
    phone_pattern = r'^[0-9]+$'
    if re.match(phone_pattern, phone):
        return phone
    else:
        return -1


class User:
    def __init__(self, username: str, password: str, email: str, phone: str):
        # User initialization with validation and loading from a file
        self.username: str = username
        self.password: str = password
        self.email: str = validate_email(email)
        self.phone: str = validate_phone(phone)
        self.users: list = []


def validate_date(date: str):
    # Validate date format
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    if date_pattern.match(date):
        return date
    else:
        return None


class Auction:
    def __init__(self, title: str, description: str, end_time: str):
        self.title: str = title
        self.description: str = description
        self.end_time: str = validate_date(end_time)


class Program:
    def __init__(self, client_socket: socket):
        self.client_socket: socket = client_socket

    def menu(self):
        # Main menu for user interaction
        try:
            option: str = input("\n1: Register\n2: Login\n3: Exit\n")
            self.client_socket.send(bytes(option, 'utf-8'))
            if option == '1':
                self.register_user()
            elif option == '2':
                self.login()
            elif option == '3':
                print("\nGoodbye!")
                exit()
            else:
                print("\nInvalid option. Please try again.")
                self.menu()
        except Exception as err:
            print(err)
            self.menu()

    def register_user(self):
        # User registration process
        username: str = input("\nEnter username: ")
        password: str = input("Enter password: ")
        email: str = input("Enter email: ")
        phone: str = input("Enter phone number: ")
        user: User = User(username, password, email, phone)
        # validate email and phone number
        if user.email == -1 and user.phone == -1:
            print("\nInvalid Email & Phone Number Format!!")
            self.menu()
        elif user.email == -1:
            print("\nInvalid Email Format!!")
            self.menu()
        elif user.phone == -1:
            print("\nInvalid Phone Number Format!!")
            self.menu()
        else:
            # registered user's data are sent to server
            self.client_socket.send(bytes(username + '||' + password + '||' + email + '||' + phone, 'utf-8'))
            reply = self.client_socket.recv(1024).decode()
            print(reply)
            self.menu()

    def login(self):
        try:
            option: str = input("\n1:Login with Email\n2:Login with Phone\n3:Menu\n")
            if option == '1':
                email: str = input("Enter email: ")
                password: str = input("Enter password: ")
                email: str = validate_email(email)
                if email == -1:
                    print("\nInvalided Email Format!!")
                    self.login()
                else:
                    self.client_socket.send(bytes('1', 'utf-8'))
                    self.client_socket.send(bytes(email + '||' + password, 'utf-8'))
                    reply: str = self.client_socket.recv(1024).decode()
                    print(reply)
                    if reply == '\nIncorrect Password!!' or reply == '\nEmail Cannot Be Found!!':
                        self.login()
                    else:
                        self.sec_menu()
            elif option == '2':
                phone: str = input("Enter Phone: ")
                password: str = input("Enter password: ")
                phone: str = validate_phone(phone)
                if phone == -1:
                    print("\nInvalided Phone Format!!")
                    self.login()
                else:
                    self.client_socket.send(bytes('2', 'utf-8'))
                    self.client_socket.send(bytes(phone + '||' + password, 'utf-8'))
                    reply: str = self.client_socket.recv(1024).decode()
                    print(reply)
                    if reply == '\nIncorrect Password!!' or reply == '\nEmail Cannot Be Found!!':
                        self.login()
                    else:
                        self.sec_menu()
            elif option == '3':
                self.menu()
            else:
                print("\nUnknown Input!!")
                self.login()
        except Exception as err:
            print(err)
            self.login()

    def create_auction(self):
        title: str = input("Enter auction title: ")
        description: str = input("Enter auction description: ")
        price: int = int(input("Enter Start Price (MMK): "))
        end_time: str = input("Enter auction end time (YYYY-MM-DD HH:MM:SS): ")

        auction: Auction = Auction(title, description, end_time)
        current_time: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # generating curren_time
        if auction.end_time is None:
            print("\nInvalid Date-Time Format!!")
            self.sec_menu()
        # Comparing Time
        elif datetime.strptime(auction.end_time, '%Y-%m-%d %H:%M:%S') <= datetime.strptime(current_time,
                                                                                           '%Y-%m-%d %H:%M:%S'):
            print("\nInvalid Time!!")
            self.sec_menu()
        else:
            self.client_socket.send(bytes(title + '||' + description + '||' + end_time + '||' + str(price), 'utf-8'))
            reply = self.client_socket.recv(1024).decode()
            print(reply)
            self.sec_menu()

    def sec_menu(self):
        try:
            option: str = input("\n1:Create Auction\n2:Bid\n3:Show Auctions\n4:History Auction\n5:Menu\n")
            self.client_socket.send(bytes(option, 'utf-8'))
            if option == '1':
                self.create_auction()
            elif option == '2':
                self.place_bid()
            elif option == '3':
                self.show_auctions()
            elif option == '4':
                self.history_auction()
            elif option == '5':
                self.menu()
        except Exception as err:
            print(err)
            self.sec_menu()

    def place_bid(self):
        try:
            auction_id: int = int(input("Enter Auction ID to Place Bid: "))
            bid_amount: int = int(input("Enter Bid Amount: "))
            self.client_socket.send(bytes(str(auction_id) + '||' + str(bid_amount), 'utf-8'))
            auction: dict = json.loads(self.client_socket.recv(1024).decode())
            print("Auction ID: ", auction['id'])
            print("Title: ", auction['title'])
            print("Description: ", auction['description'])
            print("End Time: ", auction['end_time'])
            print("Price: ", auction['price'])
            print("Highest Price: ", auction['highest_price'])
            self.sec_menu()
        except Exception as err:
            print(err)
            self.sec_menu()

    def show_auctions(self):
        auctions_json: json = self.client_socket.recv(1024).decode()
        auctions: list = json.loads(auctions_json)
        # display auctions
        for i in range(len(auctions)):
            print('\nAuction ID: '+str(auctions[i]['id']))
            print('Title: '+auctions[i]['title'])
            print('Description: '+auctions[i]['description'])
            print('End Time: '+auctions[i]['end_time'])
            print('Price:' + str(auctions[i]['price']))
            print('Highest Price:' + str(auctions[i]['highest price']))
            print('\n')
        self.sec_menu()

    def history_auction(self):
        auction_id: int = int(input("\nEnter Auction ID: "))
        self.client_socket.send(bytes(str(auction_id), 'utf-8'))
        recv_bids: list = json.loads(self.client_socket.recv(1024).decode())
        for bid in recv_bids:
            print(bid['user'], 'bid at ', bid['bid_time'], ' with amount ', bid['bid_amount'])
        self.sec_menu()


if __name__ == '__main__':
    client: Client = Client('localhost', 8888)
    client.connect_to_server()
