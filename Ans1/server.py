import socket
import pickle
import os

class FileServer:
    def __init__(self, host, port, save_dir):
        """
        Initialize the FileServer object.

        Parameters:
            host (str): The hostname or IP address of the server.
            port (int): The port number the server will listen on.
            save_dir (str): The directory where received files will be saved.
        """
        self.host = host
        self.port = port
        self.save_dir = save_dir
        # Create a TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the specified host and port
        self.sock.bind((self.host, self.port))
        # Listen for incoming connections
        self.sock.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def receive_file(self):
        """
        Receive a file from a client.
        """
        # Accept incoming connection
        client_socket, address = self.sock.accept()
        print(f"Connection from {address} has been established.")
        received_data = b""
        # Receive data in chunks until the entire file is received
        while True:
            packet = client_socket.recv(4096)
            if not packet: break
            received_data += packet
        try:
            # Deserialize the received data using pickle
            file_obj = pickle.loads(received_data)
            # Construct the file path
            file_path = os.path.join(self.save_dir, file_obj['filename'])
            # Write the received file data to disk
            with open(file_path, 'wb') as file_to_write:
                file_to_write.write(file_obj['filedata'])
            print(f"File {file_obj['filename']} has been saved successfully.")

        except (pickle.UnpicklingError, KeyError, IOError) as e:
            # Handle errors that may occur during file receiving and saving
            print(f"Error saving file: {e}")
        finally:
            # Close the client socket
            client_socket.close()

    def run(self):
        """
        Start the server and continuously receive files from clients.
        """
        try:
            while True:
                self.receive_file()
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt to gracefully shut down the server
            print("Server is shutting down.")
        finally:
            # Close the server socket
            self.sock.close()
