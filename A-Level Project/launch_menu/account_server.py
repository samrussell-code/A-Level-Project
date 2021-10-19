import socket,threading,time

#Server starts, in multiple threads. Each thread can be indicated by the opcode sent before the data, from the client.
#When the client is at the launcher screen, opcodes will either be REGISTER_ACCOUNT(00) or LOGIN_ACCOUNT(01). The server needs to read the opcode, then interpret the following data correctly.

#example data would be '00' and then, seperately, ['John Smith','password123']. First, tuple[0] is taken, and checked against every database username to see if the username has been taken or not.
#if it is taken, the server will return '0' to signify an unsuccessful registration.
#if not, the user registration is given its own unique index (previous index+1), where tuple[0] is registered in the database as a username, and tuple[1] is registered as a password. returning '1'
#to signify a successful registration.

#example data would be '01' and then, seperately, ['John Smith','password123']. First, tuple[0] is taken and checked against every database username. Return '0' if username is not in database.
#Return '1' if password does not match correct password.
#If the username and password are correct, details must be fetched back to fill out variables for the Account client class.

