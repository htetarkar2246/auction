import socket  # import for socket


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

                while True:
                    option = sock.recv(1024).decode()
                    if option == '1':
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
                        continue
                    elif option == '2':
                        title, description, end_time = sock.recv(1024).decode().split('||')
                        # temp_db to store recently created auction data
                        auction_id: int = len(self.auction.auctions)+1
                        temp_db: dict = {
                            "id": str(auction_id),
                            "title": title,
                            "description": description,
                            "end_time": end_time
                        }
                        self.auction.auctions.append(temp_db)  # appending temp_db to auctions
                        self.auction.db_saving()  # saving auctions to database

                        sock.send(bytes("\nAuction Created Successfully!!", "utf-8"))
                        continue
                    elif option == '3':
                        pass


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
                        'end_time': temp_auction[3][:-1],
                    }
                    self.auctions.append(temp_dict)
        except Exception as err:
            print(err)

    def db_saving(self):
        # Save user data to a file
        try:
            with open("Auctions.txt", "w") as file:
                for i in range(len(self.auctions)):
                    file.write(self.auctions[i]['id'] + '||' + self.auctions[i]['title'] + '||' + self.auctions[i][
                        'description'] + '||' + self.auctions[i]['end_time'] + '\n')
        except Exception as err:
            print(err)


if __name__ == '__main__':
    server: Server = Server('localhost', 8888)
    server.start()
