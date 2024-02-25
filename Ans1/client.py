import socket
import pickle
import os

class FileClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_file(self, file_path):
        if not os.path.exists(file_path):
            print("File does not exist.")
            return
        try:
            with open(file_path, 'rb') as file_to_send:
                file_data = file_to_send.read()
            file_obj = {'filename': os.path.basename(file_path), 'filedata': file_data}
            pickled_file_obj = pickle.dumps(file_obj)
            self.sock.connect((self.server_host, self.server_port))
            self.sock.sendall(pickled_file_obj)
            print(f"File {os.path.basename(file_path)} has been sent successfully.")
        except (socket.error, IOError, pickle.PicklingError) as e:
            print(f"Error sending file: {e}")
        finally:
            self.sock.close()
