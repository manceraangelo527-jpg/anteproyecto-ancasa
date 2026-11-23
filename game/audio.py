import os
import pygame
from config import SND_DIR


class GestorAudio:
    def __init__(self):
        self.activo = False
        self.musica_actual = None
        try:
            pygame.mixer.init()
            self.activo = True
        except pygame.error:
            # Si no hay tarjeta de audio, el juego sigue funcionando sin sonido
            self.activo = False

    def reproducir_musica(self, archivo, volumen=0.45):
        if not self.activo or not archivo or archivo == self.musica_actual:
            return
        ruta = os.path.join(SND_DIR, archivo)
        if os.path.exists(ruta):
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(-1)
            self.musica_actual = archivo

    def reproducir_efecto(self, archivo, volumen=0.75):
        if not self.activo or not archivo:
            return
        ruta = os.path.join(SND_DIR, archivo)
        if os.path.exists(ruta):
            sonido = pygame.mixer.Sound(ruta)
            sonido.set_volume(volumen)
            sonido.play()