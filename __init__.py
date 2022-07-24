import display
import random
import machine

from .assets import player, wall, floor
from .dungeonGenerator import Generator

max_level_size = 64
map = []
running = True
camera = (0,0)

class Tile:
  def __init__(self, tile_type):
    self.tile_type = tile_type

def init_map(map,camera):
  gen = Generator()
  gen.gen_level()
  level = gen.level
  first_room = gen.room_list[0]
  camera = (first_room[0],first_room[1])
  for y in range(len(level)-1):
    row = []
    for x in range(len(level[y])-1):
      row.append(Tile(level[x][y]))
    map.append(row)

def render():
  display.drawFill(0x000000)
  for x in range(22):
    for y in range(13):
      position = (camera[0] + x, camera[1] + y)
      if position[0] >= 0 and position[0] < max_level_size \
        and position[1] >= 0 and position[1] < max_level_size:
        if map[position[0]][position[1]].tile_type == 'wall':
          display.drawPng(x * 16, y * 16, wall)
        if map[position[0]][position[1]].tile_type == 'floor':
          display.drawPng(x * 16, y * 16, floor)
  display.drawPng(32, 32, player)
  display.flush()

init_map(map,camera)

while running:
  render()
  machine.lightsleep(50)
