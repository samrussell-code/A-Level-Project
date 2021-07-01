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
    def DisplayUserInfo(self,counter=0):
        '''
        DisplayUserInfo(counter=0) outputs a debug of the clients info with an optional counter if clientcontainers are read in a list.
        '''
        print(f'''        Data display for user #{counter} in runtime:
        Client IP - {self.clientIP}
        Outgoing Port - {self.outgoingPort}''')

server = socket.socket()         #creates a server
host = socket.gethostname() #gets the name of the computer running the server
port = 25520                             
server.bind((host, port))      #opens the specified port for the specified hostname

server.listen(5)                     #waits for a request to be sent from client, up to 5 unsuccessful attempts
connectionDict={}
while True:
   clientObj, (clientIP,clientPort) = server.accept()  #collects information from the requesting clients

   if clientIP not in connectionDict.keys(): #adds any new clients into the dictionary with the IP as the key, and the client object as the value
        connectionDict.update({clientIP:ClientContainer(clientObj,clientIP,clientPort)})

   data='Thank you for connecting!'
   clientObj.send(data.encode()) #sends over data in the correct codec
   print(connectionDict)
   
   count=1
   for key in connectionDict.keys(): #goes through every user in the connection list and outputs their information
       user=connectionDict[key]
       user.DisplayUserInfo(count)
       count+=1
   clientObj.close() #removes the connection to the client