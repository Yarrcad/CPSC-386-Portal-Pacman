import pygame


class Audio:
    def __init__(self):
        # Create mixer for audio.
        pygame.mixer.init()
        pygame.mixer.set_num_channels(2)
        self.a = pygame.mixer.Channel(0)
        self.b = pygame.mixer.Channel(1)
        self.fruit = pygame.mixer.Sound("audio/pacman_eatfruit.wav")
        self.ghost = pygame.mixer.Sound("audio/pacman_eatghost.wav")
        self.death = pygame.mixer.Sound("audio/pacman_death.wav")
        self.wew = pygame.mixer.Sound("audio/pacman_wew.wav")
        self.begin = pygame.mixer.Sound("audio/pacman_beginning.wav")

    @staticmethod
    def play():
        # Play background music.
        pygame.mixer_music.set_volume(.5)
        pygame.mixer.music.play()
