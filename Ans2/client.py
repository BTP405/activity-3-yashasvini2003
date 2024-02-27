import socket
from common import serialize, deserialize  # Import functions for serialization

def receive_complete_message(sock):
    """
    Receive a complete message from a socket.

    Parameters:
        sock (socket.socket): The socket object to receive data from.

    Returns:
        bytes: The complete message received from the socket.
    """
    data = b''
    while True:
        part = sock.recv(4096)
        data += part
        if len(part) < 4096:  # Check if the received part is the last part of the message
            break
    return data

class TaskClient:
    def __init__(self, worker_addresses):
        self.worker_addresses = worker_addresses

    def send_task(self, func_name, *args):
        """
        Send a task to available worker nodes and retrieve the result.

        Parameters:
            func_name (str): The name of the function to execute on the worker node.
            *args: Arguments to be passed to the function.

        Returns:
            Any: The result returned by the worker node after executing the task.
        """
        task_data = serialize((func_name, args))  # Serialize the task data
        for address in self.worker_addresses:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(10)  # Set a timeout for socket operations
                    s.connect(address)
                    s.sendall(task_data)
                    response = receive_complete_message(s)  # Receive the response from the worker
                    return deserialize(response)  # Deserialize and return the response
            except socket.timeout:
                print(f"Connection timed out with {address}")
            except socket.error as e:
                print(f"Connection error with {address}: {e}")
        raise Exception("Failed to send task to any worker.")  # Raise an exception if task sending fails

if __name__ == "__main__":
    # Initialize the client with worker addresses
    client = TaskClient([('localhost', 5001)])
    # Send tasks and print the results
    result = client.send_task('add', 5, 7)
    print(f"Result: {result}")
    result = client.send_task('multiply', 4, 9)
    print(f"Result: {result}")
