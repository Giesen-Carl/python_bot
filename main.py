from script_utils import *

while True:
    try:
        execute_script('script.bs')
        #execute_script('event_attack.bs')
        #execute_script('test.bs')
    except:
        print('Breaking Loop')

# valk_top = [
#     (240, 660, 1020, 80),
#     (1020, 80, 1800, 660)
# ]
# valk_bot = [
#     (230, 330, 980, 885),
#     (980, 885, 1740, 330)
# ]