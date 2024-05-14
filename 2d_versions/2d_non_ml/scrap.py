import matplotlib.pyplot as plt
import numpy as np
import math
import random 
import pandas as pd


# --------------------------------------------------------------------------
attack_x = 2
attack_y = 2
attack_coords = np.array([attack_x, attack_y])

target_x = 0
target_y = 0
target_coords = np.array([target_x, target_y])

r_coords = np.array([target_coords[0], attack_coords[1]])
length_r = abs(target_coords[1] - attack_coords[1])
TA_length = math.hypot(target_coords[0] - attack_coords[0], target_coords[1] - attack_coords[1])
theta_rad = math.acos(length_r/TA_length)
theta_deg = math.degrees(theta_rad)

print("Theta in degrees:", theta_deg)
print("Theta in radians:", theta_rad)

# --------------------------------------------------------------------------
length = 3
angle = 90
theta = math.radians(angle)

if attack_coords[0] < target_coords[0]:
    if attack_coords[1] < target_coords[1]:
        print("Attack is in the 3rd quadrant")
        new_x_val = attack_coords[0] + length*math.cos(theta_rad)
        new_y_val = attack_coords[1] + length*math.sin(theta_rad)

    else:
        print("Attack is in the 2nd quadrant")
        theta_deg = 360 - theta_deg
        theta_rad = math.radians(theta_deg)
        # new_x_val = attack_coords[0] - length*math.cos(theta_rad)
        new_x_val = attack_coords[0] + length*math.cos(theta_rad)
        new_y_val = attack_coords[1] + length*math.sin(theta_rad)

else:
    if attack_coords[1] < target_coords[1]:
        print("Attack is in the 4th quadrant")
        theta_deg = 180 - theta_deg
        theta_rad = math.radians(theta_deg)
        # new_x_val = attack_coords[0] - length*math.cos(theta_rad)
        new_x_val = attack_coords[0] + length*math.cos(theta_rad)
        new_y_val = attack_coords[1] + length*math.sin(theta_rad)

    else:
        print("Attack is in the 1st quadrant")
        theta_deg = 180 + theta_deg
        theta_rad = math.radians(theta_deg)
        new_x_val = attack_coords[0] - length*math.cos(theta_rad)
        new_y_val = attack_coords[1] - length*math.sin(theta_rad)
    

new_x_val = attack_coords[0] + length*math.cos(theta_rad)
new_y_val = attack_coords[1] + length*math.sin(theta_rad)
new_coords = np.array([new_x_val, new_y_val])


# x_val = 2.5
# y_val = 2.5
# coords = np.array([x_val, y_val])

# length = 1
# angle = 270
# theta = math.radians(angle)

# new_x = coords[0] + length*math.sin(theta)
# new_y = coords[1] + length*math.cos(theta)
# new_coords = np.array([new_x, new_y])

fig, ax = plt.subplots()
plt.xlim(-10, 10)
plt.ylim(-10, 10)

plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.grid(True)

plt.scatter(attack_coords[0], attack_coords[1], color='red')
plt.scatter(new_coords[0], new_coords[1], color='blue')
plt.scatter(target_coords[0], target_coords[1], color='green')
plt.scatter(r_coords[0], r_coords[1], color='purple')
plt.plot([attack_coords[0], new_coords[0]], [attack_coords[1], new_coords[1]], color='black', linestyle='-', label='Attack to Target')
plt.plot([attack_coords[0], target_coords[0]], [attack_coords[1], target_coords[1]], color='black', linestyle='-', label='Attack to Target')

# plt.text(coords[0], coords[1], 'B', ha='right')
# plt.text(new_coords[0], new_coords[1], 'A', ha='right')
plt.show()


