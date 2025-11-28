import pygame
import pygame.midi
import random

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = list(range(2, 7))
WHITE_KEY_INDICES = [0, 2, 4, 5, 7, 9, 11]
FRENCH_NOTE_NAMES = {
    'C': 'Do', 'D': 'Ré', 'E': 'Mi', 'F': 'Fa',
    'G': 'Sol', 'A': 'La', 'B': 'Si'
}