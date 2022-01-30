from err import ERR_CATCH
from tkinter import *
import winsound
from functools import partial
from cryptography.hazmat.primitives import hashes
import os, socket, threading
import pygame, pygame_gui
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
        self.smallFont=('Cambria Math',10)
        self.titleFont=('Cambria Math',35)
        self.gameTitleLabel=Label(text='TANK GAME',bg='#464646',fg='#eeeeee',font=self.titleFont)
        self.usernameLabel=Label(text='Username',bg='#464646',fg='#eeeeee',font=self.mediumFont)
        self.usernameEntry=Entry(bg='#eeeeee',fg='#464646',font=self.inputFont)
        self.passwordLabel=Label(text='Password',bg='#464646',fg='#eeeeee',font=self.mediumFont)
        self.passwordEntry=Entry(bg='#eeeeee',fg='#464646',show='•',font=self.inputFont)
        self.infoLabel=Label(text='',bg='#464646',fg='#eeeeee',font=self.smallFont,anchor=CENTER)
        self.loginButton=Button(text='Login',bg='#eeeeee',fg='#464646',font=self.mediumFont,command=partial(self.UpdateClient,1))
        self.registerButton=Button(text='Register',bg='#eeeeee',fg='#464646',font=self.mediumFont,command=partial(self.UpdateClient,0))
        # relx = relx - 1/2 of relwidth
        # rely = rely - 1/2 of relheight
        #SET UP RELATIVE POSITIONS OF OBJECTS IN LOGIN SCREEN
        self.gameTitleLabel.place(relx=24/64,rely=3/40,relwidth=1/4,relheight=1/15)
        self.usernameLabel.place(relx=7/16,rely=7/40,relwidth=1/8,relheight=1/30)
        self.usernameEntry.place(relx=7/16,rely=9/40,relwidth=1/8,relheight=1/20)
        self.passwordLabel.place(relx=7/16,rely=14/40,relwidth=1/8,relheight=1/30)
        self.passwordEntry.place(relx=7/16,rely=16/40,relwidth=1/8,relheight=1/20)
        self.infoLabel.place(relx=107/256,rely=22/40,relwidth=1/6,relheight=1/20)
        self.loginButton.place(relx=5/16,rely=28/40,relwidth=1/16,relheight=1/30)
        self.registerButton.place(relx=29/48,rely=28/40,relwidth=1/16,relheight=1/30)
        self.update()
    def UpdateClient(self,opcode):
        self.ContactServer(opcode)
        operation=self.RECV_DATA()
        print(operation)
        if operation[0]=='0': #recieving the server accepting entry 
            self.infoLabel.config(text=operation[1])
            self.usernameEntry.delete(0,'end')
            self.passwordEntry.delete(0,'end')

    def ContactServer(self,opcode):
        username=self.usernameEntry.get()
        password=self.passwordEntry.get()
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
        self.connection=self.CreateConnection()
        self.connection.send(data.encode())
    def RECV_DATA(self):
        operation=(self.connection.recv(65536).decode()).split('||')
        return operation
    def CreateConnection(self):
        socketObject=socket.socket()
        port=25520
        try:
            socketObject.connect(('SHA-E8-DT-018', port))
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



#####################################################
##pygame.init()
##
##pygame.display.set_caption('Quick Start')
##window_surface = pygame.display.set_mode((800, 600))
##
##background = pygame.Surface((800, 600))
##background.fill(pygame.Color('#000000'))
##
##is_running = True
##
##while is_running:
##
##    for event in pygame.event.get():
##        if event.type == pygame.QUIT:
##            is_running = False
##
##    window_surface.blit(background, (0, 0))
##
##    pygame.display.update()

class PygameWindow():
    def __init__(self,width,height):
        self.rect=pygame.Rect(0,0,width,height)
        self.width,self.height=width,height
        pygame.init()
        self.screen=pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption('Tank Game')
        pygame.mouse.set_visible(1)
        self.foreground=None
        self.background=None
        self.set_foreground('menu_title.png','#ffffff',0.5)
        self.set_background('menu_background.png')
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.foreground, (0,0))
        pygame.display.flip()
        pygame.time.delay(10000)
    def set_background(self, image=None, colourkey=None, scale=1.0):
        ''' image is the name of the image within the imagedata folder, with file type
            colourkey is the alpha value colour if there is transparency in the image.
            scale is the fraction of the screen size that the image should reach.
        '''
        if image:
            self.background=pygame.image.load(str('imagedata/')+str(image)).convert_alpha()
            self.background=pygame.transform.scale(self.background,(round(self.width*scale),round(self.height*scale)))
            self.background.set_colorkey(colourkey)
    def set_foreground(self,image=None, colourkey=None, scale=1.0):
        if image:
            self.foreground=pygame.image.load(str('imagedata/')+str(image)).convert_alpha()
            self.foreground=pygame.transform.scale(self.foreground,(round(self.width*scale),round(self.height*scale)))
            self.foreground.set_colorkey(colourkey)
resX,resY=1280,720
game_window=PygameWindow(resX,resY)    
#####################################################
#launch_window=LaunchWindow()
#launch_window.mainloop()
