import pygame
from pygame.sprite import Sprite
import spritesheet

class Pacman(Sprite):

    def __init__(self, screen, scoreboard, game):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.scoreboard = scoreboard
        self.game = game

        ss = spritesheet.spritesheet('images/sheet.png')
        self.rimages = []
        self.rimages = ss.images_at(((457, 1, 13, 13), (473, 1, 13, 13), (489, 1, 14, 14), (473, 1, 13, 13)), colorkey=(0, 0, 0))
        self.limages = []
        self.limages = ss.images_at(((461, 17, 13, 13), (474, 17, 13, 13), (489, 1, 14, 14), (474, 17, 13, 13)),
                                    colorkey=(0, 0, 0))
        self.uimages = []
        self.uimages = ss.images_at(((457, 36, 13, 13), (473, 34, 13, 13), (489, 1, 14, 14), (473, 34, 13, 13)),
                                    colorkey=(0, 0, 0))
        self.dimages = []
        self.dimages = ss.images_at(((457, 49, 13, 13), (473, 49, 13, 13), (489, 1, 14, 14), (473, 49, 13, 13)),
                                    colorkey=(0, 0, 0))
        self.ripimages = []
        self.ripimages = ss.images_at(((505, 1, 13, 13), (520, 1, 13, 13), (536, 1, 13, 13), (552, 1, 13, 13), (568, 2, 13, 13), (584, 3, 13, 13),
                                       (601, 4, 13, 13), (616, 4, 13, 13), (631, 4, 13, 13), (649, 4, 13, 13), (666, 6, 13, 13)), colorkey=(0, 0, 0))

        self.image = pygame.transform.scale(self.limages[0], (13 * 3, 13 * 3))
        self.rect = self.image.get_rect()
        self.index = 0
        self.alive = True
        self.boosted = False
        self.boosted_duration = 1440
        self.ghost_score = 0
        self.image_speed = 30
        self.move = True
        self.wait = 10 * 60

        self.rect.centery = 34.5 * 13
        self.rect.centerx = 27.5 * 13
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

        self.direction = "left"
        self.next_move = "none"

    def update(self, oportal, bportal, audio):
        if self.wait >= 0:
            self.game.pause = True
            self.wait -= 1
            if self.wait < 0:
                self.game.pause = False
        else:
            if not audio.a.get_busy():
                audio.a.play(audio.wew)
            if self.boosted:
                self.boosted_duration -= 1
                if self.boosted_duration < 0:
                    self.boosted = False
                    self.ghost_score = 0
                    self.boosted_duration = 1440
            if self.alive == False:
                self.image_speed -= 1
                if self.image_speed < 0 and self.index < len(self.ripimages):
                    self.image = pygame.transform.scale(self.ripimages[self.index], (13 * 3, 13 * 3))
                    self.index += 1
                    self.image_speed = 30
                elif self.index == len(self.ripimages):
                    self.game.pause = False
                    self.index += 1
                elif self.index > len(self.ripimages) and self.image_speed < 0:
                    self.reset()
                    oportal.active = False
                    bportal.active = False
            else:
                if self.rect.center == oportal.rect.center and bportal.active and oportal.active:
                    self.rect.center = bportal.rect.center
                    self.centerx = self.rect.centerx
                    self.centery = self.rect.centery
                    bportal.active = False
                elif self.rect.center == bportal.rect.center and oportal.active and bportal.active:
                    self.rect.center = oportal.rect.center
                    self.centerx = self.rect.centerx
                    self.centery = self.rect.centery
                    oportal.active = False
                else:
                    self.image_speed -= 1
                    if self.image_speed < 0:
                        if self.index == len(self.limages):
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
                    if self.centerx < 0:
                        self.centerx = self.screen_rect.width
                    if self.centerx > self.screen_rect.width:
                        self.centerx = 0
                    if self.move:
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



    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def death(self):
        self.scoreboard.lives -= 1
        self.scoreboard.eaten = 0
        self.direction = "left"
        self.next_move = "none"
        self.alive = False
        self.game.pause = True
        self.image_speed = 30
        self.index = 0

    def reset(self):
        self.direction = "left"
        self.next_move = "none"
        self.centery = self.rect.centery = 34.5 * 13
        self.centerx = self.rect.centerx = 27.5 * 13
        self.image = pygame.transform.scale(self.limages[0], (13 * 3, 13 * 3))
        self.index = 0
        self.image_speed = 30
        self.alive = True
        self.wait = 10 *60