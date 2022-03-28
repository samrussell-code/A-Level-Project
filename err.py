def ERR_CATCH(id):
    '''
    Returns a console print statement with the error number referenced.

    Simple script for debugging my code.
    '''
    errmsgs = [
        'Unknown error.',  # 0
        'Unsupported opcode from client.',  # 1
        'Account with this username already exists.',  # 2
        'Cannot create the database connection.',  # 3
        'No valid authtoken file found.',  # 4
        'Could not encrypt password.',  # 5
        'No username file found.',  # 6
        'Failed to recieve data in thread.',  # 7
        'Could not connect to server.',  # 8
        'User with that name does not exist.',  # 9
        'Password is incorrect.',  # 10
        'Could not find the data kill value',  # 11
        'Data collision error, abandoning this packet',  # 12
        'Client has closed the program, ending session',  # 13
        'Recursion error reached' #14
    ]
    print(str('Error #'+str(id)+'|'+errmsgs[id]+'\n'))
