import os, sys, random, math
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

class Bullet(AnimatedSprite):
    def __init__(self):
        super().__init__()
        self.idleframeList=CreateFrameList('bullet-idle')
        self.isMoving=False
        self.pos=1920/6,1080-1080/100
    def DoMaths_(self,initialposition):
        initialpositionx,initialpositiony=initialposition
        horizontal_velocity=250
        vertical_velocity=0
        newpositionx=(horizontal_velocity/144)+initialpositionx
        newpositiony=(vertical_velocity/144)+initialpositiony
        if newpositionx<2000 and newpositionx>0 and newpositiony<1080 and newpositiony>0:
            return newpositionx,newpositiony
        else:
            return initialpositionx,initialpositiony
    def update(self):
        self.Animate(self.idleframeList,144)
        self.image=pygame.transform.scale(self.image,(50,50))
        if self.isMoving==True:
            self.pos=self.DoMaths_(self.pos)
        self.rect.center=self.pos


class MouseObject(AnimatedSprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface([10,10])
        self.image.fill('#7C898B')
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
    bullet=Bullet()
    mouse=MouseObject()
    allsprites=pygame.sprite.RenderPlain((bullet,mouse)) #sprite group RenderPlain() draws all the sprites it contains into the surface. 
    clock=pygame.time.Clock() #clock helps track time.

    while True:
        clock.tick(144) #setting a maximum framerate for the animation.
        for event in pygame.event.get():
            if event.type==QUIT:
                return
            elif event.type==KEYDOWN and event.key==K_ESCAPE:
                return
            elif event.type==KEYDOWN and event.key==K_d:
                bullet.isMoving=True       
            elif event.type==KEYUP and event.key==K_d:
                bullet.isMoving=False     


        allsprites.update()
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()
    

if __name__=='__main__':
    main()
