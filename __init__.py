import display
import random
import machine

from .assets import player, wall
from .dungeonGenerator import Generator

def render(level):
  display.drawFill(0x000000)
  for x in range(22):
    for y in range(13):
      if level[x][y] == 'wall':
        display.drawPng(x * 16, y * 16, wall)
  display.drawPng(32, 32, player)
  display.flush()

gen = Generator()
gen.gen_level()
level = gen.level

while True:
  render(level)
  machine.lightsleep(50)
