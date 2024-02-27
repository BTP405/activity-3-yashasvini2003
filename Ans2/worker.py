import socket
from common import serialize, deserialize
import task  # Import the module containing task functions

def handle_client(conn):
    """
    Handle a client connection by receiving and executing a task.

    Parameters:
        conn (socket.socket): The socket object representing the client connection.
    """
    try:
        # Set a timeout for operations on this specific connection
        conn.settimeout(10)  # Set a 10-second timeout for this connection
        
        task_data = conn.recv(4096)  # Receive task data from the client
        func_name, args = deserialize(task_data)  # Deserialize the task data
        func = getattr(task, func_name, None)  # Get the function by name
        if func:
            result = func(*args)  # Execute the function with provided arguments
            print(f'Task {func_name} with args {args} returned {result}')
            conn.sendall(serialize(result))  # Serialize and send the result back to the client
        else:
            raise ValueError(f"Function {func_name} not found")
    except socket.timeout:
        print("Timed out waiting for data from client")
    except Exception as e:
        error_message = f"Error: {e}"
        conn.sendall(serialize(error_message))  # Serialize and send error message to client
        print(error_message)
    finally:
        conn.close()  # Close the connection

def worker_node(port):
    """
    Start a worker node that listens for client connections and handles tasks.

    Parameters:
        port (int): The port number on which the worker node will listen for connections.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', port))  # Bind the socket to localhost and the specified port
        s.listen()
        print(f"Worker listening on port {port}")
        while True:
            conn, addr = s.accept()  # Accept incoming connection
            with conn:
                print(f"Connected by {addr}")
                handle_client(conn)  # Handle the client connection

if __name__ == "__main__":
    # Start the worker node on port 5001
    worker_node(5001)
