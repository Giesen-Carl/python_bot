import cv2
import numpy as np
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api
import win32con

threshold = .6


def display_image(image):
    cv2.imshow('NeedNoTitle', image)
    cv2.waitKey()
    cv2.destroyAllWindows()


def load_image(image_location):
    return cv2.imread(image_location, cv2.IMREAD_UNCHANGED)


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


def draw_rectangles(img, rects):
    for (tx, ty, tw, th) in rects:
        cv2.rectangle(img, (tx, ty), (tx + tw, ty + th), (0, 255, 255), 2)


def draw_dots(img, dots):
    for (x, y) in dots:
        cv2.circle(img, (x, y), 1, (255, 0, 0), 2)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(random.randrange(100, 300) / 1000)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def key_down(key):
    return keyboard.is_pressed(key)


def start(start_key):
    print('press ' + start_key + ' to start')
    while not key_down(start_key):
        sleep(0.1)
