import pygame
import sys
import random
import time
import Controller
import Model
import View
from View import game_event
import Card
from Card import Color

def main():
    """Calls the game loop"""
    controller = Controller.Controller()
    controller.run()

main()