import socket               # Import socket module
import random
import threading
import time

clientObj = socket.socket()       # Create a socket object
host = socket.gethostname() # Get local machine name e.g. SamWorkstation
port = 25520                # Reserve a port for your service.

clientObj.connect((host, port))
username=str(host+' #'+str(random.randint(100000,999999)))
clientObj.send(username.encode())
welcomeMessage=clientObj.recv(65536).decode()
print(welcomeMessage)
def CheckForUpdate(client,username):
    while True:
        welcome=client.recv(65536).decode()
        print(welcome)
    return

print('Connection started at ',round(time.time()))
while True:
    threading.Thread(target=CheckForUpdate,args=(clientObj,username),daemon=True).start()
    data=input("CHAT: ")
    clientObj.send(data.encode())

clientObj.close                     # Close the socket when done
