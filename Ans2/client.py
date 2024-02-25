# client.py
import socket
from common import serialize, deserialize

def receive_complete_message(sock):
    data = b''
    while True:
        part = sock.recv(4096)
        data += part
        if len(part) < 4096:  # Assuming this is the end of the message
            break
    return data

class TaskClient:
    def __init__(self, worker_addresses):
        self.worker_addresses = worker_addresses

    def send_task(self, func_name, *args):
        task_data = serialize((func_name, args))
        for address in self.worker_addresses:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(10)  # Correctly set timeout here
                    s.connect(address)
                    s.sendall(task_data)
                    response = receive_complete_message(s)  # Use the new function
                    return deserialize(response)
            except socket.timeout:
                print(f"Connection timed out with {address}")
            except socket.error as e:
                print(f"Connection error with {address}: {e}")
        raise Exception("Failed to send task to any worker.")

if __name__ == "__main__":
    client = TaskClient([('localhost', 5001)])
    result = client.send_task('add', 5, 7)
    print(f"Result: {result}")
    result = client.send_task('multiply', 4, 9)
    print(f"Result: {result}")
