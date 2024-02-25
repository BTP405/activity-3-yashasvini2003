from client import FileClient

client = FileClient('localhost', 12345)

file_path = input("Enter the file path to send: ")
client.send_file(file_path)


