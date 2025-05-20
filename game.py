import sys
import pygame
import json
import os

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("LimitJump!") # title for the window
        self.screen = pygame.display.set_mode((960, 864), vsync=1) # Initialize screen.
        self.surface = pygame.Surface((320, 288))
        self.clock = pygame.time.Clock() #initialize clocc

        self.movement = [False, False]
        self.noJumps = False
        self.levelReset = False

        # this handles the level loading.
        self.levelPath = "data/levels/"
        self.currentLevel = "hub" + ".json"
        # i have no clue why i dont use current level ngl

        # this loads in all the assets from the data folder.
        self.assets = {
            'block': load_images('tiles/block'),
            'sign': load_images('tiles/sign'),
            'spike': load_images('tiles/spike'),
            'door' : load_images('tiles/door'),
            'exitdoor': load_images('tiles/exitdoor'),
            'numbers': load_images('tiles/numbers'),
            'player': load_image('player/player_base.png')
        }

        # this part is for the jump popup thingymajigy
        self.font = pygame.font.SysFont('Arial', 20)
        self.titlefont = pygame.Font('data/fonts/Pixellari.ttf', 40)
        self.startfont = pygame.font.SysFont('Arial', 15)
        self.startfont2 = pygame.font.SysFont('Arial', 25)
        self.popup_text = ''
        self.popup_timer = 120 #this is based on frames.

        self.tilemap = Tilemap(self, tile_size = 16) # for the sake of clarity.

        self.player = PhysicsEntity(self, 'player', json.load(open(self.levelPath + self.currentLevel)).get("maxjumps", 1), (50, 50), (15, 15))
        self.cTileType = 'None'

        self.load_level("hub.json", 32, 257)
        self.show_title_screen()

    def show_title_screen(self):
        while True:
            self.surface.fill((174, 166, 145))

            start_time = pygame.time.get_ticks()
            fade_surface = pygame.Surface(self.screen.get_size()).convert()
            fade_surface.fill((174, 166, 145))

            title_contain = "LimitJump!"
            start_contain = "Press SPACE to start"

            title_text = self.titlefont.render(title_contain, True, (78, 63, 42))
            start_text = self.startfont.render(start_contain, True, (78, 63, 42))
            titlerect = title_text.get_rect(center=(160, 140))
            startrect = start_text.get_rect(center=(160, 240))
            self.surface.blit(title_text, titlerect)
            self.surface.blit(start_text, startrect)

            scaled = pygame.transform.scale(self.surface, (960, 864))
            self.screen.blit(scaled, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        while True:
                            now = pygame.time.get_ticks()
                            elapsed = now - start_time
                            if elapsed > 500:
                                break

                            alpha = min(255, int((elapsed / 500) * 255))
                            fade_surface.set_alpha(alpha)

                            self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_size()), (0, 0))
                            self.screen.blit(fade_surface, (0, 0))

                            pygame.display.update()
                        self.show_controls()
                        return

                        

            self.clock.tick(60)
        
    def show_controls(self):
        while True:
            self.surface.fill((174, 166, 145))
 
            start_time = pygame.time.get_ticks()
            fade_surface = pygame.Surface(self.screen.get_size()).convert()
            fade_surface.fill((174, 166, 145))

            title_text = self.startfont2.render("Controls:", True, (78, 63, 42))
            start_text = self.startfont.render("W and D or Left and Right Arrow Keys to Move\nZ or L to interact with doors\nSPACE to Jump\nR to reset the level\n\nPress SPACE again to continue", True, (78, 63, 42))
            titlerect = title_text.get_rect(center=(160, 70))
            startrect = start_text.get_rect(center=(160, 150))

            self.surface.blit(title_text, titlerect)
            self.surface.blit(start_text, startrect)

            scaled = pygame.transform.scale(self.surface, (960, 864))
            self.screen.blit(scaled, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        while True:
                            now = pygame.time.get_ticks()
                            elapsed = now - start_time
                            if elapsed > 500:
                                break

                            alpha = min(255, int((elapsed / 500) * 255))
                            fade_surface.set_alpha(alpha)

                            self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_size()), (0, 0))
                            self.screen.blit(fade_surface, (0, 0))

                            pygame.display.update()
                        return
                        

            self.clock.tick(60)

    def screen_wipe(self, duration=500, reverse=False):
        fade_surface = pygame.Surface(self.screen.get_size()).convert()
        fade_surface.fill((0, 0, 0))
        start_time = pygame.time.get_ticks()

        while True:
            now = pygame.time.get_ticks()
            elapsed = now - start_time
            if elapsed > duration:
                break

            alpha = min(255, int((elapsed / duration) * 255))
            fade_surface.set_alpha(alpha)

            self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_size()), (0, 0))
            self.screen.blit(fade_surface, (0, 0))

            pygame.display.update()
            self.clock.tick(60)

    def load_level(self, levelName, spawnX, spawnY, transition = False):
        if (transition):
            self.screen_wipe()
        self.tilemap.load(self.levelPath + levelName)
        self.noJumps = False
        # PLAYER POS TOOK SO FKIN LONG TO PROPERLY ASSIGN
        self.player.pos = [spawnX, spawnY]
        self.player.JumpsLeft = json.load(open(self.levelPath + levelName)).get("maxjumps", 1)
        self.player.velocity = [0, 0]
        self.player.coyote_timer = 0
        self.currentLevel = levelName
        self.respawnX = spawnX
        self.respawnY = spawnY

    def hubappear(self):
        self.isHub = json.load(open(self.levelPath + self.currentLevel)).get("ishub", False)

        self.hubFont = pygame.font.SysFont('Arial', 12)
        self.hubText = 'this is your jump count.\ndo not let it run out!\nif it does, you fail the level!\n                v'
        self.hubTextTimer = 120
        
        # debug code lol
        '''
        if self.isHub:
            print("ITS THE HUB AREA")
        '''
            
        if self.hubTextTimer > 0 and self.isHub:
            hubText_surface = self.hubFont.render(self.hubText, True, (0, 0, 0))
            hubText_surface.set_alpha(100)
            text_rect = hubText_surface.get_rect(center=(181, 109)) 
            self.surface.blit(hubText_surface, text_rect)

    def run(self):

        while True:
            self.deltatime = self.clock.tick(60) / 1000
            self.surface.fill((174, 166, 145)) # fill the screen with the chosen color.

            self.levelReset = False
            # This is the initial jump count
            self.strJump = str(self.player.JumpsLeft)
            if (self.player.JumpsLeft == 255):
                self.popup_text = "∞"
                self.popup_timer = 60
            else:
                self.popup_text = self.strJump
                self.popup_timer = 60

            self.hubappear()
            
            self.tilemap.render(self.surface) #renders tilemap BEFORE player
            self.player.update(self.deltatime, self.tilemap, (self.movement[1] - self.movement[0], 0))  #moves player left and right
            self.player.render(self.surface) #renders player


            # renders the jump counter
            if self.popup_timer > 0:
                popup_surface = self.font.render(self.popup_text, True, (0, 0, 0))
                popup_surface.set_alpha(100)
                text_rect = popup_surface.get_rect(center=(160, 140)) 
                self.surface.blit(popup_surface, text_rect)
                self.popup_timer -= 1

            if (self.player.die == True):
                print("DYING")
                self.load_level(self.currentLevel, self.respawnX, self.respawnY)
                self.player.die = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # quits game, duh
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT: # d is left, a is right
                        self.movement[0] = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        # basically enables infinite jumps if jumps is set to 255
                        if (self.player.canJump == True and self.player.JumpsLeft == 255):
                            self.player.velocity[1] = -3
                            self.player.canJump = False
                            self.player.coyote_timer = 0

                        # now THIS is the code for the name of the game
                        if (self.player.canJump == True and self.player.JumpsLeft > 0):
                            self.player.velocity[1] = -3
                            self.player.canJump = False
                            self.player.JumpsLeft -= 1
                            self.player.coyote_timer = 0

                        if (self.noJumps == True):
                            self.load_level(self.currentLevel, self.respawnX, self.respawnY)
                        if (self.player.JumpsLeft == 0):
                            self.noJumps = True
                    if event.key == pygame.K_r:
                        self.load_level(self.currentLevel, self.respawnX, self.respawnY)

                    # Interaction for loading levels
                    if event.key == pygame.K_z or event.key == pygame.K_l:
                        cTile = self.player.currentTileGet(self.tilemap, self.player.pos[0], self.player.pos[1])
                        if (cTile != None):
                            print(cTile['type'])

                            if (self.isHub == True and cTile['type'] == 'exitdoor'):
                                print("level chosen")

                                # The game will crash if the level doesn't exist.
                                if (self.player.currentTilePos(self.tilemap, self.player.pos[0], self.player.pos[1]) == '17;16'):
                                    # Test Level (End Door)
                                    self.load_level("test.json", 50, 50,True)
                                if (self.player.currentTilePos(self.tilemap, self.player.pos[0], self.player.pos[1]) == '7;16'):
                                    # First Level
                                    self.load_level("level1.json", 50, 50, True)
                                if (self.player.currentTilePos(self.tilemap, self.player.pos[0], self.player.pos[1]) == '9;16'):
                                    # Second Level
                                    self.load_level("level2.json", 50, 50, True)
                                if (self.player.currentTilePos(self.tilemap, self.player.pos[0], self.player.pos[1]) == '11;16'):
                                    # Third Level
                                    self.load_level("level3.json", 50, 50, True)
                                if (self.player.currentTilePos(self.tilemap, self.player.pos[0], self.player.pos[1]) == '13;16'):
                                    # Fourth Level
                                    self.load_level("level4.json", 50, 50, True)
                                if (self.player.currentTilePos(self.tilemap, self.player.pos[0], self.player.pos[1]) == '15;16'):
                                    # Fifth Level
                                    self.load_level("level5.json", 50, 50, True)
                                

                            # exits the level if interacting with an exitdoor thats NOT in hub.
                            if (self.isHub == False and cTile['type'] == 'exitdoor'):
                                print("LEVEL EXIT")
                                self.load_level("hub.json", 32, 257, True)

                    # debugger controls. these keybinds are here to help for debugging the game.
                    if event.key == pygame.K_p:
                        print(self.player.pos)
                    if event.key == pygame.K_i:
                        print(self.player.currentTilePos(self.tilemap, self.player.pos[0], self.player.pos[1]))

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            scaled = pygame.transform.scale(self.surface, (960, 864))
            self.screen.blit(scaled, (0, 0))

            pygame.display.update()


Game().run()