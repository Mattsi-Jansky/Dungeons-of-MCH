import display
import random
import machine

from .assets import player
from .assets import wall

def drawRandomLine():
  x1 = random.randint(0,320)
  x2 = random.randint(0,320)
  y1 = random.randint(0,240)
  y2 = random.randint(0,240)
  color = random.randint(0,0xFFFFFF)
  # display.drawLine(x1,y1,x2,y2,color)
  display.drawFill(0xFFFFFF)
  display.drawPng(32, 32, player)
  display.drawPng(0, 0, wall)
  display.drawPng(0, 16, wall)
  display.flush()
  machine.lightsleep(50)

display.drawFill(0xFFFFFF)
while True:
  drawRandomLine()
