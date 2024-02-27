import socket
import threading
import pickle

class ChatServer:
    def __init__(self, host='127.0.0.1', port=9000):
        """
        Initialize the ChatServer object.

        Parameters:
            host (str): The IP address or hostname to bind the server socket. Default is '127.0.0.1'.
            port (int): The port number to listen on. Default is 9000.
        """
        # List to store client sockets
        self.clients = []
        # Lock for thread-safe access to the clients list
        self.clients_lock = threading.Lock()
        # Create a TCP socket for server-client communication
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the specified host and port
        self.server_socket.bind((host, port))
        # Start listening for incoming connections
        self.server_socket.listen()
        print(f"Server is listening at {host}:{port}")

    def broadcast(self, message):
        """
        Broadcast a message to all connected clients.

        Parameters:
            message (bytes): The message to broadcast.
        """
        with self.clients_lock:
            for client in self.clients:
                client.send(message)

    def handle_client(self, client_socket):
        """
        Handle messages from a specific client.

        Parameters:
            client_socket (socket.socket): The socket object representing the client.
        """
        while True:
            try:
                message = client_socket.recv(1024)
                self.broadcast(message)
            except:
                # If an exception occurs (e.g., client leaves), remove the client and close the socket
                with self.clients_lock:
                    self.clients.remove(client_socket)
                client_socket.close()
                break

    def accept_connections(self):
        """
        Accept incoming client connections and handle them in separate threads.
        """
        while True:
            client_socket, _ = self.server_socket.accept()
            with self.clients_lock:
                self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    # Initialize and start the chat server
    server = ChatServer()
    accept_thread = threading.Thread(target=server.accept_connections)
    accept_thread.start()
    accept_thread.join()
