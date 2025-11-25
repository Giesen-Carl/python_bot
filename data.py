regions = {
    'attack_button': (20, 890, 170, 170),
    'find_match_button': (80, 680, 390, 140),
    'confirm_attack_button': (1450, 880, 340, 80),
    'end_battle_button': (15, 815, 200, 80),
    'surrender_button': (15, 815, 200, 80),
    'confirm_surrender_button': (970, 590, 330, 150),
    'return_home_button': (820, 860, 275, 120),
    # 'star': (1668, 847, 20, 20)
    'star': (1658, 837, 40, 40)
}
troop_buttons = {
    'valk': (335, 960),
    'siege': (465, 960),
    'king': (605, 960),
    'queen': (720, 960),
    'warden': (845, 960),
    'champion': (950, 960),
    'earthquake': (1100, 960),
}

troop_placements = {
    'siege': (220, 520),
    'king': (550, 790),
    'queen': (826, 35),
    'warden': (1511, 807),
    'champion': (1790, 520),
}
valk_placement_lines = [
    (213, 481, 823, 40),
    (208, 543, 653, 884),
    (1127, 18, 1803, 514),
    (1341, 885, 1803, 552)
]
def line_2_range(line, steps):
    x1, y1, x2, y2 = line
    arr = []
    x_step_size = (x2 - x1) / (steps - 1)
    y_step_size = (y2 - y1) / (steps - 1)
    for i in range(0, steps, 1):
        arr.append((round(x1 + x_step_size * i), round(y1 + y_step_size * i)))
    return arr
arr = []
for line in valk_placement_lines:
    arr.append(line_2_range(line, 11))
valk_placements = [x for sub in arr for x in sub]

earthquake_placements = [
    (463, 517),
    (587, 511),
    (745, 511),
    (887, 499),
    (986, 503),
    (1211, 713),
    (1357, 603),
    (1115, 793),
    (1091, 607),
    (1267, 475),
    (997, 683),
]
