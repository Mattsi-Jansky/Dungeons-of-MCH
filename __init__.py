import display
import random
import machine

from .assets import player, wall, floor
from .dungeonGenerator import Generator

class Camera:
  def __init__(self, x, y):
    self.x = x
    self.y = y

max_level_size = 64
map = []
running = True
camera = Camera(0,0)
entities = []

class Entity:
  def __init__(self):
    entities.append(self)

  def get_graphic(self):
    return floor

class Player(Entity):
  def __init__(self):
    super(Entity, self).__init__()

  def get_graphic(self):
    return player

class Tile:
  def __init__(self, tile_type):
    self.tile_type = tile_type
    self.entity = None

def init_map(map,camera):
  gen = Generator()
  gen.gen_level()
  level = gen.level
  first_room = gen.room_list[0]
  camera.x = first_room[0]
  camera.y = first_room[1]
  for y in range(len(level)-1):
    row = []
    for x in range(len(level[y])-1):
      row.append(Tile(level[x][y]))
    map.append(row)
  map[camera.x][camera.y].entity = Player()

def render():
  display.drawFill(0x000000)
  for x in range(22):
    for y in range(13):
      position = (camera.x + x, camera.y + y)
      if position[0] >= 0 and position[0] < max_level_size \
        and position[1] >= 0 and position[1] < max_level_size:
        if map[position[0]][position[1]].tile_type == 'wall':
          display.drawPng(x * 16, y * 16, wall)
        if map[position[0]][position[1]].tile_type == 'floor':
          display.drawPng(x * 16, y * 16, floor)
        if map[position[0]][position[1]].entity is not None:
          display.drawPng(x * 16, y * 16, map[position[0]][position[1]].entity.get_graphic())
  display.flush()

init_map(map,camera)

while running:
  render()
  machine.lightsleep(50)
