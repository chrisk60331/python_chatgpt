import pygame


class AudioPlayer:
    def __init__(self, file_name):
        self.file_name = file_name
        pygame.init()
        pygame.mixer.init()

    def play(self):
        pygame.mixer.music.load(self.file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.quit()
