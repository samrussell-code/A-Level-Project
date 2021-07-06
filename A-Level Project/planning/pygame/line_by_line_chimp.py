import os,sys
import pygame
from pygame.locals import *

print('Warning, fonts disabled') if not pygame.font else print('Fonts enabled')
print('Warning, sound disabled') if not pygame.mixer else print ('Sound enabled')

def LoadImage(name, colourkey=None):
    '''
    LoadImage(name, colourkey=None)
    returns the image and the rectangle object created by pygame with the image's quality, when a filename and optional alpha channel key is entered.
    '''
    filename=os.path.join('planning/pygame/imagedata',name)
    try: #tries to load the file and sends an error if the file cannot be opened in image format
        image= pygame.image.load(filename) 
    except pygame.error as message:
        print('Cannot load image:',name)
        raise SystemExit(message)
    image = image.convert() #converts the image file into a new surface object
    if colourkey is not None:
        if colourkey is -1: #if colourkey is set to -1, it will set itself to the colour at the top left of the image
            colourkey = image.get_at((0,0))
        image.set_colourkey(colourkey, RLEACCEL)
    return image, image.get_rect()

def LoadSound(name):
    '''
    LoadSound(name)
    returns the sound in a usable format for pygame
    '''
    class NoneSound:
        '''
        NoneSound
        a spoof of pygame Sound where the .play function only passes. To be used when mixer is not present.
        '''
        def play(self):
            pass
        if not pygame.mixer: #checks import of mixer
            return NoneSound()
        fullname = os.path.join('planning/pygame/imagedata',name) 
        try: #tries to load the file and sends an error if the file cannot be opened in sound format
            sound = pygame.mixer.Sound(fullname)
        except pygame.error as message:
            print('Cannot load sound: ', fullname)
            raise SystemExit(mesage)
        return sound

class PlayerFist(pygame.sprite.Sprite):
    '''
    PlayerFist
    A pygame sprite that follows mouse movement on screen and follows it.
    Methods:
    Punch(target)
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = LoadImage('fist.bmp',-1)
        self.punching=False
    def Update(self):
        '''
        Update()
        moves the fist based on mouse position.
        '''
        pos = pygame.mouse.get_pos()
        self.rect.midtop=pos
        if self.punching:
            self.rect.move_ip(5,10)
    def Punch(self,target):
        '''
        Punch(target)
        returns true if the first collides with a target.
        '''
        if not self.punching:
            self.punching=True
            hitbox=self.rect.inflate(-5,-5)
            return hitbox.colliderect(target.rect)
    def Unpunch(self):
        '''
        Unpunch
        pulls the fist back to position
        '''
        self.punching=False
