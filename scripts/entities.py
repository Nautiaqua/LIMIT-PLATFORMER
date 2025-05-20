import pygame
from scripts.tilemap import Tilemap
from scripts.tilemap import KILL_TILES

class PhysicsEntity:
    def __init__(self, game, e_type, jumpamount, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) # pos is position
        self.size = size
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.velocity = [0,0] # updated every frame based on acceleration
        self.speed = 1.5
        self.canJump = False
        self.JumpsLeft = jumpamount
        self.die = False

        self.coyote_timer = 0
        self.coyote_time_max = 0.2 # THIS IS IN SECONDS.

        print(self.size)
        print(self.game.assets['player'].get_size())

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, dt, tilemap, movement=(0, 0),):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.dt = dt

        frame_movement = (movement[0] * self.speed + self.velocity[0], movement[1] + self.velocity [1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: #checks if ur moving to the right
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0 : #checks if ur moving LEFT
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0: #checks if ur moving to the right
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0 : #checks if ur moving LEFT
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.top

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        # coyote timer! what this does is allow the player to jump a  few frames after falling off. you'll see this in celeste.
        if self.collisions['down']:
            self.coyote_timer = self.coyote_time_max
        else:
            self.coyote_timer -= self.dt

        self.canJump = (self.collisions['down'] or self.coyote_timer > 0) and self.JumpsLeft > 0

        growth = 0
        entity_rect = self.rect()        
        self.player_center = (self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)
        for tile in tilemap.tiles_around(self.player_center):
            if tile['type'] in KILL_TILES:
                spike_rect = pygame.Rect(tile['pos'][0] * tilemap.tile_size - growth, tile['pos'][1] * tilemap.tile_size - growth, tilemap.tile_size + growth, tilemap.tile_size + growth)
                if entity_rect.colliderect(spike_rect):
                    self.die = True
                   

    def currentTileGet(self, activeTilemap, xPosition, yPosition):
        xTile = int((xPosition + self.size[0] / 2) // activeTilemap.tile_size)
        yTile = int((yPosition + self.size[1] / 2) // activeTilemap.tile_size)
        tilePos = str(xTile) + ";" + str(yTile)
        currentTile = activeTilemap.tilemap.get(tilePos)
        return currentTile
    
    def currentTilePos(self, activeTilemap, xPosition, yPosition):
        xCurTile = int((xPosition + self.size[0] / 2) // activeTilemap.tile_size)
        yCurTile = int((yPosition + self.size[1] / 2) // activeTilemap.tile_size)
        cTilePos = str(xCurTile) + ";" + str(yCurTile)
        return cTilePos


    def render(self, surfc): #surfc is surface
        surfc.blit(self.game.assets['player'], self.pos)