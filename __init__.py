import display
import random
import machine
import buttons

from .assets import player, wall, floor
from .dungeonGenerator import Generator

max_level_size = 64
screen_size_x = 22
screen_size_y = 13
debounce = False

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
player_pos = [0,0]
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

def init(map,camera):
  global player_pos
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
  player_pos = [spawn[0],spawn[1]]

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

def move_left(pressed):
  global debounce
  if pressed and not debounce:
    entity = map[player_pos[0]][player_pos[1]].entity
    map[player_pos[0]-1][player_pos[1]].entity = entity
    map[player_pos[0]][player_pos[1]].entity = None
    player_pos[0] = player_pos[0] - 1
    camera.update(player_pos[0],player_pos[1])
    debounce = True
  elif not pressed:
    debounce = False

init(map,camera)
buttons.attach(buttons.BTN_LEFT,move_left)

while running:
  render()
  machine.lightsleep(50)
