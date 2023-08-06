import time
import sys
import pygame



class Button:
    def __init__(self,window,pos,size,colour,txt = None, listeners = None, listener_atributes = ()):
        self.window = window
        self.pos = pos
        self.size = size
        self.listeners = listeners
        self.colour = colour
        self.txt = txt
        self.listener_atributes = listener_atributes
        ###
        self.surface = pygame.Surface([self.size[0],size[1]])
        self.surface.fill(colour)
        self.rect = pygame.Rect(size,pos)
        print(self.rect)

    def draw(self):
        self.window.blit(self.surface,self.pos)

    def check_press(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                for i_funcs,funcs in enumerate(self.listeners):
                    funcs(self.listener_atributes[i_funcs])


    def update(self):
        self.surface = pygame.Surface([self.size[0], self.size[1]])
        self.rect = pygame.Rect(self.pos,self.size)
        self.surface.fill(self.colour)
        self.draw()
        self.check_press()






