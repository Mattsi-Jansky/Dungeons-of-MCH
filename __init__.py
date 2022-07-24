import display
import random
import machine

from .assets import player, wall, floor
from .dungeonGenerator import Generator

max_level_size = 64
screen_size_x = 22
screen_size_y = 13

class Camera:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def update(self, player_x, player_y):
    self.x = player_x - int(screen_size_x / 2)
    self.y = player_y - int(screen_size_y / 2)

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
  spawn = (first_room[0] + int(first_room[2] / 2), first_room[1] + int(first_room[3] / 2))
  for y in range(len(level)):
    row = []
    for x in range(len(level[y])):
      row.append(Tile(level[x][y]))
    map.append(row)
  map[spawn[0]][spawn[1]].entity = Player()
  camera.update(spawn[0],spawn[1])
  print(f"Spawn player at {spawn[0]},{spawn[1]}")
  print(f"Size of map: {len(map)}")
  print(f"Size of level: {len(level)}")

def render():
  display.drawFill(0x000000)
  for x in range(screen_size_x):
    for y in range(screen_size_y):
      position = (camera.x + x, camera.y + y)
      if position[0] >= 0 and position[0] < max_level_size \
        and position[1] >= 0 and position[1] < max_level_size:
        if map[position[0]][position[1]].tile_type == 'wall':
          display.drawPng(x * 16, y * 16, wall)
        elif map[position[0]][position[1]].tile_type == 'floor':
          display.drawPng(x * 16, y * 16, floor)
        if map[position[0]][position[1]].entity is not None:
          display.drawPng(x * 16, y * 16, map[position[0]][position[1]].entity.get_graphic())
  display.flush()

init_map(map,camera)

while running:
  render()
  machine.lightsleep(50)
