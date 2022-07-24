import display
import random
import machine

from .assets import player, wall
from .dungeonGenerator import Generator

def render():
  display.drawFill(0x000000)
  display.drawPng(32, 32, player)
  display.drawPng(0, 0, wall)
  display.drawPng(0, 16, wall)
  display.flush()

gen = Generator()
gen.gen_level()

while True:
  render()
  machine.lightsleep(50)
