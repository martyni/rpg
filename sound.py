""" Sound Module"""
import math
from controls import pygame

def distance(point1, point2):
    """Figure out distance between 2 points"""
    x_1, y_1 = point1
    x_2, y_2 = point2
    x_abs = abs(x_1 - x_2)
    y_abs = abs(y_1 - y_2)
    return math.hypot(x_abs, y_abs)

def same_random_number(string):
    """Turn a name into a number 1-10"""
    return hash(string) % 10 + 1

class SoundBus(object):
    """ Class to handle sound effects"""
    screen_center = (228, 224)
    def __init__(self):
        self.sounds = {}
        pygame.mixer.init()
        pygame.mixer.set_num_channels(10)
        self.channels = [pygame.mixer.Channel(_) for _ in range(0, 10)]
        self.cache = {}

    def play_sound(self, x_pos, y_pos, filename):
        """Play sound"""
        sft = self.cache.get(filename) if self.cache.get(filename) else pygame.mixer.Sound(filename) 
        how_loud = 1 - (distance((x_pos, y_pos), self.screen_center) / float(200))
        if how_loud < 0:
            return None
        sft.set_volume(how_loud)
        sound_channel = same_random_number(filename)
        if not self.channels[sound_channel].get_busy():
            self.channels[sound_channel].play(sft)
            print "playing", filename, sound_channel, how_loud
        else:
            pass
        return None

    def play_song(self, filename):
        """Plays song continuously"""
        sft = pygame.mixer.Sound(filename)
        self.sounds["main"] = sft
        self.sounds["main"].play(-1)


    def stop_song(self):
        """Plays song continuously"""
        try:
            self.sounds["main"].stop()
        except KeyError:
            print self.sounds

SOUND = SoundBus()
