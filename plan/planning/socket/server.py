import socket               # Import socket module
import time
userDict={}

class ClientContainer:
    '''
    ClientContainer(username,clientObject,clientIP,outgoingPort)
    Contains the useful information about a connected client. Will be stored inside the connectionDict dict.
    Methods: DisplayUserInfo(counter)
    '''
    def __init__(self,username,clientObject,clientIP,outgoingPort):
        self.username=username
        self.clientObject=clientObject
        self.clientIP=clientIP
        self.outgoingPort=outgoingPort

    def DisplayUserMessage(self,message=''):
        '''
        DisplayUserInfo(message='') outputs the users message to server along with their info
        '''
        self.lastServerMessage=message
        print(f'''        Data display for user #{self.username} in runtime:
        Client Username - {self.username}
        Client IP - {self.clientIP}
        Outgoing Port - {self.outgoingPort}
        Message - '{message}' 
        ''')

def NewServer():
    server = socket.socket()         #creates a server
    host = socket.gethostname() #gets the name of the computer running the server
    port = 25520
    server.bind((host, port))      #opens the specified port for the specified hostname
    return server

def InstantiateClient(userDict):
    return

server=NewServer()

server.listen()                     #waits for a request to be sent from client
clientObj, (clientIP,clientPort) = server.accept()  #collects information from the requesting clients
data='Thank you for connecting!'
clientObj.send(data.encode()) #sends over data in the correct codec
username=clientObj.recv(65536).decode() #recieves the first piece of data from the client which is their workstation name, as a placeholder for a true username.

if clientObj not in userDict.keys(): #addsthe new clients into the dictionary with the IP as the key, and the client object as the value
    userDict.update({clientObj:ClientContainer(username,clientObj,clientIP,clientPort)})

while True:
    recievedData=clientObj.recv(65536).decode()
    user=userDict[clientObj]
    user.DisplayUserMessage(recievedData)
    
    for key in userDict.keys(): #sending out the data
       messageUser=userDict[clientObj].username
       dataToSend=str(messageUser+": "+recievedData)
       key.send((dataToSend).encode())
clientObj.close() #removes the connection to the client