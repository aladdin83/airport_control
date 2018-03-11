import os
import pygame

lib_path = os.path.abspath(os.path.dirname(__file__))

def load_image(filename):
    full_name = os.path.join(lib_path,'..','data','images', filename)
    try:
        image = pygame.image.load(full_name)
    except pygame.error:
        print ("Cannot load image:"), full_name
        raise (SystemExit, message)

    image = image.convert_alpha()

    return image, image.get_rect()
