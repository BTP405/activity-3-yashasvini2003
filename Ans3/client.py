import socket
import threading
import pickle
import random

class ChatClient:
    def __init__(self, host='127.0.0.1', port=9000, name=input("Enter your name: ")):
        """
        Initialize the ChatClient object.

        Parameters:
            host (str): The IP address or hostname of the server. Default is '127.0.0.1'.
            port (int): The port number to connect to. Default is 9000.
            name (str): The name of the client in the chat. Prompted to the user.
        """
        # Create a TCP socket for client-server communication
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        self.client_socket.connect((host, port))
        # Set the name of the client
        self.name = name
        print(f"Connected to {host}:{port}")
        # Send a message indicating client has joined the chat
        self.client_socket.send(pickle.dumps(f"{self.name} has joined the chat."))

    def send_message(self):
        """
        Continuously send messages typed by the user to the server.
        """
        while True:
            try:
                user_input = input("")
                message = f"{self.name}: {user_input}"
                pickled_message = pickle.dumps(message)
                self.client_socket.send(pickled_message)
            except:
                # If an exception occurs (e.g., client leaves), send a message and close the socket
                message = f"{self.name} has left the chat."
                pickled_message = pickle.dumps(message)
                self.client_socket.send(pickled_message)
                self.client_socket.close()
                break
            

    def receive_message(self):
        """
        Continuously receive messages from the server and print them to the client's console.
        """
        while True:
            try:
                message = self.client_socket.recv(1024)
                response = pickle.loads(message)
                if response:
                    if response.startswith(self.name):
                        continue  # Skip printing own messages
                    else:
                        print(response)
            except:
                # If an exception occurs (e.g., client leaves), close the socket
                self.client_socket.close()
                break

    def run(self):
        """
        Start threads for sending and receiving messages.
        """
        threading.Thread(target=self.receive_message).start()
        self.send_message()

if __name__ == "__main__":
    # Initialize and run the chat client
    client = ChatClient()
    client.run()
