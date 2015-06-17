import glob
from Assets.Utility.spritesheet import Spritesheet
class CharacterGenerator():
    def __init__(self, main, pygame):
        #Add the pygame module to the global variable list
        globals()["pygame"] = pygame
        globals()["main"] = main
        self.rpgace = r"D:\SteamLibrary\steamapps\common\RPGVXAce"
        self.char_pos = self.rpgace+r"\rtp\Graphics\Characters\\"
        self.actors = Spritesheet(self.char_pos+"Actor1.png", 96,128)
        self.current_actor = self.actors.split(0,0)
        self.start_time = pygame.time.get_ticks()
        
    def run(self, events):
        frame = ((pygame.time.get_ticks()-self.start_time)/150)%4
        if frame == 3: frame = 1
        main.screen.blit(self.current_actor.tiles[0][frame], (0,0))
        main.screen.blit(self.current_actor.tiles[1][frame], (0,32))
        main.screen.blit(self.current_actor.tiles[2][frame], (0,64))
        main.screen.blit(self.current_actor.tiles[3][frame], (0,96))
