import pygame
from pygame.sprite import Sprite


class Portal(Sprite):

    def __init__(self, color, pacman):
        super().__init__()
        self.pacman = pacman
        self.active = False
        self.recent = False
        self.usable = False
        if color == "b":
            self.image = pygame.transform.scale(pygame.image.load('images/bportal.png'), (13 * 3, 13 * 3))
            self.rect = self.image.get_rect()
        elif color == "o":
            self.image = pygame.transform.scale(pygame.image.load('images/oportal.png'), (13 * 3, 13 * 3))
            self.rect = self.image.get_rect()
            
    def location(self):
        if self.pacman.direction == 'right':
            self.rect.center = (self.pacman.centerx + 13 * 3, self.pacman.centery)
        if self.pacman.direction == 'left':
            self.rect.center = (self.pacman.centerx - 13 * 3, self.pacman.centery)
        if self.pacman.direction == 'up':
            self.rect.center = (self.pacman.centerx, self.pacman.centery - 13 * 3)
        if self.pacman.direction == 'down':
            self.rect.center = (self.pacman.centerx, self.pacman.centery + 13 * 3)
            
    def blitme(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)
