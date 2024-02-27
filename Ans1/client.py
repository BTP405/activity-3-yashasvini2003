import socket
import pickle
import os


class FileClient:
    def __init__(self, server_host, server_port):
        """
        Initialize the FileClient object.

        Parameters:
            server_host (str): The hostname or IP address of the server.
            server_port (int): The port number the server is listening on.
        """
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_file(self, file_path):
        """
        Send a file to the server.

        Parameters:
            file_path (str): The path to the file to be sent.
        """
        # Check if the file exists
        if not os.path.exists(file_path):
            print("File does not exist.")
            return
        try:
            # Read the file as binary data
            with open(file_path, 'rb') as file_to_send:
                file_data = file_to_send.read()
            # Create a dictionary object containing filename and file data
            file_obj = {'filename': os.path.basename(file_path), 'filedata': file_data}
            # Serialize the file object using pickle
            pickled_file_obj = pickle.dumps(file_obj)
            # Connect to the server
            self.sock.connect((self.server_host, self.server_port))
            # Send the serialized file object
            self.sock.sendall(pickled_file_obj)
            print(f"File {os.path.basename(file_path)} has been sent successfully.")
        except (socket.error, IOError, pickle.PicklingError) as e:
            # Handle errors that may occur during file sending
            print(f"Error sending file: {e}")
        finally:
            # Close the socket
            self.sock.close() 
