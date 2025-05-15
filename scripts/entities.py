import pygame

class PhysicsEntity:
    def __init__ (self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) # pos is position
        self.size = size
        self.velocity = [0,0] # updated every frame based on acceleration

    def update(self, movement=(0, 0)): 
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity [1])

        self.pos[0] += frame_movement[0] # updates x position
        self.pos[1] += frame_movement[1] # updates y position

    def render(self, surfc): #surfc is surface
        surfc.blit(self.game.assets['player'], self.pos)