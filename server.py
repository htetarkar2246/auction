import socket  # import for socket
import re  # import for regular expressions
import json
from datetime import datetime


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        # using User class
        # user db automatically loaded
        self.user: User = User()
        # using Auction class
        # auction db automatically loaded
        self.auction: Auction = Auction()
        # using Bid class
        # auction db automatically loaded
        self.bid: Bid = Bid()
        # variable for logged user
        self.log_user_id: int = -1

    def start(self):
        server_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        server_socket.listen()
        print("server is listen on {}:{}".format(self.ip, self.port))

        while True:
            try:
                client, address = server_socket.accept()
                print("Client {}:{} is connected".format(address[0], address[1]))
                self.client_handling(client)
            except Exception as err:
                print(err)

    def client_handling(self, client_socket):
        with client_socket as sock:
            recv = sock.recv(1024).decode()
            if recv == 'Hello!!':
                sock.send(bytes("Welcome To Auction!!", "utf-8"))
                self.menu(sock)

    def menu(self, sock):
        option = sock.recv(1024).decode()
        if option == '1':
            self.register(sock)
        elif option == '2':
            self.login(sock)

    def sec_menu(self, sock):
        option = sock.recv(1024).decode()
        if option == '1':
            self.create_auction(sock)
        elif option == '2':
            auction_id, bid_amount = sock.recv(1024).decode().split('||')
            for i in range(len(self.auction.auctions)):
                if self.auction.auctions[i]['id'] == int(auction_id):
                    if self.auction.auctions[i]['highest_price'] < int(bid_amount):
                        self.auction.auctions[i]['highest_price'] = int(bid_amount)
                        auction: json = json.dumps(self.auction.auctions[i])
                        sock.send(bytes(auction, 'utf-8'))
                        self.auction.db_saving()
                        temp_db: dict = {
                            'auction_id': self.auction.auctions[i]['id'],
                            'user': self.user.users[self.log_user_id]['username'],
                            'bid_amount': self.auction.auctions[i]['highest_price'],
                            'bid_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        self.bid.bids.append(temp_db)
                        self.bid.db_saving()
                        self.sec_menu(sock)
        elif option == '3':
            auctions: json = json.dumps(self.auction.auctions)
            sock.send(bytes(auctions, 'utf-8'))
            self.sec_menu(sock)
        elif option == '4':
            auction_id = sock.recv(1024).decode()
            to_send_bids: list = []
            for bid in self.bid.bids:
                if bid['auction_id'] == int(auction_id):
                    to_send_bids.append(bid)
                else:
                    continue
            json_bids: json = json.dumps(to_send_bids)
            sock.send(bytes(json_bids, 'utf-8'))
            self.sec_menu(sock)

    def register(self, sock):
        username, password, email, phone = sock.recv(1024).decode().split('||')
        # temp_db to store recently registered user's data
        temp_db: dict = {
            "username": username,
            "password": password,
            "email": email,
            "phone": phone
        }
        self.user.users.append(temp_db)  # appending temp_db to users
        self.user.db_saving()  # saving users to database

        sock.send(bytes("\nUser Registered Successfully!!", "utf-8"))
        self.menu(sock)

    def login(self, sock):
        option = sock.recv(1024).decode()
        if option == '1':
            email, password = sock.recv(1024).decode().split('||')
            check: int = -1
            for i in range(len(self.user.users)):
                if self.user.users[i]['email'] == email:
                    if self.user.users[i]['password'] == password:
                        check = 0
                        self.log_user_id = i
                    else:
                        check = 1
                else:
                    check = 2
            if check == 0:
                sock.send(bytes('\nWelcome User' + self.user.users[self.log_user_id]['username'], 'utf-8'))
                self.sec_menu(sock)
            elif check == 1:
                sock.send(bytes('\nIncorrect Password!!', 'utf-8'))
                self.login(sock)
            elif check == 2:
                sock.send(bytes('\nEmail Cannot Be Found!!', 'utf-8'))
                self.login(sock)
        elif option == '2':
            phone, password = sock.recv(1024).decode().split('||')
            check: int = -1
            for i in range(len(self.user.users)):
                if self.user.users[i]['phone'] == phone:
                    if self.user.users[i]['password'] == password:
                        check = 0
                        self.log_user_id = i
                    else:
                        check = 1
                else:
                    check = 2
            if check == 0:
                sock.send(bytes('\nWelcome User ' + self.user.users[self.log_user_id]['username'], 'utf-8'))
                self.sec_menu(sock)
            elif check == 1:
                sock.send(bytes('\nIncorrect Password!!', 'utf-8'))
                self.login(sock)
            elif check == 2:
                sock.send(bytes('\nPhone Cannot Be Found!!', 'utf-8'))
                self.login(sock)
        elif option == '3':
            self.menu(sock)

    def create_auction(self, sock):
        title, description, end_time, price = sock.recv(1024).decode().split('||')
        # temp_db to store recently created auction data
        auction_id: int = len(self.auction.auctions) + 1
        temp_db: dict = {
            "id": auction_id,
            "title": title,
            "description": description,
            "end_time": end_time,
            "price": int(price),
            "highest_price": int(price)
        }
        self.auction.auctions.append(temp_db)  # appending temp_db to auctions
        self.auction.db_saving()  # saving auctions to database

        sock.send(bytes("\nAuction Created Successfully!!", "utf-8"))
        self.sec_menu(sock)


class User:
    def __init__(self):
        # User initialization with validation and loading from a file
        self.users: list = []
        self.db_loading()

    def db_loading(self):
        # Load user data from a file
        try:
            with open("Users.txt", "r") as file:
                users_data: list = file.readlines()
                for user in users_data:
                    temp_user: list = user.split('||')
                    temp_dict: dict = {
                        'username': temp_user[0],
                        'password': temp_user[1],
                        'email': temp_user[2],
                        'phone': temp_user[3][:-1],
                    }
                    self.users.append(temp_dict)
        except Exception as err:
            print(err)

    def db_saving(self):
        # Save user data to a file
        try:
            with open("Users.txt", "w") as file:
                for i in range(len(self.users)):
                    file.write(self.users[i]['username'] + '||' + self.users[i]['password'] + '||' + self.users[i][
                        'email'] + '||' + self.users[i]['phone'] + '\n')
        except Exception as err:
            print(err)



class Auction:
    def __init__(self):
        # Auction loading from a file
        self.auctions: list = []
        self.db_loading()

    def db_loading(self):
        # Load user data from a file
        try:
            with open("Auctions.txt", "r") as file:
                auctions_data: list = file.readlines()
                for auction in auctions_data:
                    temp_auction: list = auction.split('||')
                    temp_dict: dict = {
                        'id': int(temp_auction[0]),
                        'title': temp_auction[1],
                        'description': temp_auction[2],
                        'end_time': temp_auction[3],
                        "price": int(temp_auction[4]),
                        "highest_price": int(temp_auction[5][:-1]),
                    }
                    self.auctions.append(temp_dict)
        except Exception as err:
            print(err)

    def db_saving(self):
        # Save user data to a file
        try:
            with open("Auctions.txt", "w") as file:
                for i in range(len(self.auctions)):
                    file.write(str(self.auctions[i]['id']) + '||' + self.auctions[i]['title'] + '||' + self.auctions[i][
                        'description'] + '||' + self.auctions[i]['end_time'] + '||'
                               + str(self.auctions[i]['price']) + '||' + str(self.auctions
                                                                             [i]['highest_price']) + '\n')
        except Exception as err:
            print(err)


class Bid:
    def __init__(self):
        # db of bids
        self.bids: list = []
        self.db_loading()

    def db_loading(self):
        # Load user data from a file
        try:
            with open("Bids.txt", "r") as file:
                bids_data: list = file.readlines()
                for bid in bids_data:
                    temp_bid: list = bid.split('||')
                    temp_dict: dict = {
                        'auction_id': int(temp_bid[0]),
                        'user': temp_bid[1],
                        'bid_amount': int(temp_bid[2]),
                        'bid_time': temp_bid[3][:-1]
                    }
                    self.bids.append(temp_dict)
        except Exception as err:
            print(err)

    def db_saving(self):
        # Save user data to a file
        try:
            with open("Bids.txt", "w") as file:
                for i in range(len(self.bids)):
                    file.write(str(self.bids[i]['auction_id']) + '||' + self.bids[i]['user'] + '||' + str(self.bids[i][
                        'bid_amount']) + '||' + self.bids[i][
                        'bid_time'] + '\n')
        except Exception as err:
            print(err)


if __name__ == '__main__':
    server: Server = Server('localhost', 8888)
    server.start()
