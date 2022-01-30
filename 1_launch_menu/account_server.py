#Server starts, in multiple threads. Each thread can be indicated by the opcode sent before the data, from the client.
#When the client is at the launcher screen, opcodes will either be REGISTER_ACCOUNT(00) or LOGIN_ACCOUNT(01). The server needs to read the opcode, then interpret the following data correctly.

#example data would be '0' and then, seperately, ['John Smith','password123']. First, tuple[0] is taken, and checked against every database username to see if the username has been taken or not.
#if it is taken, the server will return '0' to signify an unsuccessful registration.
#if not, the user registration is given its own unique index (previous index+1), where tuple[0] is registered in the database as a username, and tuple[1] is registered as a password. returning '1'
#to signify a successful registration.

#example data would be '1' and then, seperately, ['John Smith','password123']. First, tuple[0] is taken and checked against every database username. Return '0' if username is not in database.
#Return '1' if password does not match correct password.
#If the username and password are correct, details must be fetched back to fill out variables for the Account client class.
import sqlite3, socket, threading, datetime
from err import ERR_CATCH

sql_create_PROFILE_INFO_table="""CREATE TABLE IF NOT EXISTS PROFILE_INFO (
    UUID integer PRIMARY KEY,
    username text NOT NULL,
    password blob NOT NULL
);"""
sql_create_PROFILE_CONN_HIST_table="""CREATE TABLE IF NOT EXISTS PROFILE_CONN_HIST (
    CID integer PRIMARY KEY,
    UUID integer NOT NULL,
    IPID integer NOT NULL,
    AccessDate blob NOT NULL,
    AccessTime blob NOT NULL
);"""
sql_create_CONNECTION_IP_table="""CREATE TABLE IF NOT EXISTS CONNECTION_IP (
    IPID integer PRIMARY KEY,
    IP text
);"""

def dbCreateTable(connection,create_table_sql):
    '''only run this to create a new table in the db'''
    cursor=connection.cursor() #used to modify database
    cursor.execute(create_table_sql) #runs the sql formatted command to create a table
def dbAddToTable(connection,sql_insert,values,table_name='00_UNKNOWN_00'):
    cursor=connection.cursor()
    cursor.execute(sql_insert,values)
    connection.commit()
    print(cursor.rowcount,'record inserted into table: ',table_name)
def dbConnect(filename):
    print('Connecting to',filename,'...')
    connection=sqlite3.connect(str(filename+'.db'))
    return connection
def REGISTER_ACCOUNT(username,password,connection,sockname):
    
    '''First, creates an entry in profile info table with the user's information.
      Next, adds the user IP to connection ip table if not already stored.
      Then, stores the transaction with the newly generated UUID and IPID into the connection history table.
      Finally, the serversends an accept response to the client, and calls the login subroutine.'''
    
    ip=str(sockname[0])
    cursor=connection.cursor()
    cursor.execute(f'''SELECT UUID FROM PROFILE_INFO WHERE username="{username}"''') #tries to find a user with that username in profile info
    result=cursor.fetchall()
    if len(result)==0: #if username not found in profile info, registration to db can begin
        dbAddToTable(connection,'INSERT INTO PROFILE_INFO (username, password) VALUES (?,?);',(username,password),'PROFILE_INFO')#adds the username and password to the profile information
        cursor.execute(f'''SELECT IPID FROM CONNECTION_IP WHERE IP="{ip}"''');result=cursor.fetchone()#attempts to find the connection IP address in the database.
        if result==None:
            dbAddToTable(connection,'INSERT INTO CONNECTION_IP (IP) VALUES (?);',([ip]),'CONNECTION_IP')
        print('Successfully registered your account.')
        LogConnection(cursor,connection,username,ip)
        return True
    else:
        ERR_CATCH(2)

def LogConnection(cursor,connection,username,ip):

    '''Finds the UUID of the given username, then the IPID of the given IP.
      Then stores the IPID and UUID of a connection being made at a given time,found with datetime.'''

    cursor.execute(f'''SELECT UUID FROM PROFILE_INFO WHERE username="{username}"''');UUID=cursor.fetchone()[0]
    cursor.execute(f'''SELECT IPID FROM CONNECTION_IP WHERE IP="{ip}"''');IPID=(cursor.fetchone())[0]
    dt=datetime.datetime.now();date=dt.strftime("%d/%m/%y");time=dt.strftime("%X")
    dbAddToTable(connection,'INSERT INTO PROFILE_CONN_HIST (UUID, IPID, AccessDate, AccessTime) VALUES (?,?,?,?);',(UUID,IPID,date,time),'PROFILE_CONN_HIST')
    print(f'''Logged Connection at "{time}".''')

def LOGIN_ACCOUNT(username,password,connection):
    '''Returns a password of a matching username, or type None if username isn't found.
      Then calls various errors if the password is nonexistent or empty. Finally, calls LOGIN_SUCCESS, and returns True.
    '''
    cursor=connection.cursor()
    print('login account request')
    cursor.execute(f'''SELECT password FROM PROFILE_INFO WHERE username="{username}"''')
    result=cursor.fetchone() #ask miss, how do i fetch from sql db in string format rather than tuple/list format for a single item
    print(result)
    try:
        result=result[0]
    except:
        pass
    if result==None:
        ERR_CATCH(9)
    elif len(result)==0:
        ERR_CATCH(10)
    elif result==password:
        LOGIN_SUCCESS(username,cursor)
        return True
    else:
        ERR_CATCH(10)
def LOGIN_SUCCESS(username,cursor):
    cursor.execute(f'''SELECT * FROM PROFILE_INFO WHERE username="{username}"''')
    result=cursor.fetchall()
    id=result[0][0] #result 0 is everything in this user's row. [0][0] is the id position 0 in the users row.
    print('User',id,'was granted login access')

#server stuff
def NewServer():
    server=socket.socket()
    host=socket.gethostname()
    print(host)
    port=25520
    server.bind((host,port))
    return server

class ClientHandler:
    def __init__(self,socketInfo,socketObject):
        self.socketObject=socketObject
        self.StartThread(socketInfo)
    def StartThread(self,socketInfo):
        threading.Thread(target=self.RecieveData,daemon=True).start()
    def RecieveData(self):
        try:
            operation=(self.socketObject.recv(65536).decode()).split('||') #creates a list of the different items in the operation.
        except:
            ERR_CATCH(7)
        print('\noperation 0:',operation[0],'\noperation 1:',operation[1],'\noperation 2:',operation[2])
        recv_opcode,username,password,connection=int(operation[0]),operation[1],operation[2],dbConnect('ACCOUNTS')
        dbCreateTable(connection, sql_create_PROFILE_INFO_table),dbCreateTable(connection, sql_create_PROFILE_CONN_HIST_table),dbCreateTable(connection, sql_create_CONNECTION_IP_table) if connection is not None else ERR_CATCH(3)
        if recv_opcode==0:
            success=REGISTER_ACCOUNT(username,password,connection,socketObject.getpeername())
            if success==True:
                self.SendData(0,['Registered profile and logged in...'])
            else:
                self.SendData(0,['Register failed.'])

        elif recv_opcode==1:
            print('recieved opcode 1')
            success=LOGIN_ACCOUNT(username,password,connection)
            if success==True:
                self.SendData(0,['Logged into account on database...'])
            else:
                self.SendData(0,['Login failed.'])
        else:
            ERR_CATCH(1)
    def SendData(self,opcode,data_list):
        data=str(opcode)
        print('sending data', data_list,opcode)
        for item in data_list: data+='||'+item #formatting data to be sent
        self.socketObject.send(data.encode())
        self.RecieveData()

server=NewServer()
connections={}
while True:
    server.listen()
    socketObject,socketInfo=server.accept()
    if socketObject not in connections:  
        connections.update({socketObject:ClientHandler(socketInfo,socketObject)})
