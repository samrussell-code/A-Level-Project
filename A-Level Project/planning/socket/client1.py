import socket               # Import socket module
import random

clientObj = socket.socket()       # Create a socket object
host = socket.gethostname() # Get local machine name e.g. SamWorkstation
port = 25520                # Reserve a port for your service.

clientObj.connect((host, port))
username=str(host+' #'+str(random.randint(100000,999999)))
clientObj.send(username.encode())
welcomeMessage=clientObj.recv(65536).decode()
print(welcomeMessage)
while True:
    data=input("CHAT: ")
    clientObj.send(data.encode())
    print(clientObj.recv(65536).decode())
clientObj.close                     # Close the socket when done
