# worker.py
import socket
from common import serialize, deserialize
import task

def handle_client(conn):
    try:
        # Set a timeout for operations on this specific connection
        conn.settimeout(10)  # Set a 10-second timeout for this connection
        
        task_data = conn.recv(4096)
        func_name, args = deserialize(task_data)
        func = getattr(task, func_name, None)
        if func:
            result = func(*args)
            print(f'Task {func_name} with args {args} returned {result}')
            conn.sendall(serialize(result))
        else:
            raise ValueError(f"Function {func_name} not found")
    except socket.timeout:
        print("Timed out waiting for data from client")
    except Exception as e:
        error_message = f"Error: {e}"
        conn.sendall(serialize(error_message))
        print(error_message)
    finally:
        conn.close()

def worker_node(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', port))
        s.listen()
        print(f"Worker listening on port {port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                handle_client(conn)

if __name__ == "__main__":
    worker_node(5001)
