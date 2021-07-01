import socket               # Import socket module
import time

client = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name e.g. SamWorkstation
port = 25520                # Reserve a port for your service.

client.connect((host, port))
recievedData=client.recv(1024).decode()
print(recievedData)
client.close                     # Close the socket when done
time.sleep(10)