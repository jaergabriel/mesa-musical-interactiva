import pygame

pygame.mixer.init()

def cargar_sonido(ruta):
    return pygame.mixer.Sound(ruta)

def reproducir(sonido):
    canal = pygame.mixer.find_channel(True)
    if canal:
        canal.play(sonido)