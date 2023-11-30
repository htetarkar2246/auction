import socket #import for socket

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
        except Exception as err:
            print(err)
            
if __name__ == '__main__':
    client:Client = Client('localhost',8080)
    client.connect_to_server()