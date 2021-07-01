import socket               # Import socket module
import time

class ClientContainer:
    '''
    Contains the useful information about a connected client. Will be stored inside the connectionDict dict.
    Methods: DisplayUserInfo(counter)
    '''
    def __init__(self,clientObject,clientIP,outgoingPort):
        self.clientObject=clientObject
        self.clientIP=clientIP
        self.outgoingPort=outgoingPort
    def DisplayUserMessage(self,counter=0,message=''):
        '''
        DisplayUserInfo(counter=0,message) outputs the users message to server along with their info
        '''
        self.lastServerMessage=message
        print(f'''        Data display for user #{counter} in runtime:
        Client IP - {self.clientIP}
        Outgoing Port - {self.outgoingPort}
        Message - {message}''')

server = socket.socket()         #creates a server
host = socket.gethostname() #gets the name of the computer running the server
port = 25520                             
server.bind((host, port))      #opens the specified port for the specified hostname

server.listen(5)                     #waits for a request to be sent from client, up to 5 unsuccessful attempts
connectionDict={}

clientObj, (clientIP,clientPort) = server.accept()  #collects information from the requesting clients
data='Thank you for connecting!'
clientObj.send(data.encode()) #sends over data in the correct codec   
while True:
   if clientObj not in connectionDict.keys(): #adds any new clients into the dictionary with the IP as the key, and the client object as the value
        connectionDict.update({clientObj:ClientContainer(clientObj,clientIP,clientPort)})

   count=1
   server.listen(5)
   recievedData=clientObj.recv(65536).decode()
   for key in connectionDict.keys(): #goes through every user in the connection list and outputs their information
       user=connectionDict[key]
       user.DisplayUserMessage(count,recievedData)
       count+=1
   for key in connectionDict.keys():
       key.send(recievedData.encode())
clientObj.close() #removes the connection to the client