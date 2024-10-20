import socket

class OB_Server:
    def __init__(self):
        self.server_ip = "localhost"
        self.server_port = 9090

    def start_server(self):
        ob_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ob_server.bind((self.server_ip, self.server_port))
        ob_server.listen()
        print(f"OB Server listening on {self.server_ip}:{self.server_port}")

        try:
            while True:
                client_socket, address = ob_server.accept()
                with client_socket:
                    print(f"Connection from {address}")
                    self.handle_client(client_socket)
        except Exception as e:
            print(f"Error in OB server: {e}")

    def handle_client(self, client_socket):
        try:
            message = client_socket.recv(4096).decode("utf-8")
            if message:
                print(f"Bidding update received: {message}")
        except Exception as e:
            print(f"Error handling client: {e}")

if __name__ == "__main__":
    ob_server = OB_Server()
    ob_server.start_server()
