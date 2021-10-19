import sqlite3

def dbConnect(filename):
    print('Connecting to',filename,'...')
    connection=sqlite3.connect(str(filename+'.db'))
    return connection

def dbCreateTable(connection,create_table_sql):#only run this to create a new table in the db
    cursor=connection.cursor()
    cursor.execute(create_table_sql)

def REGISTER_ACCOUNT(username,password,cursor):
    return
def LOGIN_ACCOUNT(username,password,cursor):
    return
def ERR_CATCH(id):
    errmsgs=[
        'Unknown error.',
        'Unsupported opcode from client.',
        'Account with this username already exists.',
        'Cannot create the database connection.'
    ]
    print(str('Error #'+str(id)+'|'+errmsgs[id]+'\n'))
    return

recv_opcode,recv_operand=0,('John Smith','password123')#temporary data
(username,password),connection=recv_operand,dbConnect('ACCOUNTS')
sql_create_accounts_table="""CREATE TABLE IF NOT EXISTS profiles (
    id integer PRIMARY KEY,
    username text NOT NULL,
    password text NOT NULL
);"""

dbCreateTable(connection, sql_create_accounts_table) if connection is not None else ERR_CATCH(3)
REGISTER_ACCOUNT(username,password,connection) if recv_opcode==0 else LOGIN_ACCOUNT(username,password,connection) if recv_opcode==1 else ERR_CATCH(1)
