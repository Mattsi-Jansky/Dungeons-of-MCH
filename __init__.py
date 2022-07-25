import display
import random
import machine
import buttons

from .assets import player, wall, floor, goblin, troll
from .dungeonGenerator import Generator

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def transform(self, x, y):
    return Point(self.x + x, self.y + y)

max_level_size = 64
screen_size_x = 22
screen_size_y = 13
debounce = False
dirty = True
min_enemies = 8
max_enemies = 15
move_directions = [Point(0,1), Point(0,-1), Point(1,0), Point(-1,0), Point(0,0)]

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
player_pos = Point(0,0)
entities = []

class Entity:
  def __init__(self):
    entities.append(self)
    

  def get_graphic(self):
    return floor
  
  def tick(self):
    pass

class Player(Entity):
  def __init__(self):
    super(Entity, self).__init__()

  def get_graphic(self):
    return player

class Enemy(Entity):
  def __init__(self, graphic):
    super(Entity, self).__init__()
    self.graphic = graphic
  
  def get_graphic(self):
    return self.graphic
  
  def tick(self):
    direction = move_directions[random.randint(0,len(move_directions) - 1)]

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
  player_pos = Point(spawn[0],spawn[1])
  
  for i in range(random.randint(min_enemies, max_enemies)):
    room = gen.random_room()
    xSpacing = random.randint(0,room[2] - 1)
    ySpacing = random.randint(0,room[3] - 1)
    tile = map[room[0] + xSpacing][room[1] + ySpacing]
    if not tile.entity:
      graphic = goblin
      if bool(random.getrandbits(1)):
        graphic = troll
      tile.entity = Enemy(graphic)

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

def move(entity, transform):
  from_tile = map[player_pos.x][player_pos.y]
  to_point = player_pos.transform(transform.x, transform.y)
  to_tile = map[to_point.x][to_point.y]
  if not to_tile.entity and to_tile.tile_type is not 'wall' :
    to_tile.entity = from_tile.entity
    from_tile.entity = None

def move_player(pressed, transform):
  global dirty
  global player_pos
  if pressed:
    move(map[player_pos.x][player_pos.y], transform)
    player_pos = player_pos.transform(transform.x, transform.y)
    camera.update(player_pos.x,player_pos.y)
    dirty = True

def tick():
  for entity in entities:
    entity.tick()

init(map,camera)
buttons.attach(buttons.BTN_LEFT, lambda pressed: move_player(pressed, Point(-1, 0)))
buttons.attach(buttons.BTN_RIGHT, lambda pressed: move_player(pressed, Point(1, 0)))
buttons.attach(buttons.BTN_DOWN, lambda pressed: move_player(pressed, Point(0, 1)))
buttons.attach(buttons.BTN_UP, lambda pressed: move_player(pressed, Point(0, -1)))

while running:
  if dirty:
    render()
    machine.lightsleep(50)
    dirty = False
    tick()
