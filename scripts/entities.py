import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, jumpamount, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) # pos is position
        self.size = size
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.velocity = [0,0] # updated every frame based on acceleration
        self.speed = 1.5
        self.canJump = True
        self.JumpsLeft = jumpamount

        print(self.size)
        print(self.game.assets['player'].get_size())

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

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

        if self.collisions['down']:
            self.canJump = True

    def render(self, surfc): #surfc is surface
        surfc.blit(self.game.assets['player'], self.pos)