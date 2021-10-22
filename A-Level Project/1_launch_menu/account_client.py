#Encrypting a password. The fernet key is pre-loaded, and then used to encrypt the password, away from the server side.
#By the time the password is sent to the server, it should already be encrypted clientside.
from err import ERR_CATCH
import os, socket, threading, base64
os.mkdir('client') if  not os.path.exists('client') else print('Do not need to make client path, already exists.')
def TOKEN_FOUND(password):
    try:
        with open('client//username.txt','r') as file: username=file.readline()
        opcode=1
        SEND_DATA(opcode,[username,password])
    except:
        ERR_CATCH(6)
        TOKEN_MISSING()
def TOKEN_MISSING():
    #wait for user to input a password through the gui box here
    username=str(input('Enter username\n'))
    password=str(input('Enter password\n'))
    opcode=int(input('Enter code to 0 register or 1 login\n'))
    try:
        password_token=(base64.b64encode(password.encode())).decode() #uses b64 to encrypt the password
    except:
        ERR_CATCH(5)
    with open('client//username.txt','w') as file: file.write(username);file.close()
    with open('client//authtoken.txt','w') as file: file.write(password_token);file.close()
    SEND_DATA(opcode,[username,password_token])

def SEND_DATA(opcode,data_list):
    data=str(opcode)
    for item in data_list: data+='||'+item #formatting data to be sent
    connection=CreateConnection()
    connection.send(data.encode())
def CreateConnection():
    socketObject=socket.socket()
    port=25520
    try:
        socketObject.connect(('tank.servegame.com', port))
        return socketObject
    except:
        ERR_CATCH(8)
try: 
    with open('client//authtoken.txt','r') as file:
        for line in file: password=line
    TOKEN_FOUND(password)
except:
    ERR_CATCH(4)
    TOKEN_MISSING()
