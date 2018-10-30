import pygame
from pygame.sprite import Sprite
import random


class Fruit(Sprite):

    def __init__(self, screen):
        super().__init__()
        self.active = False
        self.count = 0
        self.screen = screen
        self.duration = 1440

        self.image = pygame.transform.scale(pygame.image.load('images/fruit.png').convert_alpha(), (13 * 3, 13 * 3))
        self.rect = self.image.get_rect()

        self.rect.centery = 34.5 * 13
        self.rect.centerx = 27.5 * 13
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    def update(self):
        if not self.active:
            if 0 == random.randint(0, 10000):
                self.active = True
                self.duration = 1440
                self.count += 1
        else:
            self.duration -= 1
            if self.duration < 0:
                self.active = False

    def blitme(self):
        if self.active:
            self.screen.blit(self.image, self.rect)

    def reset(self):
        self.count = 0
        self.duration = 1440
