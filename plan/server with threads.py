import socket               # Import socket module
import threading
import time
from queue import Queue
import os

def NewServer():
    server = socket.socket()         #creates a server
    host = socket.gethostname() #gets the name of the computer running the server
    port = 25520
    server.bind((host, port))      #opens the specified port for the specified hostname
    chatlogName=str('planning/socket/data/'+'chatlog - '+str(round(time.time()))+'.txt')
    newChatLog=open(chatlogName,'w')
    newChatLog.write(str('Server started at: '+str(time.time())+'\n\n'))
    newChatLog.close()
    return server,chatlogName


class Client():
    def __init__(self,IP,port,socketClientObject,userNumber,chatlogName):
        self.StartThreads()
        self.localDB={}
        self.chatlogName=chatlogName
        self.socketClientObject=socketClientObject
    def StartThreads(self):
        threading.Thread(target=self.ClientInstance,args=(clientIP,clientPort,clientObj,len(userDB)),daemon=True).start()
    def CheckForMessages(self):
        lastLine=''
        newlastLine=''
        with open(self.chatlogName, 'r') as chatlog:
            for line in chatlog.readlines():
                self.socketClientObject.send(line.encode())
        while True:
            with open(self.chatlogName, 'r') as chatlog:
                newlastLine=chatlog.readlines()[-1]
                if newlastLine!=lastLine:
                    lastLine=newlastLine
                    self.socketClientObject.send(str('\n'+lastLine).encode())


    def ClientInstance(self,IP,port,socketClientObject,userNumber):
        username=socketClientObject.recv(65536).decode()
        print(username)
        connectionMessage=str('You have successfully connected, '+username)
        socketClientObject.send(connectionMessage.encode())
        rData=''
        threading.Thread(target=self.CheckForMessages,daemon=True).start()
        while rData!='-END':
            rData=socketClientObject.recv(65536).decode()
            sData=str('\n\n'+username+': '+rData)   
            with open(self.chatlogName, 'a') as chatlog:
                chatlog.write(sData)
                #writes the users message into the chatlog

        return


server,chatlogName=NewServer()
userDB={}
#log=open('planning/socket/data/chat_log.txt','w')
#log.write("hi there")
#log.close()
messageQueue=Queue(maxsize=0) #creates a queue that goes between threads and collates messages being sent in both threads.
while True:
    print('listening')
    server.listen()
    clientObj, (clientIP,clientPort) = server.accept()
    if clientObj not in userDB:        
        userDB.update({clientObj:Client(clientIP,clientPort,clientObj,len(userDB),chatlogName)})