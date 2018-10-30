import pygame
from maze import Maze
from scoreboard import Scorebord
import functions as func
from pacman import Pacman
from pygame.sprite import Group
from menu import Menu
from button import Button
from portal import Portal
from blinky import Blinky
from inky import Inky
from pinky import Pinky
from clyde import Clyde
from fruit import Fruit
from audio import Audio

class Game:
    BLACK = (0, 0, 0)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((716, 793 + 60))
        pygame.display.set_caption("Pacman Portal")

        self.bricks = Group()
        self.shields = Group()
        self.powerpills = Group()
        self.qpills = Group()
        self.maze = Maze(self.screen, self.bricks, self.shields, self.powerpills, self.qpills, brickfile='square',
                         mazefile='images/pacmanportalmaze.txt', shieldfile='shield', powerpill='powerpill')

        self.increase = False
        self.scoreboard = Scorebord(self.screen, self)
        self.pacman = Pacman(self.screen, self.scoreboard, self)
        self.play_button = Button(self.screen, "PLAY GAME", 80 / 100)
        self.score_button = Button(self.screen, "HIGH SCORES", 90 / 100)
        self.menu = Menu()
        self.audio = Audio()
        self.fruit = Fruit(self.screen)
        self.blinky = Blinky(self.screen, self.pacman, self.scoreboard)
        self.inky = Inky(self.screen, self.pacman, self.scoreboard)
        self.pinky = Pinky(self.screen, self.pacman, self.scoreboard)
        self.clyde = Clyde(self.screen, self.pacman, self.scoreboard)
        self.oportal = Portal('o', self.pacman)
        self.bportal = Portal('b', self.pacman)
        self.active = False
        self.pause = False

    def __str__(self): return 'Game(Pacman Portal), maze=' + str(self.maze) + ')'

    def play(self):
        while True:
            pygame.time.Clock().tick(1800)
            func.check_events(self.pacman, self.score_button, self.menu, self.play_button, self, self.bportal, self.oportal, self.screen, self.maze, self.audio)
            self.update_screen()
            if self.active:
                func.check_collisions(self.pacman, self.bricks, self.shields, self.powerpills, self.scoreboard, self.blinky, self.pinky, self.inky, self.clyde, self.qpills, self.fruit, self.audio)
                self.pacman.update(self.oportal, self.bportal, self.audio)
                if not self.pause:
                    self.fruit.update()
                    self.blinky.update(self.oportal, self.bportal)
                    self.inky.update(self.oportal, self.bportal)
                    self.pinky.update(self.oportal, self.bportal)
                    self.clyde.update(self.oportal, self.bportal)
                    self.scoreboard.update_score(self)
                if self.increase:
                    self.pacman.reset()
                    self.inky.reset()
                    self.clyde.reset()
                    self.pinky.reset()
                    self.fruit.reset()
                    self.blinky.reset()
                    self.maze.build()
                    self.increase = False
                    if self.scoreboard.lives == 0:
                        self.active = False

    def update_screen(self):
        self.screen.fill(Game.BLACK)
        if self.active:
            self.maze.blitme(self.screen)
            self.scoreboard.show_score()
            self.pacman.blitme()
            self.blinky.blitme()
            self.inky.blitme()
            self.pinky.blitme()
            self.clyde.blitme()
            self.oportal.blitme(self.screen)
            self.bportal.blitme(self.screen)
            self.fruit.blitme()
        elif not self.menu.show_scores:
            self.menu.main(self.play_button, self.score_button, self.screen)
        else:
            self.menu.scores(self.score_button, self.screen)
        pygame.display.flip()


game = Game()
game.play()
