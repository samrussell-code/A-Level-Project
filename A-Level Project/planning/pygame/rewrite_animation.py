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

