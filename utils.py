import cv2
import numpy as np
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api
import win32con
from pynput import mouse
from data import *

threshold = .75

images = {}
def load_images(folder_path="images"):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            name = os.path.splitext(filename)[0]  # remove ".png"
            images[name] = cv2.imread(f'images/{name}.png', cv2.IMREAD_UNCHANGED)
    return images
load_images()


def display_image(image):
    cv2.imshow('NeedNoTitle', image)
    cv2.waitKey()
    cv2.destroyAllWindows()


img_cache = {}


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


def take_screenshot():
    img = pyautogui.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def take_screenshot_with_region(region):
    img = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def custom_click(x, y, uncert):
    x_pos = x if uncert == 0 else (random.randrange(x - uncert, x + uncert))
    y_pos = y if uncert == 0 else (random.randrange(y - uncert, y + uncert))
    win32api.SetCursorPos((x_pos, y_pos))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(random.randrange(25, 50) / 1000)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def key_down(key):
    return keyboard.is_pressed(key)


def start(start_key):
    print('press ' + start_key + ' to start')
    while not key_down(start_key):
        sleep(0.1)

def wait_until(condition):
    while not condition():
        if key_down('q'):
            raise TimeoutError()
        time.sleep(0.05)


mouse_pressed = False
def on_click(x, y, button, pressed):
    global mouse_pressed
    mouse_pressed = pressed
listener = mouse.Listener(on_click=on_click)
listener.start()


def click_mode():
    start('s')
    print('click mode started. Press "q" to exit.')
    while not key_down('q'):
        if mouse_pressed:
            x, y = pyautogui.position()
            pixel = pyautogui.pixel(x, y)
            print(f"({x}, {y}, {pixel})")
        sleep(0.1)


def write_line(line: int, text: str):
    sys.stdout.write(f"\033[{line};0H\033[K{text}\n")
    sys.stdout.flush()


def print_if_present(shot, img_name, line):
    search_img = images[img_name]
    cent = find_image(shot, search_img)
    image_found = len(cent) > 0
    write_line(line, f'{img_name}: {image_found}')


def check_for_image(img_name):
    return len(find_image(take_screenshot_with_region(regions[img_name]), images[img_name])) > 0


def check_for_any_image(img_names):
    return any(
        len(find_image(take_screenshot_with_region(regions[name]), images[name])) > 0
        for name in img_names
    )


def wait_for_image(image_name):
    write_line(1, f'waiting for {image_name}')
    wait_until(lambda: check_for_image(image_name))


def wait_for_any_image(imgs):
    write_line(1, f'waiting for either of {imgs}')
    wait_until(lambda: check_for_any_image(imgs))


def click_image(image_name):
    x, y = get_rect_centers([regions[image_name]])[0]
    custom_click(x, y, 5)


def wait_for_image_and_click(image_name):
    wait_for_image(image_name)
    click_image(image_name)


def sleep_random(min, max):
    time.sleep(random.randrange(min, max) / 1000)


def click_succession(positions):
    for pos in positions:
        x, y = pos
        custom_click(x, y, 5)
        sleep_random(20, 50)


def zoom_out():
    for i in range(1, 10):
        pyautogui.scroll(-500)


def click_troop(troop_name):
    x, y = troop_buttons[troop_name]
    custom_click(x, y, 5)


def click_troop_placements(troop_name):
    x, y = troop_placements[troop_name]
    custom_click(x, y, 5)

def click_all(points):
    for p in points:
        x, y = p
        custom_click(x, y, 5)

def drag(x, y):
    x_base = 970
    y_base = 520
    pyautogui.moveTo(x_base, y_base)
    pyautogui.dragTo(x_base + x, y_base + y, duration=0.3)

def calibrate():
    zoom_out()
    drag(200, 200)
    drag(-20, -90)