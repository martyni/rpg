"""Simple module to handle sprite collision groups"""
from controls import pygame

# pylint: disable=too-few-public-methods
# This is fine
class PhysicalGroup(pygame.sprite.Group):
    """Simple Class to place sprites that need to bump into each other."""
    name = "physical"


MAIN_PHYSICAL_GROUP = PhysicalGroup()
PC_PHYSICAL_GROUP = PhysicalGroup()
