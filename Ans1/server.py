import socket
import pickle
import os

class FileServer:
    def __init__(self, host, port, save_dir):
        self.host = host
        self.port = port
        self.save_dir = save_dir
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def receive_file(self):
        client_socket, address = self.sock.accept()
        print(f"Connection from {address} has been established.")
        received_data = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet: break
            received_data += packet
        try:
            file_obj = pickle.loads(received_data)
            file_path = os.path.join(self.save_dir, file_obj['filename'])
            with open(file_path, 'wb') as file_to_write:
                file_to_write.write(file_obj['filedata'])
            print(f"File {file_obj['filename']} has been saved successfully.")

        except (pickle.UnpicklingError, KeyError, IOError) as e:
            print(f"Error saving file: {e}")
        finally:
            client_socket.close()

    def run(self):
        try:
            while True:
                self.receive_file()
        except KeyboardInterrupt:
            print("Server is shutting down.")
        finally:
            self.sock.close()

