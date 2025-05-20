import pygame
import os

BASE_IMG_PATH = 'data/sprites/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)): # os.dir takes a path and gives us all the files in that path
        images.append(load_image(path + '/' + img_name))
        print(img_name)
    return images
def load_animation_frames(path):
    frames = []
    for i in range(1, 5):  # 5 frames: frame1.png to frame5.png
        full_path = BASE_IMG_PATH + path + f'/frame{i}.png'
        img = pygame.image.load(full_path).convert_alpha()
        img.set_colorkey((0, 0, 0))  # Optional: make black transparent like others
        frames.append(img)
    return frames