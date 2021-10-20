import sqlite3
def dbCreateTable(connection,create_table_sql):#only run this to create a new table in the db
    cursor=connection.cursor()
    cursor.execute(create_table_sql)
def dbAddToTable(connection,sql_insert,values):
    cursor=connection.cursor()
    cursor.execute(sql_insert,values)
    connection.commit()
    print(cursor.rowcount,'record inserted')
sql_create_profiles_table="""CREATE TABLE IF NOT EXISTS profiles (
    id integer PRIMARY KEY,
    username text NOT NULL,
    password text NOT NULL
);"""
def dbConnect(filename):
    print('Connecting to',filename,'...')
    connection=sqlite3.connect(str(filename+'.db'))
    return connection
def REGISTER_ACCOUNT(username,password,connection):
    cursor=connection.cursor()
    cursor.execute(f'''SELECT id FROM profiles WHERE username="{username}"''')
    result=cursor.fetchall();print(result)
    ERR_CATCH(2) if len(result)!=0 else dbAddToTable(connection,'INSERT INTO profiles (username, password) VALUES (?,?);',(username,password))

    return
def LOGIN_ACCOUNT(username,password,connection):
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

recv_opcode,recv_operand=0,('John Smithus','password123')#temporary data
(username,password),connection=recv_operand,dbConnect('ACCOUNTS')
dbCreateTable(connection, sql_create_profiles_table) if connection is not None else ERR_CATCH(3)
REGISTER_ACCOUNT(username,password,connection) if recv_opcode==0 else LOGIN_ACCOUNT(username,password,connection) if recv_opcode==1 else ERR_CATCH(1)

#Encrypting a password