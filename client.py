import socket #import for socket
import re #import for regular expressions
from datetime import datetime
class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        
    def connect_to_server(self):
        try:
            client_socket:socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip, self.port))
            client_socket.send(bytes("Hello!!", "utf-8"))
            recv = client_socket.recv(1024).decode()
            print(recv)
            #program started
            program:Program = Program(client_socket)
            program.menu()
        except Exception as err:
            print(err)

class User:
    def __init__(self, username:str, password:str, email:str, phone:str):
        # User initialization with validation and loading from a file
        self.username:str = username
        self.password:str = password
        self.email:str = self.validate_email(email)
        self.phone:str = self.validate_phone(phone)
        self.users:list = []
   
    def validate_email(self, email:str):
            # Validate email format
            email_pattern = r'^\S+@\S+\.\S+$'
            if re.match(email_pattern, email):
                return email
            else:
                return -1

    def validate_phone(self, phone:str):
            # Validate phone number format (numeric characters only)
            phone_pattern = r'^[0-9]+$'
            if re.match(phone_pattern, phone):
                return phone
            else:
                return -1

class Auction:
    def __init__(self,title:str,description:str,end_time:str):
        self.title: str = title
        self.description: str = description
        self.end_time: str = self.validate_date(end_time)

    def validate_date(self, date: str):
        # Validate date format
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
        if date_pattern.match(date):
            return date
        else:
            return None
class Program:
    def __init__(self,client_socket:socket):
        self.client_socket: socket = client_socket

    def menu(self):
        # Main menu for user interaction
        try:
            option:str= input("\n1: Register\n2: Auction\n3: Bid\n4: Exit\n")
            self.client_socket.send(bytes(option,'utf-8'))
            if option == '1':
                self.register_user()
            elif option == '2':
                self.create_auction()
            elif option == '3':
                self.place_bid()
            elif option == '4':
                print("\nGoodbye!")
                exit()
            else:
                print("\nInvalid option. Please try again.")
        except Exception as err:
                print(err)
                self.menu()

    def register_user(self):
        # User registration process
        username:str = input("\nEnter username: ")
        password:str = input("Enter password: ")
        email:str = input("Enter email: ")
        phone:str = input("Enter phone number: ")

        #validate email and phone number
        user: User = User(username, password, email, phone)
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
            self.client_socket.send(bytes(username+'||'+password+'||'+email+'||'+phone,'utf-8'))
            reply = self.client_socket.recv(1024).decode()
            print(reply)
            self.menu()

    def create_auction(self):
        title:str = input("Enter auction title: ")
        description:str = input("Enter auction description: ")
        end_time:str = input("Enter auction end time (YYYY-MM-DD HH:MM:SS): ")

        auction: Auction = Auction(title,description,end_time)
        current_time: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#generating curren_time
        if auction.end_time is None:
            print("\nInvalid Date-Time Format!!")
            self.menu()
        # Comparing Time
        elif datetime.strptime(auction.end_time,'%Y-%m-%d %H:%M:%S') <= datetime.strptime(current_time,'%Y-%m-%d %H:%M:%S'):
            print("\nInvalid Time!!")
            self.menu()
        else:
            self.client_socket.send(bytes(title+'||'+description+'||'+end_time,'utf-8'))
            reply = self.client_socket.recv(1024).decode()
            print(reply)
            self.menu()


    def place_bid(self):
        # Placeholder for bid placement logic
        pass
        
        
if __name__ == '__main__':
    client: Client = Client('localhost',8888)
    client.connect_to_server()