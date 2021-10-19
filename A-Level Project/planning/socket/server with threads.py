import socket               # Import socket module
import threading
import time

def NewServer():
    server = socket.socket()         #creates a server
    host = socket.gethostbyname('SamWorkstation') #gets the name of the computer running the server
    print(host)
    port = 25520
    server.bind((host, port))      #opens the specified port for the specified hostname
    chatlogName=str('planning/socket/data/'+'chatlog - '+str(round(time.time()))+'.txt') #creates the name and location of the text file to store the data transfer log
    newChatLog=open(chatlogName,'w')
    newChatLog.write(str('Server started at: '+str(round(time.time()))+'\n\n'))
    newChatLog.close() #closes the data log ready for runtime
    return server,chatlogName

class Client:
    '''
    Class for handling client information on the server side. Deals with send/recieve cycling and handling the log textfile.
    Methods: StartThreads(), SenderNode(), RecieverNode(IP,port,socketClientObject,userNumber)
    '''
    def __init__(self,IP,port,socketClientObject,userNumber,chatlogName):
        self.StartThreads()
        self.localDB={}
        self.chatlogName=chatlogName
        self.socketClientObject=socketClientObject #defining public variables

    def StartThreads(self):
        '''
        StartThreads():
        Subroutine ran seperately on initialisation that begins the reciever thread. Only used once.
        '''
        threading.Thread(target=self.RecieverNode,args=(clientIP,clientPort,clientObj,len(userDB)),daemon=True).start()

    def SenderNode(self):
        '''
        SenderNode():
        Subroutine ran on a seperate thread inside of the RecieveNode thread. It checks for updates in the log textfiles final line, and if the final line has changed then it sends the client object the new line.
        '''
        with open(self.chatlogName, 'r') as chatlog: #opens chatlog for reading the new line, using 'with open' ensures text file closes on completion
            for line in chatlog.readlines(): #sends the user every previous message before they joined. - this only activates after they send the first message for some reason
                self.socketClientObject.send(line.encode())  
                lastLine=line          
                isConnected=True
        while isConnected==True:
            with open(self.chatlogName, 'r') as chatlog: #reads the final line in a loop until the final line has changed, meaning the file has been updated
                newlastLine=chatlog.readlines()[-1]
                if newlastLine!=lastLine:
                    isEmpty=True if lastLine=='' else False
                    lastLine=newlastLine
                    if isEmpty==False:
                        try:
                            self.socketClientObject.send(str('\n'+lastLine).encode()) #sends the final line out to the object.
                        except:
                            print('cannot message client, client has left.')
                            isConnected=False

    def RecieverNode(self,IP,port,socketClientObject,userNumber): 
        '''
        RecieverNode(self,IP,port,socketClientObject,userNumber):
        Subroutine ran in a thread that checks for recieved data from the client and converts that data into a writeable format to be put into the log and managed by the sender node.
        '''
        try:
            username=socketClientObject.recv(65536).decode()  #the first data recieved should always be the username, or workstation name
            connectionMessage=str('You have successfully connected, '+username)
            socketClientObject.send(connectionMessage.encode()) #sends back the confirmation message to agree to a connection.
            rData=''
            threading.Thread(target=self.SenderNode,daemon=True).start() #creates the sender node
            while rData!='-END':
                rData=socketClientObject.recv(65536).decode() #retreives any data it can
                sData=str('\n\n'+username+': '+rData)    #creates a formatted version, then inputs it into the log file
                with open(self.chatlogName, 'a') as chatlog:
                    chatlog.write(sData)
                    #writes the users message into the chatlog
        except:
            print('User has disconnected')
        return

server,chatlogName=NewServer()
userDB={}
while True:
    server.listen()
    clientObj, (clientIP,clientPort) = server.accept()
    if clientObj not in userDB:        
        userDB.update({clientObj:Client(clientIP,clientPort,clientObj,len(userDB),chatlogName)})
