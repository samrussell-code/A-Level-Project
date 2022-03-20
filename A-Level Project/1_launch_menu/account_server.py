#Server starts, in multiple threads. Each thread can be indicated by the opcode sent before the data, from the client.
#When the client is at the launcher screen, opcodes will either be REGISTER_ACCOUNT(00) or LOGIN_ACCOUNT(01). The server needs to read the opcode, then interpret the following data correctly.

#example data would be '0' and then, seperately, ['John Smith','password123']. First, tuple[0] is taken, and checked against every database username to see if the username has been taken or not.
#if it is taken, the server will return '0' to signify an unsuccessful registration.
#if not, the user registration is given its own unique index (previous index+1), where tuple[0] is registered in the database as a username, and tuple[1] is registered as a password. returning '1'
#to signify a successful registration.

#example data would be '1' and then, seperately, ['John Smith','password123']. First, tuple[0] is taken and checked against every database username. Return '0' if username is not in database.
#Return '1' if password does not match correct password.
#If the username and password are correct, details must be fetched back to fill out variables for the Account client class.
import opcode
from pickle import TRUE
import random
import sqlite3, socket, threading, datetime, time
from tkinter import END
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
    AccessTime blob NOT NULL,
    AccessReason blob
);"""
sql_create_CONNECTION_IP_table="""CREATE TABLE IF NOT EXISTS CONNECTION_IP (
    IPID integer PRIMARY KEY,
    IP text
);"""
sql_create_LOBBY_table="""CREATE TABLE IF NOT EXISTS LOBBY (
    LobbyID integer PRIMARY KEY,
    LobbyName blob,
    LobbyPassword blob,
    PlayerID1 integer,
    PlayerID2 integer,
    IsOnline blob,
    Player1Data blob,
    Player2Data blob
);"""
def dbCreateTable(connection,create_table_sql):
    '''only run this to create a new table in the db'''
    cursor=connection.cursor() #used to modify database
    cursor.execute(create_table_sql) #runs the sql formatted command to create a table
def dbAddToTable(connection,sql_insert,values,table_name='00_UNKNOWN_00',debug=True):
    cursor=connection.cursor()
    cursor.execute(sql_insert,values)
    connection.commit()
    if debug==True:
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
        LogConnection(cursor,connection,username,ip,'Registered Account')
        return True
    else:
        ERR_CATCH(2)

def LogConnection(cursor,connection,username,ip,reason='No Reason Given'):

    '''Finds the UUID of the given username, then the IPID of the given IP.
      Then stores the IPID and UUID of a connection being made at a given time,found with datetime.'''

    cursor.execute(f'''SELECT UUID FROM PROFILE_INFO WHERE username="{username}"''');UUID=cursor.fetchone()[0]
    cursor.execute(f'''SELECT IPID FROM CONNECTION_IP WHERE IP="{ip}"''')
    result=cursor.fetchone()
    if result==None: #adds new IP to table and attempts to get an id again 
        dbAddToTable(connection,'INSERT INTO CONNECTION_IP (IP) VALUES (?);',([ip]),'CONNECTION_IP')
        cursor.execute(f'''SELECT IPID FROM CONNECTION_IP WHERE IP="{ip}"''')
        IPID=cursor.fetchone()[0]
    else:
        IPID=result[0]
    dt=datetime.datetime.now();date=dt.strftime("%d/%m/%y");time=dt.strftime("%X")
    dbAddToTable(connection,'INSERT INTO PROFILE_CONN_HIST (UUID, IPID, AccessDate, AccessTime,AccessReason) VALUES (?,?,?,?,?);',(UUID,IPID,date,time,reason),'PROFILE_CONN_HIST')
    print(f'''Logged Connection at "{time}".''')

def LOGIN_ACCOUNT(username,password,connection,sockname):
    '''Returns a password of a matching username, or type None if username isn't found.
      Then calls various errors if the password is nonexistent or empty. Finally, calls LOGIN_SUCCESS, and returns True.
    '''
    ip=str(sockname[0])
    cursor=connection.cursor()
    cursor.execute(f'''SELECT password FROM PROFILE_INFO WHERE username="{username}"''')
    result=cursor.fetchone() #ask miss, how do i fetch from sql db in string format rather than tuple/list format for a single item
    try:
        result=result[0]
    except:
        ERR_CATCH(0)
    if result==None:
        ERR_CATCH(9)
    elif len(result)==0:
        ERR_CATCH(10)
    elif result==password:
        LOGIN_SUCCESS(username,cursor)
        LogConnection(cursor,connection,username,ip,'Logged Into Account')
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
    port=25520
    server.bind((host,port))
    return server

class ClientHandler:
    def __init__(self,socketInfo,socketObject):
        self.socketObject=socketObject
        self.StartThread(socketInfo)
    def StartThread(self,socketInfo):
        threading.Thread(target=self.RecieveData,daemon=True).start()
    def RecieveData(self): #should only be used for logging in
        try:
            operation=(self.socketObject.recv(65536).decode()).split('||') #creates a list of the different items in the operation.
        except:
            #ERR_CATCH(7)
            pass
        #print('recieved data',operation)
        recv_opcode,username,password,connection=int(operation[0]),operation[1],operation[2],dbConnect('ACCOUNTS')
        dbCreateTable(connection, sql_create_PROFILE_INFO_table),dbCreateTable(connection, sql_create_PROFILE_CONN_HIST_table),dbCreateTable(connection, sql_create_CONNECTION_IP_table),
        dbCreateTable(connection,sql_create_LOBBY_table) if connection is not None else ERR_CATCH(3)
        if recv_opcode==0:
            success=REGISTER_ACCOUNT(username,password,connection,socketObject.getpeername())
            if success==True:
                self.SendData(0,['Registered profile and logged in...',1])
            else:
                self.SendData(0,['Register failed.',0])

        elif recv_opcode==1:
            print('recieved opcode 1')
            success=LOGIN_ACCOUNT(username,password,connection,socketObject.getpeername())
            if success==True:
                self.SendData(0,['Logged into account on database...',1])
            else:
                self.SendData(0,['Login failed.',0])
        elif recv_opcode==2:
            print('recieved opcode 2')
            lobby_name=operation[3]
            self.CREATE_LOBBY(operation,connection,socketObject.getpeername())
        elif recv_opcode==3:
            print('recieved opcode 3')
            self.JOIN_LOBBY(operation,connection,socketObject.getpeername())
        else:
            ERR_CATCH(1)

    def CREATE_LOBBY(self,operation,connection,sockname):
        '''The player creating a lobby is the host, ref player1
        '''
        player1,lobby_password,lobby_name=operation[1],operation[2],operation[3]
        cursor=connection.cursor()
        ip=str(sockname[0])
        cursor.execute(f'''SELECT UUID FROM PROFILE_INFO WHERE username="{player1}"''')
        result=cursor.fetchone() #result[0] is player1 id.
        playerID1=result[0]
        cursor.execute(f'''SELECT LobbyID FROM LOBBY WHERE PlayerID1="{playerID1}"''')
        result=cursor.fetchone()
        
        if result==None:
            dbAddToTable(connection,'INSERT INTO LOBBY (LobbyName,LobbyPassword,PlayerID1,IsOnline) VALUES (?,?,?,?);',(lobby_name,lobby_password,playerID1,'True'),'LOBBY')
            LogConnection(cursor,connection,player1,ip,f'''Created Lobby: {lobby_name}''')
            cursor.execute(f'''SELECT LobbyID FROM LOBBY WHERE PlayerID 1="{playerID1}"''')
            result=cursor.fetchone()
            lobby_ID=result[0]
        else:
            lobby_ID=result[0]
            dbAddToTable(connection,'UPDATE LOBBY SET LobbyName=?, LobbyPassword=?, PlayerID2=?, IsOnline=? WHERE PlayerID1=?;',(lobby_name,lobby_password,None,'True',playerID1),'LOBBY')
            LogConnection(cursor,connection,player1,ip,f'''Updated Lobby: {lobby_name}''')
        self.lobby_ID=lobby_ID
        self.connection=connection
        game_log=open(str(str(lobby_ID)+'.txt'),'w')
        game_log.write(str('Lobby restarted at: '+str(round(time.time()))+'\n\n'))
        game_log.write('User #'+str(playerID1)+': "'+str(player1)+'" is ready.\n\n')
        game_log.close()
        #now wait until player 2 has joined in the database, by checking the database until a result is found
        playerID2=None
        while playerID2==None:
            cursor.execute(f'''SELECT PlayerID2 FROM LOBBY WHERE LobbyID="{lobby_ID}"''')
            playerID2=cursor.fetchone()[0] #breaks when player joins
        self.SendData(4,[playerID2,'Game Ready'],False)#OPCODE4 is lobby ready, sends the ID of the opponent
        self.ManageGame(1)

    def JOIN_LOBBY(self,operation,connection,sockname): #ISSUE - MULTIPLE LOBBIES WITH THE SAME USERNAME AND PASSWORD MEAN USERS ONLY JOIN THE FIRST FETCHED LOBBY
        '''The player joining a lobby is the guest, ref player2
        '''
        player2,lobby_password,lobby_name=operation[1],operation[2],operation[3]
        cursor=connection.cursor()
        ip=str(sockname[0])
        cursor.execute(f'''SELECT LobbyID FROM LOBBY WHERE LobbyName="{lobby_name}" AND LobbyPassword="{lobby_password}" AND IsOnline = "True"''') #  
        result=cursor.fetchone()
        if result==None:
            print('no lobby found with the requested username password that is online')
            return #ends the subroutine
        lobby_ID=result[0]
        self.lobby_ID=lobby_ID
        cursor.execute(f'''SELECT UUID FROM PROFILE_INFO WHERE username="{player2}"''')
        playerID2=cursor.fetchone()[0]
        print('found lobby with ID ',lobby_ID)
        dbAddToTable(connection,'UPDATE LOBBY SET PlayerID2=? WHERE LobbyID=?;',(playerID2,lobby_ID),'LOBBY')
        self.connection=connection
        game_log=open(str(str(lobby_ID)+'.txt'),'a')
        game_log.write('User #'+str(playerID2)+': "'+str(player2)+'" is ready.\n\n')
        game_log.write(str('ground'+str(random.randint(1,3))))#line7 is floortype, generates a floortype for the game
        game_log.close()
        cursor.execute(f'''SELECT PlayerID1 FROM LOBBY WHERE LobbyID="{lobby_ID}"''')
        playerID1=cursor.fetchone()[0] #gets the host ID
        self.SendData(4,[playerID1,'Game Ready'],False)#OPCODE4 is lobby ready, sends the ID of the opponent
        self.ManageGame(2)

    def UpdatePlayerInputs(self,playernumber):
        ''' Starts at both players ready
        '''
        while self.GAME_TIME==True:
            try:
                info_list=self.RecieveGameInfo()
                #print('info list:',info_list)
                #[Input_Left,Input_Right,Queued_Bullet]
                if playernumber==1:
                    self.Player1.left_input,self.Player1.right_input,self.Player1.bullet_queued=info_list[0],info_list[1],info_list[2]
                    #info for player 1 has been collected. in order to communicate this to player 2, and retrieve their data, two instances of clienthandler must communicate externally.
                elif playernumber==2:
                    self.Player2.left_input,self.Player2.right_input,self.Player2.bullet_queued=info_list[0],info_list[1],info_list[2]#
            except:
                #ERR_CATCH(0)
                pass
            

    def ManageGame(self,player_id):#both connections are in this subroutine, so need to make sure no generation occurs here
        '''MAIN
        '''
        self.Player1=Player(0.1,0.6)
        self.Player2=Player(0.8,0.6)
        game_log=open(str(str(self.lobby_ID)+'.txt'),'r')#using the text file ensures sync across both instances of server connection
        for pos,line in enumerate(game_log): #this for loop finds the 7th line in the file and sets it to var line
            if pos == 6:
                #print('line',pos,'is: ',line)
                floortype=line
        print('sending ground texture code...')
        connection=dbConnect('ACCOUNTS')
        self.SendData(5,[floortype,'kill||'],False)#OPCODE5 is type of ground texture to use
        dbAddToTable(connection,'UPDATE LOBBY SET Player1Data=? WHERE LobbyID=?;',('0.1 0.6',self.lobby_ID),'LOBBY',False)
        dbAddToTable(connection,'UPDATE LOBBY SET Player2Data=? WHERE LobbyID=?;',('0.8 0.6',self.lobby_ID),'LOBBY',False)
        time.sleep(1)
        self.GAME_TIME=True
        threading.Thread(target=self.UpdatePlayerInputs,args=(player_id,),daemon=True).start()
        threading.Thread(target=self.UpdateDatabase,args=(player_id,),daemon=True).start()
        while self.GAME_TIME==True:
            #main game updater, sends data to clients
            player_list=[self.Player1,self.Player2]
            player=player_list[player_id-1]
            #print('player.left:',player.left_input,'player.right:',player.right_input,'player.velocity:',player.velocity_x,'player.position',player.position_x, self.Player1.position_x, self.Player2.position_x)
            if int(player.left_input)==1 and int(player.right_input)!=1:
                player.velocity_x=-0.0001
            elif int(player.right_input)==1 and int(player.left_input)!=1:
                player.velocity_x=0.0001
            elif int(player.right_input)==0 and int(player.left_input)==0:
                player.velocity_x=0
            if player.bullet.is_queued==True: #if bullet is waiting to be fired, place it in the same position as the player
                player.bullet.position_x,player.bullet.position_y=player.position_x,player.position_y
                player.bullet.is_queued=False
            player.position_x+=player.velocity_x;player.position_y+=player.velocity_y #update the positions of YOUR PLAYER
            player.bullet.position_x+=player.bullet.velocity_x
            player.bullet.position_y+=player.bullet.velocity_y
                
            if int(player_id)==1:
                self.Player1=player #this will be empty if user is p2
            elif int(player_id)==2:
                self.Player2=player #this will be empty if user is p1
            self.SendData(6,[
            self.Player1.position_x,
            self.Player1.position_y,
            self.Player1.bullet.position_x,
            self.Player1.bullet.position_y,
            self.Player2.position_x,
            self.Player2.position_y,
            self.Player2.bullet.position_x,
            self.Player2.bullet.position_y,
            'kill||'
            ],False)#OPCODE6 is game data

    def UpdateDatabase(self,player_id):
        connection=dbConnect('ACCOUNTS')
        while self.GAME_TIME==True:
            if int(player_id)==1:
                #upload player 1 inputs to database host
                #read player 2 inputs from database and apply to self.player2.left/right

                dbAddToTable(connection,'UPDATE LOBBY SET Player1Data=? WHERE LobbyID=?;',(str(self.Player1.get_position()),self.lobby_ID),'LOBBY',False)
                cursor=connection.cursor()
                cursor.execute(f'''SELECT Player2Data FROM LOBBY WHERE LobbyID="{self.lobby_ID}"''') # 
                result=cursor.fetchone()[0]
                #print('got a player 2 position of ',result)
                self.Player2.set_position(result)      
            elif int(player_id)==2:
                #upload player 2 inputs to database
                #read player 1 inputs from database and apply to self.player1.left/right
                dbAddToTable(connection,'UPDATE LOBBY SET Player2Data=? WHERE LobbyID=?;',(str(self.Player2.get_position()),self.lobby_ID),'LOBBY',False)
                cursor=connection.cursor()
                cursor.execute(f'''SELECT Player1Data FROM LOBBY WHERE LobbyID="{self.lobby_ID}"''') # 
                result=cursor.fetchone()[0]
                self.Player1.set_position(result)
            #print(self.Player1.get_position(),self.Player2.get_position())

    def SendData(self,opcode,data_list,recieve=True):
        data=str(opcode)
        #print('sending data', data_list,opcode)
        for item in data_list: data+='||'+str(item) #formatting data to be sent
        self.socketObject.send(data.encode())
        if recieve==True:
            self.RecieveData()
        #6||0||0||0||0||kill|| 6||0||0||0||0||kill|| 6||0||0||0||0||kill||
    def RecieveGameInfo(self):
        try:
            operation=(self.socketObject.recv(65536).decode()).split('||') #creates a list of the different items in the operation.
        except:
            #ERR_CATCH(7)
            pass
        try:
            kill_pos=operation.index('kill')
            operation=operation[:kill_pos]
            while operation[0]!='4':
                operation=operation[1:len(operation)] #data error, makes sure first value is always the opcode 4
                recv_opcode=operation[0]
                #print('recieved data in game',operation)
                return operation[1:len(operation)]
        except:
            #ERR_CATCH(12)
            pass

    def OverwriteFileLine(self,line,data):
        with open(str(str(self.lobby_ID)+'.txt'),'r') as file:
            lines=file.readlines()
        while (len(lines)-1)<line:
            lines.append('')
        lines[line]=data
        with open(str(str(self.lobby_ID)+'.txt'),'w') as file:
            #print('LINES:',lines)
            file.writelines(lines)    


class Player():
    def __init__(self,init_position_x=0,init_position_y=0):
        self.left_input=0
        self.right_input=0
        self.velocity_x=0
        self.velocity_y=0
        self.position_x=init_position_x
        self.position_y=init_position_y
        self.bullet=Bullet(init_position_x,init_position_y)
    def get_position(self):#returns the player position variables in a str
        return str(self.position_x)+' '+str(self.position_y)
    def set_position(self,input_str):
        input_str=input_str.split()
        #print('input string:',input_str)
        self.position_x,self.position_y=float(input_str[0]),float(input_str[1])
class Bullet():
    def __init__(self,init_x,init_y):
        self.position_x=init_x
        self.position_y=init_y
        self.velocity_x=0
        self.velocity_y=0
        self.mouse_angle=0
        self.is_queued=False

server=NewServer()
connections={}
while True:
    server.listen()
    socketObject,socketInfo=server.accept()
    if socketObject not in connections:  
        connections.update({socketObject:ClientHandler(socketInfo,socketObject)})
