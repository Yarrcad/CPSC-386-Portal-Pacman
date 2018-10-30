import pygame.font


class Scorebord:

    def __init__(self, screen, game):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game = game

        self.score = 0
        self.lives = 3
        self.level = 1
        self.eaten = 0

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.clives = pygame.transform.scale(pygame.image.load('images/pacman1.png'), (13 * 3, 13 * 3))
        self.update_score(game)

        self.tscore_rect = (self.screen_rect.right * 1 / 20, self.screen_rect.bottom - 50)
        self.cscore_rect = (self.screen_rect.right * 4 / 20, self.screen_rect.bottom - 50)
        self.tlives_rect = (self.screen_rect.right * 8 / 20, self.screen_rect.bottom - 50)
        self.c2lives_rect = (self.screen_rect.right * 11 / 20, self.screen_rect.bottom - 50)
        self.c3lives_rect = (self.screen_rect.right * 12.5 / 20, self.screen_rect.bottom - 50)
        self.tlevel_rect = (self.screen_rect.right * 15 / 20, self.screen_rect.bottom - 50)
        self.clevel_rect = (self.screen_rect.right * 18 / 20, self.screen_rect.bottom - 50)
        self.tscore = self.font.render("Score: ", True, self.WHITE, self.BLACK)
        self.cscore = self.font.render(str(self.score), True, self.YELLOW, self.BLACK)
        self.tlives = self.font.render("Lives: ", True, self.WHITE, self.BLACK)
        self.tlevel = self.font.render("Level: ", True, self.WHITE, self.BLACK)
        self.clevel = self.font.render(str(self.level), True, self.YELLOW, self.BLACK)

    def update_score(self, game):
        if self.eaten == 240:
            self.level += 1
            self.game.increase = True
            self.eaten = 0
        self.tscore = self.font.render("Score: ", True, self.WHITE, self.BLACK)
        self.cscore = self.font.render(str(self.score), True, self.YELLOW, self.BLACK)
        self.tlives = self.font.render("Lives: ", True, self.WHITE, self.BLACK)
        self.tlevel = self.font.render("Level: ", True, self.WHITE, self.BLACK)
        self.clevel = self.font.render(str(self.level), True, self.YELLOW, self.BLACK)
        if self.lives == 0:
            game.increase = True
            self.lives = 3
            with open('hs.txt', 'a') as f:
                f.write('\n' + str(self.score))
            game.active = False

    def show_score(self):
        """Draw scores and ships to the screen"""
        self.screen.blit(self.tscore, self.tscore_rect)
        self.screen.blit(self.cscore, self.cscore_rect)
        self.screen.blit(self.tlives, self.tlives_rect)
        self.screen.blit(self.tlevel, self.tlevel_rect)
        self.screen.blit(self.clevel, self.clevel_rect)
        if self.lives > 2:
            self.screen.blit(self.clives, self.c3lives_rect)
        if self.lives > 1:
            self.screen.blit(self.clives, self.c2lives_rect)
