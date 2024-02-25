import socket
import threading
import pickle
import random

class ChatClient:
    def __init__(self, host='127.0.0.1', port=9000, name=input("Enter your name: ")):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.name = name
        print(f"Connected to {host}:{port}")
        self.client_socket.send(pickle.dumps(f"{self.name} has joined the chat."))

    def send_message(self):
        while True:
            try:
                user_input = input("")
                message = f"{self.name}: {user_input}"
                pickled_message = pickle.dumps(message)
                self.client_socket.send(pickled_message)
            except:
                message = f"{self.name} has left the chat."
                pickled_message = pickle.dumps(message)
                self.client_socket.send(pickled_message)
                self.client_socket.close()
                break
            

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024)
                response = pickle.loads(message)
                if response:
                    if response.startswith(self.name):
                        continue
                    else:
                        print(response)
            except:
                self.client_socket.close()
                break

    def run(self):
        threading.Thread(target=self.receive_message).start()
        self.send_message()

if __name__ == "__main__":
    client = ChatClient()
    client.run()

