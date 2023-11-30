import socket #import for socket

class Server:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port 
        #using User class
        #user db automatically loaded
        self.user = User()
        
    def start(self):
        server_socket:socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        server_socket.listen()
        print("server is listen on {}:{}".format(self.ip, self.port))

        while True:
            try:
                client, address = server_socket.accept()
                print("Client {}:{} is connected".format(address[0], address[1]))
                self.client_hadling(client)
            except Exception as err:
                print(err)
             
    def client_hadling(self, client_socket):
        with client_socket as sock:
            recv = sock.recv(1024).decode()
            if recv == 'Hello!!':
                sock.send(bytes("Welcome To Auction!!", "utf-8"))

                while True:         
                    option = sock.recv(1024).decode()
                    if option == '1':
                        username,password,email,phone = sock.recv(1024).decode().split('||')
                        #temp_db to store recently regirstered user's data
                        temp_db: dict = {
                            "username": username,
                            "password": password,
                            "email": email,
                            "phone": phone
                            }
                        self.user.users.append(temp_db)#appending temp_db to users
                        self.user.db_saving()#saving users to database

                        sock.send(bytes("\nUser Registered Successfully!!","utf-8"))
                        continue
                    elif option == '2':
                        pass
                    elif option == '3':
                        pass                        
                    
class User:
    def __init__(self):
        # User initialization with validation and loading from a file
        self.users:list = []
        self.db_loading()

    def db_loading(self):
            # Load user data from a file
            try:
                with open("Users.txt", "r") as file:
                    users_data: list = file.readlines()
                    for user in users_data:
                        temp_user:list= user.split('||')
                        temp_dict:dict = {
                            'username': temp_user[0],
                            'password':temp_user[1],
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
                        file.write(self.users[i]['username']+'||'+self.users[i]['password']+'||'+self.users[i]['email']+'||'+self.users[i]['phone']+'\n')
            except Exception as err:
                print(err)   

if __name__ == '__main__':
    server: Server = Server('localhost',8080)
    server.start()