import pygame

pygame.mixer.init()

def cargar_sonido(ruta):
    return pygame.mixer.Sound(ruta)

def reproducir(sonido):
    if not pygame.mixer.get_busy():
        sonido.play()