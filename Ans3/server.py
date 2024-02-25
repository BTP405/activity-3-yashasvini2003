import socket
import threading
import pickle


class ChatServer:
    def __init__(self, host='127.0.0.1', port=9000):
        self.clients = []
        self.clients_lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print(f"Server is listening at {host}:{port}")

    def broadcast(self, message):
        with self.clients_lock:
            for client in self.clients:
                client.send(message)

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024)
                self.broadcast(message)
            except:
                with self.clients_lock:
                    self.clients.remove(client_socket)
                client_socket.close()
                break

    def accept_connections(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            with self.clients_lock:
                self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    server = ChatServer()
    accept_thread = threading.Thread(target=server.accept_connections)
    accept_thread.start()
    accept_thread.join()