import os, sys, random
import pygame
from pygame.locals import *

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

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.linearIndex=0
        self.boomerangIndex=0
        self.randomIndex=0
        self.isIdle=True     
        self.increasing=True
    def Animate(self,frameList,slowness,animationType='linear'):
        if animationType=='linear':
            self.linearIndex+=1
            if self.linearIndex>=(len(frameList))*slowness:
                self.linearIndex=0
            self.image=frameList[self.linearIndex//slowness]
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

class TankNozzle(AnimatedSprite):
    def __init__(self):
        super().__init__()
        self.movingframeList=CreateFrameList('tanknozzle-moving')
        self.idleframeList=[self.movingframeList[3]];self.boomerangIndex=30
        self.relativePos=0,0
    def update(self):
        self.Animate(self.idleframeList,10) if self.isIdle==True else self.Animate(self.movingframeList,10,'boomerang')
        self.rect.center=self.relativePos

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
        self.Animate(self.tankmovingframeList,144) if self.isIdle==True else self.Animate(self.tankmovingframeList,10)
        pos = (960,540)
        self.nozzle.relativePos=pos
        self.rect.center=pos
        
def main():
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
    allsprites=pygame.sprite.RenderPlain((tank,tank.nozzle)) #sprite group RenderPlain() draws all the sprites it contains into the surface. 
    clock=pygame.time.Clock() #clock helps track time.

    while True:
        clock.tick(144) #setting a maximum framerate for the animation.
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

        allsprites.update()
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()
    

if __name__=='__main__':
    main()
