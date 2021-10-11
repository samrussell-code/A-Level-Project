import socket               # Import socket module
import random
import threading
import time

clientObj = socket.socket()       # Create a socket object
clientName = socket.gethostname() # Get local machine name e.g. SamWorkstation
port = 25520                # Reserve a port for your service.

hostname=str(input('Enter password:'))
clientObj.connect((hostname, port))
username=str(clientName+' #'+str(random.randint(100000,999999)))
clientObj.send(username.encode())
welcomeMessage=clientObj.recv(65536).decode()
print(welcomeMessage)


def CheckForUpdate(client,username): #waits to recieve information from the server - always called in the background.
    while True:
        recievedMessage=client.recv(65536).decode()
        print(recievedMessage)
    return

print('Connection started at ',round(time.time()))
while True:
    threading.Thread(target=CheckForUpdate,args=(clientObj,username),daemon=True).start()
    data=input("CHAT: ")
    clientObj.send(data.encode())

clientObj.close                     # Close the socket when done
