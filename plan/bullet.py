import os, sys, random
from math import *
import pygame
from pygame.locals import *
from planning.pygame.animation import AnimatedSprite
import time
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
        self.Animate(self.empty,60)
    def update(self):
        if self.isIdle==False:
            if self.age<self.LIFESPAN:
                print(self.age,self.LIFESPAN)
                self.age+=1
                self.Animate(self.animationList,self.FRAMERATE)
                self.rect.center=self.relativePos
            else:
                self.DoNothing()
                self.isIdle=True
        else:
            self.age=0
            self.isIdle=True
            self.DoNothing()
            
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
        self.FRAMERATE=144 #this value affects the speed at which the program runs
        self.isMoving=False
        self.pos=1920/2,1080/2 #the bullet's starting position unless otherwise specified
        self.velocity,self.angle,self.count=0,0,0 #setting up variable to be used later
        self.maximumBounces=2
        self.Animate(self.idleframeList,60) #animates itself with the idle images
        self.bboxx,self.bboxy=self.image.get_size() #sets up the initial collision box
        self.bounceNumber=1
        self.xDirection=3
        self.particle=Particle('bullet-particle',60,0.64,self.pos)#creates the particle that will follow
        
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
        vMovement=-(vMovement)+(((9.81)*(time)**2)/2) #modifies vertical velocity based off time, horizontal movement should be constant.
        terminalVelocity=3000
        vMovement=terminalVelocity if abs(vMovement)>terminalVelocity else vMovement
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
    '''
    MouseObject(AnimatedSprite)
    Class that represents the users mouse.
    '''
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
    framerate=144
    bullet=Bullet()
    bullet.FRAMERATE=framerate
    mouse=MouseObject()
    allsprites=pygame.sprite.RenderPlain((bullet,bullet.particle,mouse)) #sprite group RenderPlain() draws all the sprites it contains into the surface. 
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
