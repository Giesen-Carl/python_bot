from utils import *
from data import *
from pyautogui import *
click_delay = 0.1
def hero_place(name):
    click_troop(name)
    sleep(click_delay)
    click_troop_placements(name)
    sleep(click_delay)
    click_troop(name)
    sleep(click_delay)
def siege_place():
    click_troop('siege')
    sleep(click_delay)
    click_troop_placements('siege')
    sleep(click_delay)
def valks():
    click_troop('valk')
    sleep(click_delay)
    click_all(valk_placements)
    sleep(click_delay)
def earthquakes():
    click_troop('earthquake')
    sleep(click_delay)
    click_all(earthquake_placements)
    sleep(click_delay)
def run_attack():
    valks()
    siege_place()
    hero_place('king')
    hero_place('queen')
    hero_place('champion')
    hero_place('warden')
    earthquakes()
    wait_for_any_image(['star', 'return_home_button'])

def loop():
    start('s')
    print('running')
    while not key_down('q'):
        wait_for_image_and_click('attack_button')
        wait_for_image_and_click('find_match_button')
        wait_for_image_and_click('confirm_attack_button')
        wait_for_image('end_battle_button')
        calibrate()
        run_attack()
        if not check_for_image('return_home_button'):
            wait_for_any_image(['end_battle_button', 'surrender_button'])
            click_image('surrender_button')
            wait_for_image_and_click('confirm_surrender_button')
        wait_for_image_and_click('return_home_button')


def print_mode():
    start('s')
    print('running')
    while not key_down('q'):
        shot = take_screenshot()
        print_if_present(shot, 'attack_button', 1)
        print_if_present(shot, 'find_match_button', 2)
        print_if_present(shot, 'confirm_attack_button', 3)
        print_if_present(shot, 'end_battle_button', 4)
        print_if_present(shot, 'confirm_surrender_button', 5)
        print_if_present(shot, 'return_home_button', 6)
        sleep(0.1)


loop()
# print_mode()
# click_mode()

# def snip(region):
#     img = take_screenshot_with_region(region)
#     display_image(img)

# click_mode()
# start('s')
# wait_for_image_and_click('star')
