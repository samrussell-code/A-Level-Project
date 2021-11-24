#Server starts, in multiple threads. Each thread can be indicated by the opcode sent before the data, from the client.
#When the client is at the launcher screen, opcodes will either be REGISTER_ACCOUNT(00) or LOGIN_ACCOUNT(01). The server needs to read the opcode, then interpret the following data correctly.

#example data would be '0' and then, seperately, ['John Smith','password123']. First, tuple[0] is taken, and checked against every database username to see if the username has been taken or not.
#if it is taken, the server will return '0' to signify an unsuccessful registration.
#if not, the user registration is given its own unique index (previous index+1), where tuple[0] is registered in the database as a username, and tuple[1] is registered as a password. returning '1'
#to signify a successful registration.

#example data would be '1' and then, seperately, ['John Smith','password123']. First, tuple[0] is taken and checked against every database username. Return '0' if username is not in database.
#Return '1' if password does not match correct password.
#If the username and password are correct, details must be fetched back to fill out variables for the Account client class.
import sqlite3, socket, threading
from err import ERR_CATCH
def dbCreateTable(connection,create_table_sql):#only run this to create a new table in the db
    cursor=connection.cursor() #used to modify database
    cursor.execute(create_table_sql) #runs the sql formatted command to create a table
def dbAddToTable(connection,sql_insert,values):
    cursor=connection.cursor()
    cursor.execute(sql_insert,values)
    connection.commit()
    print(cursor.rowcount,'record inserted')
sql_create_profiles_table="""CREATE TABLE IF NOT EXISTS profiles (
    id integer PRIMARY KEY,
    username text NOT NULL,
    password blob NOT NULL
);"""
def dbConnect(filename):
    print('Connecting to',filename,'...')
    connection=sqlite3.connect(str(filename+'.db'))
    return connection
def REGISTER_ACCOUNT(username,password,connection):
    cursor=connection.cursor()
    cursor.execute(f'''SELECT id FROM profiles WHERE username="{username}"''')
    result=cursor.fetchall()
    if len(result)==0:
        dbAddToTable(connection,'INSERT INTO profiles (username, password) VALUES (?,?);',(username,password))
        print('Successfully registered your account.')
    else:
        ERR_CATCH(2)
def LOGIN_ACCOUNT(username,password,connection):
    cursor=connection.cursor()
    cursor.execute(f'''SELECT password FROM profiles WHERE username="{username}"''')
    result=cursor.fetchone() #ask miss, how do i fetch from sql db in string format rather than tuple/list format for a single item
    print(result)
    try:
        result=result[0]
    except:
        ERR_CATCH(0)
    if result==None:
        ERR_CATCH(10)
    elif len(result)==0:
        ERR_CATCH(9)
    elif result==password:
        LOGIN_SUCCESS(username,cursor)
    return
def LOGIN_SUCCESS(username,cursor):
    cursor.execute(f'''SELECT * FROM profiles WHERE username="{username}"''')
    result=cursor.fetchall()
    id=result[0][0] #result 0 is everything in this user's row. [0][0] is the id position 0 in the users row.
    print('User',id,'was granted login access')

#server stuff
def NewServer():
    server=socket.socket()
    host=socket.gethostname()
    port=25520
    server.bind((host,port))
    return server

class ClientLogOnHandler:
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
        print(operation)
        recv_opcode,username,password,connection=int(operation[0]),operation[1],operation[2],dbConnect('ACCOUNTS')
        dbCreateTable(connection, sql_create_profiles_table) if connection is not None else ERR_CATCH(3)
        REGISTER_ACCOUNT(username,password,connection) if recv_opcode==0 else LOGIN_ACCOUNT(username,password,connection) if recv_opcode==1 else ERR_CATCH(1)

server=NewServer()
connections={}
while True:
    server.listen()
    socketObject,socketInfo=server.accept()
    if socketObject not in connections:  
        connections.update({socketObject:ClientLogOnHandler(socketInfo,socketObject)})


