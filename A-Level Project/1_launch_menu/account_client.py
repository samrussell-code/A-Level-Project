#Encrypting a password. The fernet key is pre-loaded, and then used to encrypt the password, away from the server side.
#By the time the password is sent to the server, it should already be encrypted clientside.
from cryptography.fernet import Fernet
from err import ERR_CATCH
import os, socket, threading
def TOKEN_FOUND(password):
    try:
        with open('client//username.txt','r') as file: username=file.read()
        SEND_DATA(00,[username,password])
    except:
        ERR_CATCH(6)
        os.remove('client//authtoken.bin')
        TOKEN_MISSING()
def TOKEN_MISSING():
    key= b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
    cipher=Fernet(key) #creates a fernet object of the encryption key
    #wait for user to input a password through the gui box here
    username='jonny emery'
    password='password24'
    try:
        password_token=cipher.encrypt(password.encode()) #uses the fernet object to encrypt the password
    except:
        ERR_CATCH(5)
    with open('client//username.txt','w') as file: file.write(username);file.close()
    with open('client//authtoken.bin','wb') as file: file.write(password_token);file.close()
    SEND_DATA(00,[username,password_token.decode()])

def SEND_DATA(opcode,data_list):
    data=str(opcode)
    for item in data_list: data+='|'+item #formatting data to be sent
    connection=CreateConnection()
    print(data)
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
    with open('client//authtoken.bin','rb') as file:
        for line in file: password=line
    TOKEN_FOUND(password)
except:
    ERR_CATCH(4)
    TOKEN_MISSING()
