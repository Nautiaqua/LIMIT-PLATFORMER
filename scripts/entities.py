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
        self.anim_timer = 0
        self.anim_index = 0
        self.anim_speed = 0.18  # Lower = faster
        self.facing_right = True
        self.walk_right = self.game.assets['walk_right']
        self.walk_left = self.game.assets['walk_left']
        self.jump_right = self.game.assets['jump_right']
        self.jump_left = self.game.assets['jump_left']
        self.jump_phase = 0  # 0: looking up, 1: up, 2: falling, 3: landing
        self.jump_anim_lock = 0  # Timer to hold the landing squish




        self.coyote_timer = 0
        self.coyote_time_max = 0.2 # THIS IS IN SECONDS.

        print(self.size)
        print(self.game.assets['player'].get_size())

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, dt, tilemap, movement=(0, 0),):
        # Handle vertical motion for jump phases
        if not self.collisions['down']:  # In the air
            if self.velocity[1] < -0.5:  # Going up
                self.jump_phase = 1
            elif self.velocity[1] > 0.5:  # Falling
                self.jump_phase = 2
        else:
            if self.jump_phase in [1, 2]:  # Just landed
                self.jump_phase = 3
                self.jump_anim_lock = 0.05  # Show landing frame for 0.15 sec
            elif self.jump_anim_lock > 0:
                self.jump_anim_lock -= dt
                if self.jump_anim_lock <= 0:
                    self.jump_phase = 0  # Reset to idle

        self.is_jumping = self.jump_phase in [1, 2, 3]



        # Determine direction
        if movement[0] > 0:
            self.facing_right = True
        elif movement[0] < 0:
            self.facing_right = False

        # Animation frame control
        if movement[0] != 0:  # Only animate when moving
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(self.walk_right)
        else:
            self.anim_index = 0  # Reset to idle frame when not moving

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

        for tile in tilemap.tiles_around(self.pos):
            if tile['type'] in KILL_TILES:
                self.die = True
            else:
                pass

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


    def render(self, surfc):
        if self.is_jumping:
            if self.facing_right:
                current_image = self.jump_right[self.jump_phase]
            else:
                current_image = self.jump_left[self.jump_phase]
        else:
            if self.facing_right:
                current_image = self.walk_right[self.anim_index]
            else:
                current_image = self.walk_left[self.anim_index]

        surfc.blit(current_image, self.pos)



