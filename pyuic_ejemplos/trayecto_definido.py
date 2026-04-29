"""
Description: Move line(linear motion)
"""

import os
import sys
import time
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI


#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################


arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

arm.move_gohome(wait=True)

arm.set_position(x=100, y=-50, z=250, roll=180, pitch=0, yaw=0, speed=100, wait=True)
print(arm.get_position(), arm.get_position(is_radian=True))
arm.set_position(x=-44, y=-170, z=250, roll=180, pitch=0, yaw=0, speed=100, wait=True)
print(arm.get_position(), arm.get_position(is_radian=True))
cont = 0
x = 's'
while x != "a":
    x = input()
with open("Batma_logo_0001.ngc", 'r') as fp:
    lines = sum(1 for line in fp)
    print('Total Number of lines:', lines)
start_time = time.time()
with open('F1_gcode_0001.ngc') as gcode:
    for line in gcode:
        line = line.strip()
        coord = re.findall(r'[XY].?\d+.\d+', line)
        if coord :
            xx = coord[0].split('X')
            xx = xx[1]
            yy = coord[1].split('Y')
            yy = yy[1]
            if float(yy) > 150:
                arm.set_position(x=-44 - float(xx) , y=-228 - float(yy), z=210, roll=180, pitch=0, yaw=0, speed=100, wait=True)
            if float(yy) > 50 and float(yy) < 150:
                arm.set_position(x=-44 - float(xx) , y=-228 - float(yy), z=209, roll=180, pitch=0, yaw=0, speed=100, wait=True)
            if float(yy) < 50:
                arm.set_position(x=-44 - float(xx) , y=-228 - float(yy), z=209, roll=180, pitch=0, yaw=0, speed=100, wait=True)
            cont = cont + 1
            if cont % 100 == 0:
                 
                print (str(cont) + " lines. Lines to finish "  + str(lines - cont) + "\r")
            
print("--- %s seconds ---" % (time.time() - start_time))
arm.set_position(x=-44, y=-135, z=250, roll=180, pitch=0, yaw=0, speed=100, wait=True)
print(arm.get_position(), arm.get_position(is_radian=True))
arm.set_position(x=-44, y=-335, z=250, roll=180, pitch=0, yaw=0, speed=100, wait=True)
print(arm.get_position(), arm.get_position(is_radian=True))
arm.set_position(x=-44, y=-335, z=250, roll=180, pitch=0, yaw=0, speed=100, wait=True)
print(arm.get_position(), arm.get_position(is_radian=True))

arm.move_gohome(wait=True)
arm.disconnect()