from server import FileServer

server = FileServer('localhost', 12345, 'received_files')
server.run()