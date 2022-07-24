import display
import random
import machine

from .assets import player, wall, floor
from .dungeonGenerator import Generator

gen = Generator()
gen.gen_level()
level = gen.level
first_room = gen.room_list[0]
camera = (first_room[0],first_room[1])
max_level_size = 64

def render():
  display.drawFill(0x000000)
  for x in range(22):
    for y in range(13):
      position = (camera[0] + x, camera[1] + y)
      if position[0] >= 0 and position[0] < max_level_size \
        and position[1] >= 0 and position[1] < max_level_size:
        if level[position[0]][position[1]] == 'wall':
          display.drawPng(x * 16, y * 16, wall)
        if level[position[0]][position[1]] == 'floor':
          display.drawPng(x * 16, y * 16, floor)
  display.drawPng(32, 32, player)
  display.flush()

while True:
  render()
  machine.lightsleep(50)
