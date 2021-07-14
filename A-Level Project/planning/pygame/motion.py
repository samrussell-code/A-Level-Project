import os, sys, random
from math import *
import pygame
from pygame.locals import *
from planning.pygame.animation import AnimatedSprite
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

class Bullet(AnimatedSprite):
    def __init__(self):
        super().__init__()
        self.idleframeList=CreateFrameList('bullet-idle')
        self.isMoving=False
        self.pos=1920/2,1080/2
        self.velocity,self.angle,self.count=0,0,0
        self.framerate=0
        self.Animate(self.idleframeList,self.framerate)
        self.bboxx,self.bboxy=self.image.get_size()
        self.lastStaticPosition=self.pos
        self.bounceNumber=0
        
    def UpdatePosition_(self,initialposition,horizontal_movement,vertical_movement):
        initialpositionx,initialpositiony=initialposition
        newpositionx=(horizontal_movement/self.framerate)+initialpositionx
        newpositiony=(vertical_movement/self.framerate)+initialpositiony
        if newpositionx<1920 and newpositionx>-10 and newpositiony<1010 and newpositiony>-10:
            ignore,angle=self.GetVelocityAngle((newpositionx,newpositiony),(initialpositionx,initialpositiony))
            self.UpdateRotation_(angle)
            return newpositionx,newpositiony
        else:
            if self.bounceNumber>5:
                print('stationary')
                self.isMoving=False
                self.lastStaticPosition=self.pos
                self.bounceNumber=0
            else:
                print('bouncing,',self.bounceNumber)
                self.bounceNumber+=1
                self.count=0
                self.lastStaticPosition=self.pos
                self.UpdateRotation_(90)
                self.velocity=self.velocity/1.5
            return initialpositionx,initialpositiony

    def UpdateRotation_(self,angle):
        originalImage=self.image
        self.image=pygame.transform.rotate(originalImage,angle)
        x,y=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)

    def GetDisplacement_(self,velocity=0.01,angle=0.01,time=0):
        hMovement=velocity*cos(radians(angle))
        vMovement=velocity*sin(radians(angle))
        vMovement=-(vMovement)+(((9.81/2)*(time)**2)/2)
        print(f'''
        velocity = {velocity}
        angle = {angle}
        pos = {self.pos}
        hMovement = {hMovement}
        vMovement = {vMovement}
        ''')
        terminalVelocity=3000
        vMovement=terminalVelocity if vMovement>terminalVelocity else vMovement
        self.pos=self.UpdatePosition_(self.pos,hMovement,vMovement)
        
    def GetVelocityAngle(self,forcePosition,objectPosition):
        dY=forcePosition[1]-objectPosition[1] #y is inversed so a negative y is upwards and a positive y is downwards
        dX=forcePosition[0]-objectPosition[0] #x is not inversed so a negative x is left and positive x is right
        hypotenuse=sqrt((dY**2)+(dX**2)) #this is always positive
        angle=degrees(atan(dY/dX)) if dX!=0 and hypotenuse>10 else 90
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
        self.Animate(self.idleframeList,self.framerate)
        self.image=pygame.transform.scale(self.image,(self.bboxx//5,self.bboxy//5))
        if self.isMoving==True:
            self.GetDisplacement_(self.velocity,self.angle,self.count)
            self.count+=1
            print(self.count)
        else:
            self.count=0
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

def main():
    pygame.init()
    screen=pygame.display.set_mode((1920,1080)) #set display size.
    pygame.display.set_caption('Tank Animation')
    pygame.mouse.set_visible(0)
    background=pygame.Surface(screen.get_size()) #creates a surface based on screen size.
    background=background.convert()
    background.fill((250,250,250))
    screen.blit(background, (0,0)) #creates the background on the overarching screen surface.
    pygame.display.flip() #flip updates a display that is idle.
    framerate=60
    bullet=Bullet()
    bullet.framerate=framerate
    mouse=MouseObject()
    allsprites=pygame.sprite.RenderPlain((bullet,mouse)) #sprite group RenderPlain() draws all the sprites it contains into the surface. 
    clock=pygame.time.Clock() #clock helps track time.

    while True:
        clock.tick(framerate) #setting a maximum framerate for the animation.
        for event in pygame.event.get():
            if event.type==QUIT:
                return
            elif event.type==KEYDOWN and event.key==K_ESCAPE:
                return
            elif event.type==MOUSEBUTTONDOWN and event.button==1 and bullet.isMoving==False:
                bullet.velocity,bullet.angle=bullet.GetVelocityAngle(event.pos,bullet.pos)
                bullet.isMoving=True


        allsprites.update()
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()
    

if __name__=='__main__':
    main()
