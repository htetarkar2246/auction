import socket #import for socket

class Server:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

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
            #     option = sock.recv(1024).decode()
            #     if option == 1:
            #         self.registeration(sock)
                    

if __name__ == '__main__':
    server: Server = Server('localhost',8080)
    server.start()