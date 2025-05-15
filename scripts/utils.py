import pygame

BASE_IMG_PATH = 'data/sprites/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((174, 166, 145))
    return img