from ast import Sub, excepthandler
from cgitb import text
from msilib.schema import Font
from re import L
from turtle import screensize
from err import ERR_CATCH
from tkinter import *
from functools import partial
from cryptography.hazmat.primitives import hashes
import socket, threading, pygame, pygame_gui

class LaunchWindow(Tk):
    def __init__(self):
        super().__init__()
        self.WIDTH,self.HEIGHT=1920,1080
        self.title('Tank Game Launcher')
        self.geometry('1280x720+0+0')
        self.minsize(640,360)
        self.config(bg='#464646')
        self.iconbitmap('imagedata/icon.jpg')
        self.mediumFont=('Calibri Light',15)
        self.inputFont=('Calibri Light',10)
        self.smallFont=('Cambria Math',10)
        self.titleFont=('Cambria Math',35)
        self.resolutionChoice=StringVar(value=('256x144','512x288','640x360','960x540','1152x648','1280x720','1664x936','1920x1080','2048x1152','2560x1440','3840x2160'))
        self.gameTitleLabel=Label(text='TANK GAME',bg='#464646',fg='#eeeeee',font=self.titleFont)
        self.resListLabel=Label(text='Resolution:',bg='#464646',fg='#eeeeee',font=self.smallFont)
        self.resListbox=Listbox(self,listvariable=self.resolutionChoice,height=1,font=self.inputFont,selectmode='SINGLE')
        self.usernameLabel=Label(text='Username',bg='#464646',fg='#eeeeee',font=self.mediumFont)
        self.usernameEntry=Entry(bg='#eeeeee',fg='#464646',font=self.inputFont)
        self.passwordLabel=Label(text='Password',bg='#464646',fg='#eeeeee',font=self.mediumFont)
        self.passwordEntry=Entry(bg='#eeeeee',fg='#464646',show='•',font=self.inputFont)
        self.infoLabel=Label(text='',bg='#464646',fg='#eeeeee',font=self.smallFont,anchor=CENTER)
        self.loginButton=Button(text='Login',bg='#eeeeee',fg='#464646',font=self.mediumFont,command=partial(self.UpdateClient,1))
        self.registerButton=Button(text='Register',bg='#eeeeee',fg='#464646',font=self.mediumFont,command=partial(self.UpdateClient,0))
        self.resListbox.select_set(3)
        self.gameTitleLabel.place(relx=24/64,rely=3/40,relwidth=1/4,relheight=1/15)
        self.resListLabel.place(relx=14/16,rely=3/80,relwidth=1/16,relheight=1/30)
        self.resListbox.place(relx=14/16,rely=3/40,relwidth=1/16,relheight=1/8)
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
        #print('updateclient recieved',operation)
        if operation[0]=='0': #recieving the server accepting entry 
            self.infoLabel.config(text=operation[1])
            self.usernameEntry.delete(0,'end')
            self.passwordEntry.delete(0,'end')
            if operation[2]=='1':#operation[2] is a true/false success/fail
                resStr=self.resListbox.get(self.resListbox.curselection())
                res=resStr.split('x')
                self.destroy()
                resX,resY=int(res[0]),int(res[1])
                if resX==0 or resY==0:
                    resX,resY=1280,720
                game_window=PygameWindow(resX,resY,self.username,socket.gethostname())

    def ContactServer(self,opcode):
        self.username=self.usernameEntry.get()
        password=self.passwordEntry.get()
        try:
            password_token=self.EncryptPassword(password)
        except:
            ERR_CATCH(5)
        #with open('client//username.txt','w') as file: file.write(username);file.close()
        #with open('client//authtoken.txt','w') as file: file.write(password_token);file.close()
        self.SEND_DATA(opcode,[self.username,password_token])
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
            self.UpdateFontSize(self.resListLabel,self.smallFont)
            self.UpdateFontSize(self.resListbox,self.inputFont)
        self.after(100,self.update)
    def CheckWindowChange(self,width):
        return True if self.WIDTH!=self.winfo_width() else False
    def UpdateFontSize(self,widget,font):
        width=self.winfo_width()
        fontName,fontSize=font
        fontSize=round((fontSize/1280)*width)
        widget.config(font=(fontName,fontSize))

class PygameWindow():
    def __init__(self,width,height,username,ip):
        self.username,self.ip=username,ip
        self.rect=pygame.Rect(0,0,width,height)
        self.FRAMERATE=144
        self.screenwidth,self.screenheight=width,height
        pygame.init()
        self.screen=pygame.display.set_mode(self.rect.size)
        self.UIManager=pygame_gui.UIManager((self.screenwidth,self.screenheight))
        pygame.display.set_caption('Tank Game')
        icon=pygame.image.load('imagedata/icon.jpg')
        pygame.display.set_icon(icon)
        pygame.mouse.set_visible(1) #the difference between a sprite and an image is that multiple sprites can use the same image, but image only has to be loaded once this way.
        self.imageDict={
        'bullet-idle_1':Image('bullet-idle_1.png','#ffffff',0.025,self.screenwidth,self.screenheight),
        'menu_background':Image('menu_background.png',None,1,self.screenwidth,self.screenheight),
        'menu_title':Image('menu_title.png','#ffffff',0.3,self.screenwidth,self.screenheight),
        'ground1':Image('ground1.png',None,0.25,self.screenwidth,self.screenheight),
        'ground2':Image('ground2.png',None,0.25,self.screenwidth,self.screenheight),
        'ground3':Image('ground3.png',None,0.25,self.screenwidth,self.screenheight),
        'tank1':Image('tank1.png','#ffffff',0.05,self.screenwidth,self.screenheight),
        'tank2':Image('tank2.png','#ffffff',0.05,self.screenwidth,self.screenheight),
        'tank3':Image('tank3.png','#ffffff',0.05,self.screenwidth,self.screenheight),        
        'enemytank1':Image('enemytank1.png','#ffffff',0.05,self.screenwidth,self.screenheight),
        'enemytank2':Image('enemytank2.png','#ffffff',0.05,self.screenwidth,self.screenheight),
        'enemytank3':Image('enemytank3.png','#ffffff',0.05,self.screenwidth,self.screenheight)
        }
        self.selectAudio={
        'bgamb':pygame.mixer.music.load('mp3/bgamb.mp3'),
        'fire':pygame.mixer.music.load('mp3/fire.mp3')
        }
        pygame.mixer.music.set_volume(0.05)
        self.background=Sprite(self.screen,self.imageDict['menu_background'],True,0.5,0.5) #sprite of image menu_background, with no collisions, in the centre of screen.
        self.title_object=Sprite(self.screen,self.imageDict['menu_title'],False,0.5,0.15)
        self.title_object.animations.update({'Bounce':VectorAnimation([
        '300 0 -0.1', #syntax FRAMES X_update Y_update
        '500 0 0',
        '300 0 0.1',
        '500 0 0'])})# creates a simple motion animation called bounce, for the foreground sprite.
        
        create_button_layout=self.button_layout(0.1,0.4,0.2,0.1,False)
        self.create_button=pygame_gui.elements.UIButton(relative_rect=create_button_layout,text='Create Lobby',manager=self.UIManager) #these rects have set sizes

        join_button_layout=self.button_layout(0.1,0.6,0.2,0.1,False)
        self.join_button=pygame_gui.elements.UIButton(relative_rect=join_button_layout,text='Join Lobby',manager=self.UIManager)

        name_entry_layout=self.button_layout(0.6,0.4,0.2,0.1,False)
        self.name_entry=pygame_gui.elements.UITextEntryLine(relative_rect=name_entry_layout,manager=self.UIManager)

        password_entry_layout=self.button_layout(0.6,0.6,0.2,0.1,False)
        self.password_entry=pygame_gui.elements.UITextEntryLine(relative_rect=password_entry_layout,manager=self.UIManager)

        self.SPRITE_RENDER_LIST=[self.background,self.title_object] #every sprite to be rendered should go in this list, sprite on top is end of list.
        self.last_time=0
        self.input_list=[0,0,0,0,'kill||']
        #FORMAT A,D,MOUSECOORDINATES,LMB
        self.old_inf=['6', '10', '10', '10', '10', '10', '10', '10', '10']
        self.update()

    def update(self):
        self.is_running=True
        while self.is_running:
            pygame.time.wait(round(1000/self.FRAMERATE))
            self.manage_events()
            self.calculate_delta_time()
            self.UIManager.update(self.deltatime)
            self.blit_objects()

            if self.GAME_START==True:
                #e.g.['6', '0', '0', '0', '0', '0', '0', '0', '0']
                if len(self.GameManager.server_response)==9: #if no data has collided
                    inf=self.GameManager.server_response
                    self.old_inf=inf
                else: #data collision avoidance
                    inf=self.old_inf
                #print('inf:',inf)
                #print('ORIGINAL TANK PX/PY',self.tank.pX,self.tank.pY)
                self.tank.RefreshPosition(inf[1],inf[2])
                #print('NEW TANK PX/PY',self.tank.pX,self.tank.pY)
                self.bullet.RefreshPosition(inf[3],inf[4])
                #print('NEW BULLET PX/PY',self.bullet.pX,self.bullet.pY)
                self.enemytank.RefreshPosition(inf[5],inf[6])
                #print('NEW ENEMYTANK PX/PY',self.enemytank.pX,self.enemytank.pY)
                self.opponentbullet.RefreshPosition(inf[7],inf[8])
                #print('NEW OPPONENTBULLET PX/PY',self.opponentbullet.pX,self.opponentbullet.pY)

          

    def button_layout(self,offsetx,offsety,sizex=-1,sizey=-1,auto=True):
        if auto==True: #size of button should be automatic
            return pygame.Rect((round(offsetx*self.screenwidth),round(offsety*self.screenheight)),(-1,-1))
        else:
            return pygame.Rect(round(offsetx*self.screenwidth),round(offsety*self.screenheight),round(sizex*self.screenwidth),round(sizey*self.screenheight))
    
    def convert_to_relative_space(self,pos):
        '''Takes absolute pixel positions, in a tuple, as parameter
           Returns relative screen space positions, in a tuple
        '''
        px,py=pos
        px/=self.screenwidth
        py/=self.screenheight
        return (px,py)

    def calculate_delta_time(self):
        ''' Gets the time since window intialised, then subtracts that from the previous call on time, to get the change in time, deltatime, then saves the last call.
            Delta time is in ms. Use this value for physics calculations so motion is not tied to framerate but instead time.
        '''
        self.newtime=(pygame.time.get_ticks())
        self.deltatime=self.newtime-self.last_time
        self.last_time=self.newtime

    def manage_events(self):
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.is_running=False
                if event.type==pygame_gui.UI_BUTTON_PRESSED:
                    self.name=self.name_entry.get_text()
                    self.password=self.password_entry.get_text() #grabs the lobby name and password entered
                    if event.ui_element==self.create_button:
                        print('create')
                        self.GAME_START()
                    elif event.ui_element==self.join_button:
                        print('join')
                        self.GAME_FIND()
                if self.GAME_START==True: #these are checked only during game runtime
                    #[a,d,m1]
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_a:
                            #print('left')
                            self.input_list[0]=1                            
                        elif event.key==pygame.K_d:
                            #print('right')
                            self.input_list[1]=1
                    if event.type==pygame.KEYUP:
                        if event.key==pygame.K_a:
                            #print('left up')
                            self.input_list[0]=0
                        if event.key==pygame.K_d:
                            #print('right up')
                            self.input_list[1]=0
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        if event.button==1:
                            #print(left mouse down)
                            self.input_list[2]=self.convert_to_relative_space(pygame.mouse.get_pos())
                            self.input_list[3]=1
                    elif event.type==pygame.MOUSEBUTTONUP:
                        if event.button==1:
                            #print(left mouse up)
                            self.input_list[2]=0
                            self.input_list[3]=0               
                self.UIManager.process_events(event)

    def GAME_START(self): #PLAYER 1 stuff here
        ''' Clears the list of items to render on the screen, then draws lobby title text, either waiting for player 2, or player 2 found
        '''
        self.UIManager.clear_and_reset();self.SPRITE_RENDER_LIST=[]#empties the screen
        self.GameManager=GameManager(self.ip,self.username,2,self.name,self.password)#2 for create, 3 for join
        lobby_title_text_layout=self.button_layout(0.3,0.3,0.4,0.05,False)
        lobby_title_text=pygame_gui.elements.UITextBox(html_text=f'''<b><u>{self.GameManager.lobby_name}: Waiting for opponent... </u></b>''',relative_rect=lobby_title_text_layout,manager=self.UIManager)
        opcode,opponentName=self.PLAYER_JOIN()
        self.SpawnPlayers(opponentName,1)

    def GAME_FIND(self): #PLAYER 2 stuff here
        self.UIManager.clear_and_reset();self.SPRITE_RENDER_LIST=[]
        self.GameManager=GameManager(self.ip,self.username,3,self.name,self.password)
        opcode,opponentName=self.PLAYER_JOIN()
        self.SpawnPlayers(opponentName,2)

    def PLAYER_JOIN(self):
        '''final subroutine to run before synchronisation of the game will begin
        '''
        result=self.GameManager.CheckServerResponse()
        while result==None:
            pass #FIX HERE
        self.UIManager.clear_and_reset();self.SPRITE_RENDER_LIST=[]#empties the screen
        return (result[0],result[1])
    
    def SpawnPlayers(self,opponentname,playerType=1):
        if playerType==1:
            self.bullet=Sprite(self.screen,self.imageDict['bullet-idle_1'],False,0.1,0.6)
            self.opponentbullet=Sprite(self.screen,self.imageDict['bullet-idle_1'],False,0.8,0.6)
            self.tank=Sprite(self.screen,self.imageDict['tank1'],False,0.1,0.6)
            self.enemytank=Sprite(self.screen,self.imageDict['enemytank1'],False,0.8,0.6)
            self.SPRITE_RENDER_LIST.extend([self.bullet,self.opponentbullet,self.tank,self.enemytank])
        elif playerType==2:
            self.bullet=Sprite(self.screen,self.imageDict['bullet-idle_1'],False,0.8,0.6)
            self.opponentbullet=Sprite(self.screen,self.imageDict['bullet-idle_1'],False,0.1,0.6)
            self.tank=Sprite(self.screen,self.imageDict['tank1'],False,0.8,0.6)
            self.enemytank=Sprite(self.screen,self.imageDict['enemytank1'],False,0.1,0.6)
            self.SPRITE_RENDER_LIST.extend([self.bullet,self.opponentbullet,self.tank,self.enemytank])
        print('waiting for ground texture code...')
        result=self.GameManager.CheckServerResponse()#server now sends out type of ground to use in game
        floor=Sprite(self.screen,self.imageDict[result[1]],False,0.5,0.9)
        self.SPRITE_RENDER_LIST.append(floor)
        print('ground texture set up complete.')
        self.selectAudio['bgamb']
        pygame.mixer.music.play()        
        threading.Thread(target=self.PingServer,daemon=True).start()  
        
    def PingServer(self):
        result=self.GameManager.CheckServerResponse() #takes another result so that the game can begin updating positions
        self.GAME_START=True
        threading.Thread(target=self.SendToServer,daemon=True).start()
        while self.GAME_START==True:
            result=self.GameManager.CheckServerResponse()

    def SendToServer(self):
        '''
        every loop, collect the pending inputs from a list of possible inputs
        then send the list of inputs to the server, for the server to convert into motion
        '''
        while self.GAME_START==True:
            self.GameManager.SendData(self.input_list)
            #print('sent input:',self.input_list)
        

    def blit_objects(self):
        pygame.draw.rect(self.screen,(255,255,255),pygame.Rect(0,0,self.screenwidth,self.screenheight))
        for sprite in self.SPRITE_RENDER_LIST:
            for animation in sprite.animations.values(): #updates every animation, for every sprite
                update_x,update_y=animation.UpdateAnimation(self.deltatime)
                sprite.pX+=(update_x*self.deltatime)
                sprite.pY+=(update_y*self.deltatime)
            #print(self.SPRITE_RENDER_LIST.index(sprite))
            try:
                self.screen.blit(sprite.image,(sprite.pX,sprite.pY)) #renders every sprite
            except:
                #print('did not blit sprite',self.SPRITE_RENDER_LIST.index(sprite))
                pass
            if sprite.isCollider==False:
                if sprite.collider.debugBBox==True:  #renders the colliders for each sprite that has debug set to true
                    self.screen.blit(sprite.collider.surface,(sprite.pX,sprite.pY))
        self.UIManager.draw_ui(self.screen)
        pygame.display.flip()

class Image():
    '''imagename is the filename

       colourkey is the alpha colour

       scaleX/scaleY is the scale of the image to be used by default by a sprite
    '''
    #scale should be a percentage of the screen size to scale, so 100 (self.imagewidth / self.screenwidth)
    #
    def __init__(self,imagename=None,colourkey=None,scaleX=1.0,screenwidth=1280,screenheight=720):
        self.imagename,self.colourkey,self.scaleX=imagename,colourkey,scaleX
        if imagename!=None:
            self.image=pygame.image.load(str('imagedata/')+str(self.imagename)).convert_alpha()
            self.imagewidth,self.imageheight=self.image.get_size() #gets the size before the scale
            newwidth,newheight=round(self.imagewidth*(scaleX/100)*screenwidth),round(self.imageheight*(scaleX/100)*screenwidth)
            self.image=pygame.transform.scale(self.image,(newwidth,newheight))
            self.imagewidth,self.imageheight=self.image.get_size() #gets the size after the scale
            self.image.set_colorkey(colourkey)

class Sprite():
    def __init__(self,screen,image=None,isCollider=False,pivotX=0,pivotY=0):
        '''Screen is the pygame screen to be used.

            Image is the currently rendered image object for the sprite to use.

            collider is bool, if sprite is already a collider then it does not need its own collisions.

            spawnX and spawnY are the initial position of the sprite.
        '''
        self.screen=screen
        self.image,self.imagewidth,self.imageheight,self.sX,self.pX,self.pY=image.image,image.imagewidth,image.imageheight,image.scaleX,(pivotX*screen.get_width())-(image.imagewidth/2),(pivotY*screen.get_height())-(image.imageheight/2)
        self.screen.blit(self.image,(self.pX,self.pY))
        self.animations={}
        self.isCollider=isCollider
        #print('sprite of :',self.image,self.pX,self.pY)
        if self.image!=None and isCollider==False:
            self.collider=BoundingBox(self.screen,self.imagewidth,self.imageheight,self.pX,self.pY,False)
    def RefreshPosition(self,iX,iY):
        self.pX=(float(iX)*self.screen.get_width())-(self.imagewidth/2)
        self.pY=(float(iY)*self.screen.get_height())-(self.imageheight/2)

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

class VectorAnimation():
    def __init__(self,instructions):
        self.tick=0
        self.current_instruction=0
        self.instruction_progress=0
        self.instructions=instructions
        self.total_instructions=len(self.instructions)-1
        self.instruction_duration=int((self.instructions[self.current_instruction]).split(' ')[0])
    #FIX THIS - take the original position of the object before the animation, so the object can reset position on loop
    def UpdateAnimation(self,deltatime):
        '''
        Returns a tuple coordinate to be applied to the current position of the object being animated.
        Should be called every frame.
        '''
        #strange deltatime bug causing increasing position offset of an animation, the lower the framerate. additionally, when window is moved, frame in the animation pauses but time does not, so on next time calculation, large distance is moved.
        #print('instructions=',self.instructions,'current instruction=',self.current_instruction,'instruction length',self.instruction_duration, 'total instructions',self.total_instructions)
        if int(self.instruction_progress)<int(self.instruction_duration):#if current instruction is not yet finished
            self.instruction_progress+=deltatime #increases the progress on the instruction by the change in time since last call.
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

class GameManager():
    def __init__(self,ip,username,opcode,name,password):
        '''Creates a connection to the server, and asks the server to connect to a lobby
        '''
        self.socketObject=socket.socket()
        self.port=25520
        self.username=username
        self.name=name
        self.connection=self.CreateConnection()
        self.lobby_name=name
        self.lobby_password=password
        create_lobby_data=self.FORMAT_DATA(opcode,[username,self.lobby_password,self.lobby_name])
        self.connection.send(create_lobby_data.encode()) #OPCODE 2 IS CREATE LOBBY, OPCODE 3 IS JOIN LOBBY
        self.time=0

    def CreateConnection(self):
        try:
            self.socketObject.connect(('tank.servegame.com', self.port))
            return self.socketObject
        except:
            ERR_CATCH(8)

    def CheckServerResponse(self):
            self.server_response=(self.socketObject.recv(65536).decode()).split('||')
            #find the position in the response list where #kill# is found, then cut the list before this point
            try:
                kill_pos=self.server_response.index('kill')
                self.server_response=self.server_response[:kill_pos] #slices off the end of the recieved data after kill is found
            except:
                #ERR_CATCH(11)
                pass
            
           # print(len(self.server_response))#debug
            #print('recieved',self.server_response)
            return self.server_response

    def SendData(self,data):
        ''' Sends the input from the client side to the server, for example any user inputs such as an attack, the angle of the attack, move key pressed.
            The server will take this data and do the maths on its end, then return the position vectors each item should be at, which the client can
            blit. I predict this will lose smooth motion of objects, so to counter this the velocity vector of each item could be passed, so the client
            can make an estimation of the path of the object and then the distance teleported should not be so great if connection is lost.
            TLDR; lower latency, but potentially unstable motion

            Or, make it so that the time taken between server responses is kept, e.g. 60ms. Then the object moves at a calculated velocity to its
            target position, so that it takes 60ms to reach it. Then, if the server is averaging a stable response time, the motion will be smooth,
            and only teleport when ping is unstable. This one will double latency as you have to wait for the next position to exist before moving object.
            TLDR; fully smooth motion at the cost of double latency

            Client will only update the frame using a thread that is only called after a server response (e.g. the framerate is tied to the server response, but not the in game time)

            FORMAT for data to be sent should be as follows, this means that all collisions need to be calculated on server side, the tank, bullet would each be a seperate object
            This data is purely for rendering an interpretation of the scene on the client, and not for calculating the physics:
            *userid*
            objectname||object_position||object_rotation
            tank||110,323||0.5,0.2||10
            bullet||116,323||object_rotation
            FORMAT for purely sending off inputs:
            *userid*
            mouse_world_position
            inputname||on/off
            inputname||on/off
            
        '''
        data=self.FORMAT_DATA(4,data)#OPCODE4 is game data
        self.connection.send(data.encode())
    def FORMAT_DATA(self,opcode,data_list):
        data=str(opcode)
        for item in data_list: data+='||'+str(item)
        return data

launch_window=LaunchWindow()
launch_window.mainloop()