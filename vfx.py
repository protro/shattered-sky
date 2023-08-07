import pygame
from pygame.locals import *

def clip(surf,x,y,x_size,y_size):
    clipR = pygame.Rect(x,y,x_size,y_size)
    surf.set_clip(clipR)
    image = surf.subsurface(surf.get_clip())
    return image.copy()

def blur(surf,filter_img,x,y,movement,scale):
    main = surf.copy()
    img = clip(surf,x,y,filter_img.get_width(),filter_img.get_height())
    filter_img.set_colorkey((255,0,255))
    img.blit(filter_img,(0,0))
    img.set_colorkey((0,255,255))
    img_size = [img.get_width(),img.get_height()]
    main.blit(pygame.transform.scale(img,(img_size[0]+scale[0],img_size[1]+scale[1])),(x+movement[0]-int(scale[0]/2),y+movement[1]-int(scale[1]/2)))
    return main
