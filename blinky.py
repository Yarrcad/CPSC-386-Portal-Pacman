import pygame
from pygame.sprite import Sprite
import spritesheet

class Blinky(Sprite):

    def __init__(self, screen, pacman, scoreboard):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.pacman = pacman
        self.chase = True
        self.portal = False
        self.active = True
        self.move_speed = 1
        self.scoreboard = scoreboard

        ss = spritesheet.spritesheet('images/sheet.png')
        self.rimages = []
        self.rimages = ss.images_at(((457, 65, 13, 14), (473, 65, 13, 14)), colorkey=(0, 0, 0))
        self.limages = []
        self.limages = ss.images_at(((489, 65, 13, 14), (505, 65, 13, 14)), colorkey=(0, 0, 0))
        self.uimages = []
        self.uimages = ss.images_at(((521, 65, 13, 14), (521, 65, 13, 14)), colorkey=(0, 0, 0))
        self.dimages = []
        self.dimages = ss.images_at(((553, 65, 13, 14), (569, 65, 13, 14),), colorkey=(0, 0, 0))
        self.bimages = []
        self.bimages = ss.images_at(((585, 65, 13, 14), (601, 65, 13, 14)), colorkey=(0, 0, 0))
        self.bwimages = []
        self.bwimages = ss.images_at(((585, 65, 13, 14), (633, 65, 13, 14), (601, 65, 13, 14), (617, 65, 13, 14)), colorkey=(0, 0, 0))
        self.erimage = ss.image_at((583, 81, 13, 14), colorkey=(0, 0, 0))
        self.elimage = ss.image_at((595, 81, 13, 14), colorkey=(0, 0, 0))
        self.euimage = ss.image_at((608, 81, 13, 14), colorkey=(0, 0, 0))
        self.edimage = ss.image_at((624, 81, 13, 14), colorkey=(0, 0, 0))

        self.image = pygame.transform.scale(self.limages[0], (13 * 3, 13 * 3))
        self.rect = self.image.get_rect()
        self.index = 0
        self.image_speed = 30

        self.rect.centery = 22.5 * 13
        self.rect.centerx = 27.5 * 13
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.pghost = (self.rect.centerx, self.rect.centery)
        self.font = pygame.font.Font(None, 28)
        self.ptext = self.font.render(str(self.pacman.ghost_score * 200), 1, (255, 255, 255))


        self.direction = "right"
        self.next_move = "none"

    def update(self, oportal, bportal):
        if self.active:
            if self.scoreboard.level > 2:
                self.portal = True
            if self.scoreboard.eaten > 180:
                self.move_speed = 2
            if self.pacman.alive:
                if self.rect.center == oportal.rect.center and bportal.active and oportal.active and self.portal:
                    self.rect.center = bportal.rect.center
                    self.centerx = self.rect.centerx
                    self.centery = self.rect.centery
                    bportal.active = False
                elif self.rect.center == bportal.rect.center and oportal.active and bportal.active and self.portal:
                    self.rect.center = oportal.rect.center
                    self.centerx = self.rect.centerx
                    self.centery = self.rect.centery
                    oportal.active = False
                elif self.pacman.boosted:
                    self.image_speed -= 1
                    if self.image_speed < 0:
                        if self.index >= len(self.limages):
                            self.index = 0
                        if self.pacman.boosted_duration > 720:
                            self.image = pygame.transform.scale(self.bimages[self.index], (13 * 3, 13 * 3))
                        else:
                            self.image = pygame.transform.scale(self.bwimages[self.index], (13 * 3, 13 * 3))
                        self.index += 1
                        self.image_speed = 30
                else:
                    self.image_speed -= 1
                    if self.image_speed < 0:
                        if self.index >= len(self.limages):
                            self.index = 0
                        if self.direction == "right":
                            self.image = pygame.transform.scale(self.rimages[self.index], (13 * 3, 13 * 3))
                        elif self.direction == "left":
                            self.image = pygame.transform.scale(self.limages[self.index], (13 * 3, 13 * 3))
                        elif self.direction == "up":
                            self.image = pygame.transform.scale(self.uimages[self.index], (13 * 3, 13 * 3))
                        elif self.direction == "down":
                            self.image = pygame.transform.scale(self.dimages[self.index], (13 * 3, 13 * 3))
                        self.index += 1
                        self.image_speed = 30
                if self.chase:
                    if self.centerx < 0:
                        self.centerx = self.screen_rect.width
                    if self.centerx > self.screen_rect.width:
                        self.centerx = 0
                    if self.direction == "right":
                        self.centerx += self.move_speed
                    elif self.direction == "left":
                        self.centerx -= self.move_speed
                    elif self.direction == "up":
                        self.centery -= self.move_speed
                    elif self.direction == "down":
                        self.centery += self.move_speed
                    self.rect.centerx = self.centerx
                    self.rect.centery = self.centery
            else:
                self.reset()
        elif self.pacman.alive:
            if self.direction == "right":
                self.centerx += 1
            elif self.direction == "left":
                self.centerx -= 1
            elif self.direction == "up":
                self.centery -= 1
            elif self.direction == "down":
                self.centery += 1
            self.rect.centerx = self.centerx
            self.rect.centery = self.centery
            if self.rect.centery < 33 * 13 and self.rect.centery > 25 * 13 and self.rect.centerx > 21 * 13 and self.rect.centerx < 35 * 13:
                self.reset()
        else:
            self.reset()

    def blitme(self):
        if self.active:
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(self.ptext, self.pghost)
            if self.direction == "right":
                self.screen.blit(self.erimage, self.rect)
            elif self.direction == "left":
                self.screen.blit(self.elimage, self.rect)
            elif self.direction == "up":
                self.screen.blit(self.euimage, self.rect)
            elif self.direction == "down":
                self.screen.blit(self.edimage, self.rect)

    def reset(self):
        self.centery = self.rect.centery = 22.5 * 13
        self.centerx = self.rect.centerx = 27.5 * 13
        self.direction = "right"
        self.next_move = "none"
        self.move_speed = 1
        self.active = True

    def death(self):
        self.active = False
        self.ptext = self.font.render(str(self.pacman.ghost_score * 200), 1, (255, 255, 255))
        self.pghost = (self.rect.centerx, self.rect.centery)
