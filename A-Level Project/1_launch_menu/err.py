def ERR_CATCH(id):
    errmsgs=[
        'Unknown error.',
        'Unsupported opcode from client.',
        'Account with this username already exists.',
        'Cannot create the database connection.',
        'No valid authtoken bin found.',
        'Could not encrypt password.',
        'No username file found.',
        'Failed to recieve data in thread (buffer size may have been exceeded)',
        'Could not connect to server.'
    ]
    print(str('Error #'+str(id)+'|'+errmsgs[id]+'\n'))