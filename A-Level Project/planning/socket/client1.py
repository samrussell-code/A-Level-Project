import socket               # Import socket module
import time

clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name e.g. SamWorkstation
port = 25520                # Reserve a port for your service.

clientObj.connect((host, port))
recievedData=clientObj.recv(65536).decode()
print(recievedData)
while True:
    data=input("CHAT: ")
    clientObj.send(data.encode())
    print(clientObj.recv(65536).decode())
clientObj.close                     # Close the socket when done
