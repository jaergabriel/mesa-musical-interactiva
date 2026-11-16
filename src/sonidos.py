import pygame

pygame.mixer.init()
pygame.mixer.set_num_channels(32) # Subimos a 32 para tener un canal exclusivo por zona

def cargar_sonido(ruta):
    return pygame.mixer.Sound(ruta)

def reproducir(sonido):
    canal = pygame.mixer.find_channel(True)
    if canal:
        canal.play(sonido)
        return canal
    return None