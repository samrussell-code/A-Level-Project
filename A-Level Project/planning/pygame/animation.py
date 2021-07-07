import os, sys
import pygame
from pygame.locals import *

def LoadImage(name, colourkey=None,customFileExtension=False):
    '''
    LoadImage(name, colourkey=None,customFileExtension=False)
    returns the image and the rectangle object created by pygame with the image's quality, when a filename and optional alpha channel key is entered.
    custom file extension allows the user to input their own file extension if set to true
    '''
    
    filename=os.path.join('planning/pygame/imagedata',name) if customFileExtension==False else str('planning/pygame/imagedata/'+name)
    try: #tries to load the file and sends an error if the file cannot be opened in image format
        image= pygame.image.load(filename) 
    except pygame.error as message:
        print('Cannot load image:',name)
        raise SystemExit(message)
    image = image.convert() #converts the image file into a new surface object
    if colourkey is not None:
        if colourkey == -1: #if colourkey is set to -1, it will set itself to the colour at the top left of the image
            colourkey = image.get_at((0,0))
        image.set_colorkey(colourkey, RLEACCEL)
    return image, image.get_rect()

def CreateFrameDict(spriteName):
    '''
    CreateFrameList(spriteName)
    Creates a dictionary of images loaded from imagedata under the same prefix
    '''
    loadlist=[]
    for file in os.listdir('planning/pygame/imagedata'):
        if os.path.isfile(os.path.join('planning/pygame/imagedata', file)) and (spriteName+'_') in str(file) and ('.png' in str(file) or '.jpg' in str(file)):
            loadlist.append(file)
    frameDict={}
    for filename in loadlist:
        frameDict.update({filename.split('.')[0]:LoadImage(filename,-1,True)}) #adds the filename without the extension to a list as the key, with the loaded image as the value
    return frameDict

class AnimationHandler:
    def __init__(self,frameDict):
        self.frameDict=frameDict
    def SetIdleFrame(self,filename):
        self.idleFrame=self.frameDict[filename]

class PlayerTank(pygame.sprite.Sprite):
    '''
    PlayerTank
    Methods:

    '''
    def __init__(self,frameDict):
        self.frameDict=frameDict
        animHandler=AnimationHandler(self.frameDict)
        animHandler.SetIdleFrame('tank_1')


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

    tankFrames=CreateFrameDict('tank')
    tank=PlayerTank(tankFrames)



if __name__=='__main__':
    main()