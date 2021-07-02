import socket               # Import socket module
import threading

def NewServer():
    server = socket.socket()         #creates a server
    host = socket.gethostname() #gets the name of the computer running the server
    port = 25520
    server.bind((host, port))      #opens the specified port for the specified hostname
    return server

def ClientInstance(IP,port,socketClientObject,userNumber):
    username=socketClientObject.recv(65536).decode()
    print(username)
    connectionMessage=str('You have successfully connected, '+username)
    socketClientObject.send(connectionMessage.encode())
    rData=''
    while rData!='-END':
        rData=socketClientObject.recv(65536).decode()
        sData=str(username+': '+rData)
        #give rData to an external container that can communicate with the other clients, then have every client update from the container.
        socketClientObject.send(sData.encode())
    return


server=NewServer()
userDB={}
while True:
    print('listening')
    server.listen()
    clientObj, (clientIP,clientPort) = server.accept()
    if clientObj not in userDB:
        threading.Thread(target=ClientInstance,args=(clientIP,clientPort,clientObj,len(userDB)),daemon=True).start()
        userDB.update({len(userDB):clientObj})
