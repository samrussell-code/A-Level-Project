#Server starts, in multiple threads. Each thread can be indicated by the opcode sent before the data, from the client.
#When the client is at the launcher screen, opcodes will either be REGISTER_ACCOUNT(00) or LOGIN_ACCOUNT(01). The server needs to read the opcode, then interpret the following data correctly.

#example data would be '00' and then, seperately, ['John Smith','password123']. First, tuple[0] is taken, and checked against every database username to see if the username has been taken or not.
#if it is taken, the server will return '0' to signify an unsuccessful registration.
#if not, the user registration is given its own unique index (previous index+1), where tuple[0] is registered in the database as a username, and tuple[1] is registered as a password. returning '1'
#to signify a successful registration.

#example data would be '01' and then, seperately, ['John Smith','password123']. First, tuple[0] is taken and checked against every database username. Return '0' if username is not in database.
#Return '1' if password does not match correct password.
#If the username and password are correct, details must be fetched back to fill out variables for the Account client class.
import sqlite3
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
    result=cursor.fetchall();print(result)
    if len(result)==0:
        dbAddToTable(connection,'INSERT INTO profiles (username, password) VALUES (?,?);',(username,password))
        print('Successfully registered your account.')
    else:
        ERR_CATCH(2)
def LOGIN_ACCOUNT(username,password,connection):
    return

recv_opcode,recv_operand=0,('John Smithus','password123')#temporary data #this is where we want to recieve the client data.
(username,password),connection=recv_operand,dbConnect('ACCOUNTS')
dbCreateTable(connection, sql_create_profiles_table) if connection is not None else ERR_CATCH(3)
REGISTER_ACCOUNT(username,password,connection) if recv_opcode==0 else LOGIN_ACCOUNT(username,password,connection) if recv_opcode==1 else ERR_CATCH(1)


