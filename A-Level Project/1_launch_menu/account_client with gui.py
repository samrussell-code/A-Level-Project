from err import ERR_CATCH
from tkinter import *
import winsound
from functools import partial
from cryptography.hazmat.primitives import hashes
import os, socket, threading
class LaunchWindow(Tk):
    def __init__(self):
        super().__init__()
        self.WIDTH,self.HEIGHT=1920,1080
        self.title('Tank Game Launcher')
        self.geometry('1888x1062+0+0')
        self.minsize(640,360)
        self.config(bg='#464646')
        #self.iconbitmap('assets//jack.ico')
        self.mediumFont=('Calibri Light',15)
        self.inputFont=('Calibri Light',10)
        self.titleFont=('Cambria Math',35)
        self.gameTitleLabel=Label(text='TANK GAME',bg='#464646',fg='#eeeeee',font=self.titleFont)
        self.usernameLabel=Label(text='Username',bg='#464646',fg='#eeeeee',font=self.mediumFont)
        self.usernameEntry=Entry(bg='#eeeeee',fg='#464646',font=self.inputFont)
        self.passwordLabel=Label(text='Password',bg='#464646',fg='#eeeeee',font=self.mediumFont)
        self.passwordEntry=Entry(bg='#eeeeee',fg='#464646',show='•',font=self.inputFont)
        self.loginButton=Button(text='Login',bg='#eeeeee',fg='#464646',font=self.mediumFont,command=partial(self.ContactServer,1))
        self.registerButton=Button(text='Register',bg='#eeeeee',fg='#464646',font=self.mediumFont,command=partial(self.ContactServer,0))
        # relx = relx - 1/2 of relwidth
        # rely = rely - 1/2 of relheight
        #SET UP RELATIVE POSITIONS OF OBJECTS IN LOGIN SCREEN
        self.gameTitleLabel.place(relx=24/64,rely=3/40,relwidth=1/4,relheight=1/15)
        self.usernameLabel.place(relx=7/16,rely=7/40,relwidth=1/8,relheight=1/30)
        self.usernameEntry.place(relx=7/16,rely=9/40,relwidth=1/8,relheight=1/20)
        self.passwordLabel.place(relx=7/16,rely=14/40,relwidth=1/8,relheight=1/30)
        self.passwordEntry.place(relx=7/16,rely=16/40,relwidth=1/8,relheight=1/20)
        self.loginButton.place(relx=5/16,rely=28/40,relwidth=1/16,relheight=1/30)
        self.registerButton.place(relx=29/48,rely=28/40,relwidth=1/16,relheight=1/30)
        self.update()
    def ContactServer(self,opcode):
        username=self.usernameEntry.get()
        password=self.passwordEntry.get()
        print(username,password)
        try:
            password_token=self.EncryptPassword(password)
            print(password_token)
        except:
            ERR_CATCH(5)
        #with open('client//username.txt','w') as file: file.write(username);file.close()
        #with open('client//authtoken.txt','w') as file: file.write(password_token);file.close()
        self.SEND_DATA(opcode,[username,password_token])
    def SEND_DATA(self,opcode,data_list):
        data=str(opcode)
        for item in data_list: data+='||'+item #formatting data to be sent
        connection=self.CreateConnection()
        connection.send(data.encode())
    def CreateConnection(self):
        socketObject=socket.socket()
        port=25520
        try:
            socketObject.connect(('tank.servegame.com', port))
            return socketObject
        except:
            ERR_CATCH(8)
    def EncryptPassword(self,password):
        token=(hashes.Hash(hashes.SHA512()))
        token.update((password).encode())
        token=token.finalize()
        token=str(token)[2:-1]
        return token    
    def update(self):
        if self.CheckWindowChange(self.WIDTH)==True:
            self.UpdateFontSize(self.gameTitleLabel,self.titleFont)
            self.UpdateFontSize(self.usernameLabel,self.mediumFont)
            self.UpdateFontSize(self.usernameEntry,self.inputFont)
            self.UpdateFontSize(self.passwordLabel,self.mediumFont)
            self.UpdateFontSize(self.passwordEntry,self.inputFont)
            self.UpdateFontSize(self.loginButton,self.inputFont)
            self.UpdateFontSize(self.registerButton,self.inputFont)
        self.after(100,self.update)
    def CheckWindowChange(self,width):
        return True if self.WIDTH!=self.winfo_width() else False
    def UpdateFontSize(self,widget,font):
        width=self.winfo_width()
        fontName,fontSize=font
        fontSize=round((fontSize/1280)*width)
        widget.config(font=(fontName,fontSize))
window=LaunchWindow()
window.mainloop()