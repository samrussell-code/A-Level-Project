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
        self.screenwidth,self.screenheight=width,height
        pygame.init()
        self.screen=pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption('Tank Game')
        pygame.mouse.set_visible(1)
        self.imageDict={'menu_background':Image('menu_background.png',None,10,10),'menu_title':Image('menu_title.png','#ffffff',2,2)} # all loaded images are stored in dictionary
        # the difference between a sprite and an image is that multiple sprites can use the same image, but image only has to be loaded once this way.
        self.background=Sprite(self.screen,self.imageDict['menu_background'],True,0.5,0.5)
        self.foreground=Sprite(self.screen,self.imageDict['menu_title'],False,0.5,0.1)
        self.foreground.animations.update({'Bounce':Animation([
        '30 0 -0.1', #syntax FRAMES X_update Y_update
        '200 0 0',
        '30 0 0.1',
        '200 0 0'])})# creates a simple motion animation called bounce.

        self.RENDER_LIST=[self.background,self.foreground]
        pygame.display.flip()
        self.update()
    def update(self):
        while True:
            self.blit_objects()
    def blit_objects(self):
        for sprite in self.RENDER_LIST:
            for animation in sprite.animations.values(): #updates every animation, for every sprite
                update_x,update_y=animation.UpdateAnimation()
                sprite.pX+=update_x
                sprite.pY+=update_y
            self.screen.blit(sprite.image,(sprite.pX,sprite.pY)) #renders every sprite
            if sprite.isCollider==False:
                if sprite.collider.debugBBox==True:  #renders the colliders for each sprite that has debug set to true
                    self.screen.blit(sprite.collider.surface,(sprite.pX,sprite.pY))
        pygame.display.flip()

class Image():
    '''imagename is the filename

       colourkey is the alpha colour

       scaleX/scaleY is the scale of the image to be used by default by a sprite
    '''
    def __init__(self,imagename=None,colourkey=None,scaleX=1.0,scaleY=1.0):
        self.imagename,self.colourkey,self.scaleX,self.scaleY=imagename,colourkey,scaleX,scaleY
        if imagename!=None:
            self.image=pygame.image.load(str('imagedata/')+str(self.imagename)).convert_alpha()
            self.imagewidth,self.imageheight=self.image.get_size() #gets the size before the scale
            self.image=pygame.transform.scale(self.image,(round(self.imagewidth*scaleX),round(self.imageheight*scaleY)))
            self.imagewidth,self.imageheight=self.image.get_size() #gets the size after the scale
            self.image.set_colorkey(colourkey)

class Sprite():
    def __init__(self,screen,image=None,isCollider=False,pivotX=0,pivotY=0):
        '''Screen is the pygame screen to be used.

            Image is the currently rendered image object for the sprite to use.

            collider is bool, if sprite is already a collider then it does not need its own collisions.

            spawnX and spawnY are the initial position of the sprite.
        '''
        self.image,self.imagewidth,self.imageheight,self.sX,self.sY,self.pX,self.pY=image.image,image.imagewidth,image.imageheight,image.scaleX,image.scaleY,(pivotX*screen.get_width())-(image.imagewidth/2),(pivotY*screen.get_height())-(image.imageheight/2)
        screen.blit(self.image,(self.pX,self.pY))
        self.animations={}
        self.isCollider=isCollider
        if self.image!=None and isCollider==False:
            self.collider=BoundingBox(screen,self.imagewidth,self.imageheight,self.pX,self.pY,True)

class BoundingBox():
    '''Class that handles all collisions, used by the Sprite class.
    '''
    def __init__(self,screen,width,height,pX=0,pY=0,debugBBox=False):
        self.width,self.height,self.pX,self.pY,self.debugBBox,self.screen=width,height,pX,pY,debugBBox,screen
        self.topLeft=(0+pX,0+pY)
        self.topRight=(self.width+pX,0+pY)
        self.botLeft=(0+pX,self.height+pY)
        self.botRight=(self.width+pX,self.height+pY)
        if self.debugBBox==True:
            self.ShowCollisions()
    def ShowCollisions(self):
        self.colliderRect=pygame.Rect(self.topLeft[0],self.topLeft[1],self.botRight[0],self.botRight[1])
        self.surface=pygame.Surface((self.topRight[0]-self.topLeft[0],self.botLeft[1]-self.topRight[1]))
        self.surface.set_alpha(100)
        self.surface.fill((255,0,0))
        self.screen.blit(self.surface,(self.topLeft[0],self.topLeft[1]))

class Animation():
    def __init__(self,instructions):
        self.tick=0
        self.current_instruction=0
        self.instruction_progress=0
        self.instructions=instructions
        self.total_instructions=len(self.instructions)-1
        self.instruction_duration=int((self.instructions[self.current_instruction]).split(' ')[0])

    def UpdateAnimation(self):
        '''
        Returns a tuple coordinate to be applied to the current position of the object being animated.
        Should be called every frame.
        '''
        #print('instructions=',self.instructions,'current instruction=',self.current_instruction,'instruction length',self.instruction_duration, 'total instructions',self.total_instructions)
        if int(self.instruction_progress)<int(self.instruction_duration):#if current instruction is not yet finished
            self.instruction_progress+=1
            to_send_x=float((self.instructions[self.current_instruction]).split(' ')[1]) #gets the y coord
            to_send_y=float((self.instructions[self.current_instruction]).split(' ')[2]) #gets the x coord
            return to_send_x,to_send_y
        else:
            if self.current_instruction<self.total_instructions: #if all instructions are not finished
                self.current_instruction+=1               
            else:
                #print('reset animation / animation ended.')
                self.current_instruction=0
            self.instruction_duration=(self.instructions[self.current_instruction]).split(' ')[0] #gets the duration of the newly loaded instruction
            self.instruction_progress=0 #resets the progress for the new instruction 
            return 0,0


    def GetPositionUpdate(self):
        self.instructions[self.current_instruction]

        self.last_x,self.last_y=self.new_x,self.new_y
        return self.new_x,self.new_y
resX,resY=1280,720
game_window=PygameWindow(resX,resY)
#####################################################
#launch_window=LaunchWindow()
#launch_window.mainloop()
