import os, sys, random
import pygame
from math import *
from pygame.locals import *

class AnimatedSprite(pygame.sprite.Sprite):
    '''
    AnimatedSprite(pygame-Sprite)
    My building block for all of my simple sprites.
    Contains the animate method which allows it to shift between different frames in different fashions e.g. random, boomerang, linear
    isIdle (Bool), increasing (Bool)
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.linearIndex=0
        self.boomerangIndex=0
        self.randomIndex=0
        self.isIdle=True     
        self.increasing=True
    def Animate(self,frameList,slowness,animationType='linear'):
        '''
        Animate(frameList,slowness,animationType)
        Animates the sprite with the list input.
        '''
        if animationType=='linear':
            self.linearIndex+=1
            if self.linearIndex>=(len(frameList))*slowness:
                self.linearIndex=0
            try:
                self.image=frameList[self.linearIndex//slowness]
            except:
                self.image=frameList[self.linearIndex]
            self.rect=self.image.get_rect()
        elif animationType=='boomerang':
            if self.boomerangIndex>=(len(frameList))*slowness:
                self.increasing=False;self.boomerangIndex-=1
            elif self.boomerangIndex==0:
                self.increasing=True;self.boomerangIndex+=1
            self.image=frameList[self.boomerangIndex//slowness]
            self.rect=self.image.get_rect()
            self.boomerangIndex=self.boomerangIndex+1 if self.increasing==True else self.boomerangIndex-1
        elif animationType=='random':
            if self.randomIndex>=slowness:
                self.randomImage=random.randint(0,((len(frameList)))-1)
                self.image=frameList[self.randomImage]
                self.rect=self.image.get_rect()
                self.randomIndex=0
            self.randomIndex+=1
            return


class Particle(AnimatedSprite):
    def __init__(self,animationName='null',FRAMERATE=60,lifespan=0.3,parentPos=(-1000,-1000)):
        super().__init__()
        LIFESPAN=round(lifespan*FRAMERATE)
        age=0
        animationList=CreateFrameList(animationName)
        self.isIdle=True
        self.relativePos=parentPos
        self.animationList,self.FRAMERATE,self.LIFESPAN,self.age=animationList,FRAMERATE,LIFESPAN,age
        self.empty=CreateFrameList('nothing')
        self.Animate(self.empty,self.FRAMERATE)
    def DoNothing(self):
        self.Animate(self.empty,60,'boomerang')
    def update(self):
        if self.isIdle==False:
            if self.age<self.LIFESPAN:
                self.age+=1
                self.Animate(self.animationList,self.FRAMERATE)
                self.image=pygame.transform.scale(self.image,(84,84))
                self.rect.topleft=(self.relativePos[0]-40,self.relativePos[1]-20)
            else:
                self.DoNothing()
                self.isIdle=True
        else:
            self.age=0
            self.isIdle=True
            self.DoNothing()


class PlayerTank(AnimatedSprite):
    '''
    PlayerTank
    Methods:
    '''
    def __init__(self):
        super().__init__()
        self.tankmovingframeList=CreateFrameList('tank-moving') #collects all the images for the tank into a dictionary
        self.tankidleframeList=CreateFrameList('tank-idle')
        self.nozzle=TankNozzle()
    def update(self):
        '''
        update()
        updates playertank every frame
        '''
        self.Animate(self.tankmovingframeList,60) if self.isIdle==True else self.Animate(self.tankmovingframeList,10)
        pos = (960,540)
        self.nozzle.relativePos=pos
        self.rect.center=pos

class TankNozzle(AnimatedSprite):
    '''
    TankNozzle(AnimatedSprite)
    The nozzle component spawned by tank on init
    '''
    def __init__(self):
        super().__init__()
        self.movingframeList=CreateFrameList('tanknozzle-moving')
        self.idleframeList=[self.movingframeList[3]];self.boomerangIndex=30
        self.relativePos=0,0
    def update(self):
        self.Animate(self.idleframeList,10) if self.isIdle==True else self.Animate(self.movingframeList,10,'boomerang')
        self.rect.center=self.relativePos

class Bullet(AnimatedSprite):
    '''
    Bullet(AnimatedSprite)
    Object to be spawned by tank that can be moving or stationary, and bounces when colliding with the screen borders. All subroutines inside this object are internal and therefore protected.
    Methods:
    UpdatePosition_(),UpdateRotation_(),GetDisplacement_(),GetVelocityAngle()
    '''
    def __init__(self):
        super().__init__()
        self.idleframeList=CreateFrameList('bullet-idle')
        self.COEFFICIENT_RESTITUTION=0.4 #this value affects the bouncing power of the bullet against objects it collides with.
        self.FRAMERATE=60 #this value affects the speed at which the program runs
        self.isMoving=False
        self.pos=1920/2,1080/2 #the bullet's starting position unless otherwise specified
        self.velocity,self.angle,self.count=0,0,0 #setting up variable to be used later
        self.maximumBounces=2
        self.Animate(self.idleframeList,60) #animates itself with the idle images
        self.bboxx,self.bboxy=self.image.get_size() #sets up the initial collision box
        self.bounceNumber=1
        self.xDirection=3
        self.particle=Particle('bullet-particle',60,0.4,self.pos)#creates the particle that will follow
        self.particle.FRAMERATE=5
        
    def UpdatePosition_(self,initialposition,horizontal_movement,vertical_movement): #takes the current position and updates it based on the horizontal and vertical components included
        '''
        UpdatePosition_()
        Takes the current position and updates it based on the horizontal and vertical components also input.
        Returns the updated position if successful, or original position if unsuccessful.
        Also decides if the object should stop moving upon a collision, or if it should bounce.
        '''
        initialpositionx,initialpositiony=initialposition
        newpositionx=(horizontal_movement/self.FRAMERATE)+initialpositionx
        newpositiony=(vertical_movement/self.FRAMERATE)+initialpositiony
        if newpositionx<1920 and newpositionx>-10 and newpositiony<1010 and newpositiony>-10: #if the updated position is within the bounding box
            ignore,angle=self.GetVelocityAngle((newpositionx,newpositiony),(initialpositionx,initialpositiony)) #gets the angle generated from the gradient of the change in positions
            self.UpdateRotation_(angle) #updates the objects image to be rotated correctly
            return newpositionx,newpositiony #returns the new position
        else:
            #creating a bounce particle
            self.particle.relativePos=self.pos
            self.particle.isIdle=False
            
            if self.bounceNumber>self.maximumBounces: #if the object has already bounced more times than the maximum
                self.isMoving=False #stops the movement cycle and resets the number of bounces
                self.bounceNumber=1
                self.particle.isIdle=True
            else: #if the object still needs to bounce
                self.bounceNumber+=1
                self.count=0
                if newpositionx<-9 or newpositionx>1919: #detects if it is a horizontal bounce
                    self.bounceNumber=3
                    self.velocity=-self.velocity #reverses the velocity in while maintaining the angle, essentialy rotating by 180 degrees
                else:
                    self.UpdateRotation_(self.angle) #sets the new rotation to the angle the object hit the floor at
                self.velocity=self.velocity/(1/self.COEFFICIENT_RESTITUTION) #decreases the new velocity by the restitution coefficient
            return initialpositionx,initialpositiony

    def UpdateRotation_(self,angle):
        originalImage=self.image #saves the previous image so that image degradation doesnt occur while image is rotating
        self.image=pygame.transform.rotate(originalImage,angle) #sets the new image to a copy of the original image at a different angle
        x,y=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center=(x,y) #makes sure the image is still centered in the correct position

    def GetDisplacement_(self,velocity=0.01,angle=0.01,time=0):
        hMovement=velocity*cos(radians(angle)) # seperates the magnitudal velocity into its horizontal and vertical components
        vMovement=velocity*sin(radians(angle))
        vMovement=-(vMovement)+(((9.81/2)*(time)**2)/2) #modifies vertical velocity based off time, horizontal movement should be constant.
        terminalVelocity=3000
        vMovement=terminalVelocity if vMovement>terminalVelocity else vMovement
        self.pos=self.UpdatePosition_(self.pos,hMovement,vMovement)
        
    def GetVelocityAngle(self,forcePosition,objectPosition):
        dY=forcePosition[1]-objectPosition[1] #y is inversed so a negative y is upwards and a positive y is downwards
        dX=forcePosition[0]-objectPosition[0] #x is not inversed so a negative x is left and positive x is right
        self.xDirection=dX
        hypotenuse=sqrt((dY**2)+(dX**2)) #this is always positive
        angle=degrees(atan(dY/dX)) if (dX!=0 and hypotenuse>2) else 0 if dX>0 else 180 
        if dY<0 and dX>0:#0 to 90
            angle=abs(angle)
        elif dY<0 and dX<0: #90 to 180
            angle=90-abs(angle)+90
        elif dY>0 and dX<0: #180 to 270
            angle=abs(angle)+180
        elif dY>0 and dX>0: #270 to 360
            angle=90-abs(angle)+270
        hypotenuse=hypotenuse*2.5
        return hypotenuse,angle
        
    def update(self):
        self.Animate(self.idleframeList,self.FRAMERATE) #always animating the bullet.
        self.image=pygame.transform.scale(self.image,(self.bboxx//5,self.bboxy//5)) #scales the bullet image down by 5
        if self.isMoving==True:
            self.GetDisplacement_(self.velocity,self.angle,self.count)
            self.count+=1
        else:
            self.count=0
            self.UpdateRotation_(180) if self.xDirection<-1 else self.UpdateRotation_(0) if self.xDirection>1 else self.UpdateRotation_(270) #changes the direction of the stationary bullet depending on its last velocity.
        self.rect=self.image.get_rect()
        self.rect.center=self.pos


class MouseObject(AnimatedSprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface([10,10])              
    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.rect=self.image.get_rect()
        self.rect.center=self.pos


def CreateFrameList(stateName):
    '''
    CreateFrameList(spriteName)
    Creates a dictionary of images loaded from imagedata under the same prefix
    '''
    loadlist=[]
    for file in os.listdir('planning/pygame/imagedata'):
        if os.path.isfile(os.path.join('planning/pygame/imagedata', file)) and (stateName+'_') in str(file) and ('.png' in str(file) or '.jpg' in str(file)):
            loadlist.append(file)
    frameList=[]
    for filename in loadlist:
        frameList.append(pygame.image.load(str('planning/pygame/imagedata/')+str(filename)))
    return frameList
def GameWindowSetup():
    '''
    GameWindowSetup() sets up the pygame window with the tank and all its components.
    '''
    pygame.init()
    screen=pygame.display.set_mode((1920,1080)) #set display size.
    pygame.display.set_caption('Tank Animation')
    pygame.mouse.set_visible(1)
    background=pygame.Surface(screen.get_size()) #creates a surface based on screen size.
    background=background.convert()
    background.fill((250,250,250))
    screen.blit(background, (0,0)) #creates the background on the overarching screen surface.
    pygame.display.flip() #flip updates a display that is idle.
    tank=PlayerTank()
    bullet=Bullet()
    allsprites=pygame.sprite.RenderPlain((tank,tank.nozzle,bullet,bullet.particle)) #sprite group RenderPlain() draws all the sprites it contains into the surface. 
    clock=pygame.time.Clock() #clock helps track time.
    return screen,background,tank,allsprites,clock,bullet
def EventChecker(tank,clock,bullet):
    clock.tick(60) #setting a maximum framerate for the animation.
    for event in pygame.event.get():
        if event.type==QUIT:
            return
        elif event.type==KEYDOWN and event.key==K_ESCAPE:
            return
        elif event.type==KEYDOWN and event.key==K_d:
            tank.isIdle=False            
        elif event.type==KEYDOWN and event.key==K_a:
            tank.isIdle=False
        elif event.type==KEYDOWN and event.key==K_w:
            tank.nozzle.isIdle=False
            tank.nozzle.increasing=True
        elif event.type==KEYDOWN and event.key==K_s:
            tank.nozzle.isIdle=False
            tank.nozzle.increasing=False
        elif event.type==KEYUP and event.key==K_w:
            tank.nozzle.isIdle=True
            tank.nozzle.idleframeList=[tank.nozzle.image]
        elif event.type==KEYUP and event.key==K_s:
            tank.nozzle.isIdle=True
            tank.nozzle.idleframeList=[tank.nozzle.image]
        elif event.type==KEYUP and event.key==K_d:
            tank.isIdle=True            
        elif event.type==KEYUP and event.key==K_a:
            tank.isIdle=True
        elif event.type==MOUSEBUTTONDOWN and event.button==1 and bullet.isMoving==False:
            bullet.velocity,bullet.angle=bullet.GetVelocityAngle(event.pos,bullet.pos)
            bullet.isMoving=True
def RefreshScreen(screen,spritegroup,background):
    spritegroup.update()
    screen.blit(background, (0,0))
    spritegroup.draw(screen)
    pygame.display.flip()