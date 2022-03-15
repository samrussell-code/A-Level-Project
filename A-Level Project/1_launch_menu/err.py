def ERR_CATCH(id):
    errmsgs=[
        'Unknown error.', #0
        'Unsupported opcode from client.', #1
        'Account with this username already exists.', #2
        'Cannot create the database connection.', #3
        'No valid authtoken file found.', #4
        'Could not encrypt password.', #5
        'No username file found.', #6
        'Failed to recieve data in thread. (buffer size may have been exceeded)', #7
        'Could not connect to server.', #8
        'User with that name does not exist.', #9
        'Password is incorrect.', #10
        'Could not find the data kill value' #11
    ]
    print(str('Error #'+str(id)+'|'+errmsgs[id]+'\n'))