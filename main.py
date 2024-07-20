from utils import *
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api
import win32con

# farm_img = load_image('images/farm.png')
# wheat_img = load_image('images/needle.png')
# matches = find_image(farm_img, wheat_img)
# # draw_dots(farm_img, matches)
# # display_image(farm_img)
# print(matches)
start('s')
while not key_down('q'):
    print('running')
    sleep(0.2)

