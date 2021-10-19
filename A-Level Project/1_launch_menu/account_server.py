def REGISTER_ACCOUNT(inf):
    username,password=inf
    print(username,password)
    return
def LOGIN_ACCOUNT(inf):
    username,password=inf
    print(username,password)
    return
def ERROR_CATCH(id):
    errmsgs=[
        'Unknown error',
        'Unsupported opcode from client'
    ]
    print(str('Error #'+str(id)+'|'+errmsgs[id]+'\n'))
    return

recv_opcode=8
recv_operand=('John Smith','password123')

REGISTER_ACCOUNT(recv_operand) if recv_opcode==0 else LOGIN_ACCOUNT(recv_operand) if recv_opcode==1 else ERROR_CATCH(1)


