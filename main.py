from types import SimpleNamespace

from utils import *
from data import *
from pyautogui import *
import json
click_delay = 0.1


def hero_place(name):
    click_unit(name)
    sleep(click_delay)
    click_unit_placements(name)
    sleep(click_delay)
    click_unit(name)
    sleep(click_delay)
def siege_place():
    click_unit('siege')
    sleep(click_delay)
    click_unit_placements('siege')
    sleep(click_delay)
def valks():
    click_unit('valk')
    sleep(click_delay)
    click_all(config['unit_placements']['valk'])
    sleep(click_delay)
def earthquakes():
    click_unit('earthquake')
    sleep(click_delay)
    click_all(config['unit_placements']['earthquake'])
    sleep(click_delay)
def run_attack():
    valks()
    siege_place()
    hero_place('king')
    hero_place('queen')
    hero_place('champion')
    hero_place('warden')
    earthquakes()
    wait_for_any_image(['star', 'return_home'])

def loop():
    start('s')
    print('running')
    while not key_down('q'):
        wait_for_image_and_click('attack')
        wait_for_image_and_click('find_match')
        wait_for_image_and_click('confirm_attack')
        wait_for_image('end_battle')
        calibrate()
        run_attack()
        if not check_for_image('return_home'):
            wait_for_any_image(['end_battle', 'surrender'])
            click_image('surrender')
            wait_for_image_and_click('confirm_surrender')
        wait_for_image_and_click('return_home')


loop()
