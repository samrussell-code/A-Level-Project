from planning.pygame.objects import *

def main():
    screen,background,tank,spritegroup,clock,bullet=GameWindowSetup()
    while True:
        EventChecker(tank,clock,bullet)
        RefreshScreen(screen,spritegroup,background)    

if __name__=='__main__':
    main()
