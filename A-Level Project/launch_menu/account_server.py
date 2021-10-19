import socket,threading,time

#Server starts, in multiple threads. Each thread can be indicated by the opcode sent before the data, from the client.
#When the client is at the launcher screen, opcodes will either be REGISTER_ACCOUNT(0) or LOGIN_ACCOUNT(1). The server needs to read the opcode, then interpret the following data correctly.

#example data would be '0' and then, seperately, ('John Smith','password123'). First, tuple[0] is taken, and checked against every database username to see if the username has been taken or not.
#if it is taken, the server will return '0' to signify an unsuccessful registration.
#if not, the user registration is given its own unique index (previous index+1), where tuple[0] is registered in the database as a username, and tuple[1] is registered as a password. returning '1'
#to signify a successful registration.

#example data would be '01' and then, seperately, ('John Smith','password123'). First, tuple[0] is taken and checked against every database username. Return '0' if username is not in database.
#Return '1' if password does not match correct password.
#If the username and password are correct, details must be fetched back to fill out variables for the Account client class.

recv_opcode=0
recv_operand=('John Smith','password123')

REGISTER_ACCOUNT(recv_operand) if recv_opcode==0 else LOGIN_ACCOUNT(recv_operand) if 1 else ERROR_CATCH(1)

def REGISTER_ACCOUNT():
    return
def LOGIN_ACCOUNT():
    return
def ERROR_CATCH(id)
    errmsgs=[
        'Unknown error'
        'Unsupported opcode from client'
    ]
    return str('Error #'+id+'|'+errmsgs[id])