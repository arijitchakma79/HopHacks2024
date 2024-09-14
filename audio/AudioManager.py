import pygame

class AudioManager:
    def __init__(self) -> None:
        pygame.mixer.init()

    def play(self, filePath, volume = 1.0):
        pygame.mixer.music.load("res/" + filePath)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)