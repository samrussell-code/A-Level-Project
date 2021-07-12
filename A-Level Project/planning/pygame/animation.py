import os, sys
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
        print(filename)
        frameList.append(pygame.image.load(str('planning/pygame/imagedata/')+str(filename)))
    return frameList

class PlayerTank(pygame.sprite.Sprite):
    '''
    PlayerTank
    Methods:
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tankmovingframeList=CreateFrameList('tank-moving') #collects all the images for the tank into a dictionary
        self.tankidleframeList=CreateFrameList('tank-idle')
        self.index=0
        self.isIdle=True
        #create a subroutine that has a parameter of a list containing the desired frame collection
        #on update, check the state of the tank to see if it is idle
        #use the idle list if idle, and the moving list if not idle
    def Animate(self,frameList,slowness):
        self.index+=1
        if self.index>=(len(frameList))*slowness:
            self.index=0
        self.image=frameList[self.index//slowness]
        self.rect=self.image.get_rect()
    def update(self):
        '''
        update()
        updates playertank every frame
        '''
        self.Animate(self.tankmovingframeList,144) if self.isIdle==True else self.Animate(self.tankmovingframeList,10)
        pos = (960,540)
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
    allsprites=pygame.sprite.RenderPlain((tank)) #sprite group RenderPlain() draws all the sprites it contains into the surface. 
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
            elif event.type==KEYUP and event.key==K_d:
                tank.isIdle=True

        allsprites.update()
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()
    


if __name__=='__main__':
    main()