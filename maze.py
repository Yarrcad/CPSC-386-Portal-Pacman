import pygame
from imagerect import ImageRect


class Maze:
    RED = (255, 0, 0)
    PIX_SIZE = 13

    def __init__(self, screen, bricks, shields, powerpills, qpills, brickfile, mazefile, shieldfile, powerpill):
        self.screen = screen

        self.filename = mazefile
        self.brickfile = brickfile
        self.shieldfile = shieldfile
        self.powerpill = powerpill

        self.bricks = bricks
        self.shields = shields
        self.powerpills = powerpills
        self.qpills = qpills
        self.count = 60

        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

    def __str__(self): return 'maze(' + self.filename + ')'

    def build(self):
        self.count = 30
        self.bricks.empty()
        self.powerpills.empty()
        self.qpills.empty()
        self.shields.empty()
        sz = Maze.PIX_SIZE
        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'X':
                    brick = ImageRect(self.screen, self.brickfile, sz, sz)
                    brick.rect = pygame.Rect(ncol * sz, nrow * sz, brick.rect.width, brick.rect.height)
                    self.bricks.add(brick)
                elif col == 'o':
                    shield = ImageRect(self.screen, self.shieldfile, sz, sz)
                    shield.rect = pygame.Rect(ncol * sz, nrow * sz, shield.rect.width, shield.rect.height)
                    self.shields.add(shield)
                elif col == 'P':
                    powerpill = ImageRect(self.screen, self.powerpill, int(0.5 * sz), int(0.5 * sz))
                    powerpill.rect = pygame.Rect(ncol * sz + powerpill.rect.width/2, nrow * sz +
                                                 powerpill.rect.height/2, powerpill.rect.width, powerpill.rect.height)
                    self.powerpills.add(powerpill)
                elif col == 'Q':
                    qpill = ImageRect(self.screen, self.powerpill, int(2 * sz), int(2 * sz))
                    qpill.rect = pygame.Rect(ncol * sz - qpill.rect.width/4, nrow * sz - qpill.rect.height/4, qpill.rect.width, qpill.rect.height)
                    self.qpills.add(qpill)

    def blitme(self, screen):
        self.count -= 1
        self.bricks.draw(screen)
        self.shields.draw(screen)
        self.powerpills.draw(screen)
        if self.count < 0:
            self.count = 60
        elif self.count < 30:
            self.qpills.draw(screen)
