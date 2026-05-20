import os
import cv2
import numpy as np
import pyautogui
import random
import time
from pynput import keyboard

pressed_keys = set()

def on_press(key):
    pressed_keys.add(key)

def on_release(key):
    pressed_keys.discard(key)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)

listener.start()

images = {}
for filename in os.listdir('config/images'):
    if filename.lower().endswith(".png"):
        name = os.path.splitext(filename)[0]  # remove ".png"
        images[name] = cv2.imread(f'config/images/{name}.png', cv2.IMREAD_UNCHANGED)

threshold = .75
def find_image(base_image, search_image):
    result = cv2.matchTemplate(base_image, search_image, cv2.TM_CCOEFF_NORMED)
    yloc, xloc = np.where(result >= threshold)
    w = search_image.shape[1]
    h = search_image.shape[0]
    more_rectangles = []
    for (x, y) in zip(xloc, yloc):
        more_rectangles.append([int(x), int(y), int(w), int(h)])
        more_rectangles.append([int(x), int(y), int(w), int(h)])
    less_rectangles, weights = cv2.groupRectangles(more_rectangles, 1, 0.2)
    centers = get_rect_centers(less_rectangles)
    return centers

def get_rect_centers(rects):
    centers = []
    for rect in rects:
        x = round(rect[0] + rect[2] / 2)
        y = round(rect[1] + rect[3] / 2)
        centers.append((x, y))
    return centers

def custom_click(x, y, uncert):
    x_pos = x if uncert == 0 else (random.randrange(x - uncert, x + uncert))
    y_pos = y if uncert == 0 else (random.randrange(y - uncert, y + uncert))
    pyautogui.moveTo(x_pos, y_pos, duration=random.randrange(50, 100) / 1000)
    pyautogui.mouseDown()
    time.sleep(random.randrange(25, 50) / 1000)
    pyautogui.mouseUp()

def key_down(key):
    return keyboard.KeyCode.from_char(key) in pressed_keys

def start(start_key):
    print('press ' + start_key + ' to start')
    while not key_down(start_key):
        time.sleep(0.1)

def wait_until(condition):
    while not condition():
        if key_down('q'):
            raise TimeoutError()
        time.sleep(0.05)

def take_screenshot_with_region(region):
    img = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def check_for_image(image_name, region):
    return len(find_image(take_screenshot_with_region(region), images[image_name])) > 0


def check_for_any_image(image_1_name, image_1_region, image_2_name, image_2_region):
    return check_for_image(image_1_name, image_1_region) or check_for_image(image_2_name, image_2_region)
    
def check_for_inf_image(image_names, image_region):
    return any(check_for_image(name, image_region) for name in image_names)


def wait_for_image(image_name, region):
    wait_until(lambda: check_for_image(image_name, region))


def wait_for_any_image(image_1_name, image_1_region, image_2_name, image_2_region):
    wait_until(lambda: check_for_any_image(image_1_name, image_1_region, image_2_name, image_2_region))

    
def wait_for_inf_image(image_names, image_region):
    wait_until(lambda: check_for_inf_image(image_names, image_region))


def custom_scroll(val):
    pyautogui.scroll(val)


def custom_drag(x, y, x_diff, y_diff, duration):
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(x + x_diff, y + y_diff, duration=(duration / 1000))

def execute(line, command, parameters):
    print(command, parameters)
    if command == '#':
        return line + 1
    if command == 'WAIT_KEY':
        start(parameters[0])
    if command == 'GOTO':
        return int(parameters[0])-1
    if command == 'END':
        return -1
    if command == 'PRINT':
        print(parameters[0])
    if command == 'WAIT_IMAGE':
        wait_for_image(parameters[0], (int(parameters[1]), int(parameters[2]), int(parameters[3]), int(parameters[4])))
    if command == 'WAIT_ANY_IMAGE':
        wait_for_any_image(parameters[0], (int(parameters[1]), int(parameters[2]), int(parameters[3]), int(parameters[4])), parameters[5], (int(parameters[6]), int(parameters[7]), int(parameters[8]), int(parameters[9])))
    if command == 'WAIT_INF_IMAGE':
        wait_for_inf_image(parameters[4:], (int(parameters[0]), int(parameters[1]), int(parameters[2]), int(parameters[3])))
    if command == 'CLICK':
        custom_click(int(parameters[0]), int(parameters[1]), 5)
        time.sleep(0.05)
    if command == 'SLEEP':
        time.sleep(int(parameters[0]) / 1000)
    if command == 'SCROLL':
        custom_scroll(int(parameters[0]))
    if command == 'DRAG':
        custom_drag(int(parameters[0]), int(parameters[1]), int(parameters[2]), int(parameters[3]), int(parameters[4]))
    if command == 'CHECK_NOT_IMAGE':
        if not check_for_image(parameters[0], (int(parameters[1]), int(parameters[2]), int(parameters[3]), int(parameters[4]))):
            return line + 1
        else:
            return line + int(parameters[5])
    return line + 1


def execute_script(path):
    with open(path, "r") as f:
        script = [line.strip().split(' ') for line in f]
    line = 0
    while line >= 0:
        line = execute(line, script[line][0], script[line][1:])