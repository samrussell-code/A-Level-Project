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
        if colourkey == -1: #if colourkey is set to -1, it will set itself to the colour at the top left of the image
            colourkey = image.get_at((0,0))
        image.set_colorkey(colourkey, RLEACCEL)
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
    def update(self):
        '''
        update()
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

class Chimp(pygame.sprite.Sprite):
    """
    Chimp
    moves a pygame sprite across the screen. it can spin the monkey when it is punched.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect =LoadImage('chimp.bmp', -1)
        screen = pygame.display.get_surface() #gets the size of the display canvas as a viable area.
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = False
    def update(self):
        """
        update()
        walk or spin, depending on the monkeys state.
        """
        if self.dizzy:
            self._Spin()
        else:
            self._Walk()
    def _Walk(self): #_method suggests a protected method only to be used by the chimp class.
        """
        _walk()
        move the monkey across the screen, and turn at the ends.
        """
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or \
                    self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.rect = newpos
    def _Spin(self):
        """
        _spin()
        spin the monkey image.
        """
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)
    def IsPunched(self):
        """
        punched()
        this will cause the monkey to start spinning
        """
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


def main():
    pygame.init()
    screen=pygame.display.set_mode((468,60)) #get display size.
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(0)

    background=pygame.Surface(screen.get_size()) #creates a surface based on screen size.
    background=background.convert()
    background.fill((250,250,250))

    if pygame.font: #creates a font object as the title, renders it into the surface object.
        font=pygame.font.Font(None,36)
        text=font.render('Pummel The Chimp, And Win $$$',1,(10,10,10))
        textpos=text.get_rect(centerx=background.get_width()/2)
        background.blit(text,textpos) #blit is the final push (paste) of an object onto a surface.

    screen.blit(background, (0,0)) #creates the background on the overarching screen surface.
    pygame.display.flip() #flip updates a display that is idle.

    whiffSound=LoadSound('whiff.wav')
    punchSound=LoadSound('punch.wav')
    chimp=Chimp()
    fist=PlayerFist()
    allsprites=pygame.sprite.RenderPlain((fist,chimp)) #sprite group RenderPlain() draws all the sprites it contains into the surface. 
    clock=pygame.time.Clock() #clock helps track time.

    while True:
        clock.tick(60) #setting a maximum framerate for the game.

        for event in pygame.event.get(): #handling every possible input by calling each subroutine respective to the player inputs.
            if event.type==QUIT:
                return
            elif event.type==KEYDOWN and event.key==K_ESCAPE:
                return
            elif event.type==MOUSEBUTTONDOWN:
                if fist.Punch(chimp):
                    punchSound.play()
                    chimp.IsPunched()
                else:
                    whiffSound.play()
            elif event.type==MOUSEBUTTONUP:
                fist.Unpunch()

        allsprites.update()

        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()

if __name__=='__main__':
    main()