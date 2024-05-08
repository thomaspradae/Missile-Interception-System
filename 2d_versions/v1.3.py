# -------------------------------------------------------------------------------
# This is the third version of the algorithm (2D Version (v.1.3)). In this case the attacker is only
# limited by his length to the target. Meaning, he isn't limited to being under the target (y value).
# -------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import math
import random 
import pandas as pd

# 1. Create Points
# Set seed for reproducibility
# Save this one
# random.seed(420) 
# random.seed(423) 
# random.seed(421)


class Point: 
    def __init__(self, type):
        self.type = type
        self.coordinates = np.array([0, 0])

    def create_target(self):
        x = random.uniform(-3.0, 3.0)
        y = random.uniform(-2.0, 2.0)
        self.coordinates = np.array([x, y])
        return self.coordinates
    
    def create_defense(self, target):
        x = random.uniform(target.coordinates[0] - 1.5, target.coordinates[0] + 1.5)
        y = random.uniform(target.coordinates[1] - 1.5, target.coordinates[1] + 1.5)
        self.coordinates = np.array([x, y])
        return self.coordinates
    
    def create_attack(self, target, defense):
        x_side_left = random.uniform(-9.5, target.coordinates[0] - 2)
        x_side_right = random.uniform(target.coordinates[0] + 2, 9.5)
        y_below = random.uniform(target.coordinates[1] - 2, -9.5)
        y_above = random.uniform(target.coordinates[1] + 2, 9.5)
        x_inclusive = random.uniform(-9.5, 9.5)
        y_inclusive = random.uniform(-9.5, 9.5)
        y_below_x_inclusive = np.array([x_inclusive, y_below])
        y_above_x_inclusive = np.array([x_inclusive, y_above])
        x_left_y_inclusive = np.array([x_side_left, y_inclusive])
        x_right_y_inclusive = np.array([x_side_right, y_inclusive])

        self.coordinates = random.choice([y_below_x_inclusive, y_above_x_inclusive, x_left_y_inclusive, x_right_y_inclusive])
        return self.coordinates

target = Point("target")
target.create_target()
print("Target Coordinates:", target.coordinates)

defense = Point("defense")
defense.create_defense(target)
print("Defense Coordinates:", defense.coordinates)

attack = Point("attack")
attack.create_attack(target, defense)
print("Attack Coordinates:", attack.coordinates)

# Some quick visualization 
adjacent_Rcoordinates = np.array([target.coordinates[0], attack.coordinates[1]])

def intercept(defense, attack, target):
    TD_length = math.hypot(target.coordinates[0] - defense.coordinates[0], target.coordinates[1] - defense.coordinates[1])
    TA_length = math.hypot(target.coordinates[0] - attack.coordinates[0], target.coordinates[1] - attack.coordinates[1])
    DA_length = math.hypot(defense.coordinates[0] - attack.coordinates[0], defense.coordinates[1] - attack.coordinates[1])

    if TA_length < TD_length:
            return "Intercept not possible"
    
    # Use sine and cosine rule to get the angle theta and length AI
    td_angle_rad = math.acos((TA_length**2 + DA_length**2 - TD_length**2)/(2*TA_length*DA_length)) 
    td_angle_deg = math.degrees(td_angle_rad)
    ad_angle_deg = 180 - 2*td_angle_deg
    ad_angle_rad = math.radians(ad_angle_deg)
    AI_length = DA_length*(math.sin(td_angle_rad)/math.sin(ad_angle_rad)) 
    print("AI_length:", AI_length)
    print("td_angle_deg:", td_angle_deg)

    # To find the intercept point, we need to know the angle of the attack with respect to the x axis
    # For this we make a right triangle using A and T, let's call the point R (for right angle) for
    # the point where (xR, yR) = (xT, yA). Then we can use Soh Cah Toa to find the angle of interest

    # The hypotenuse of the triangle is simply TA, let's use the adjacent as the x distance from T to R
    legnth_adacent_R = abs(target.coordinates[0] - attack.coordinates[0])
    print("target.coordinates[0]:", target.coordinates[0])
    print("attack.coordinates[0]:", attack.coordinates[0])
    print("legnth_adacent_R:", legnth_adacent_R)

    theta_rad = math.acos(legnth_adacent_R/TA_length)
    theta_deg = math.degrees(theta_rad)
    print("theta_deg:", theta_deg)
    print("theta_rad:", theta_rad)

    if attack.coordinates[0] < target.coordinates[0]:
        if attack.coordinates[1] < target.coordinates[1]:
            print("Attack is in the 3rd quadrant")
        else: 
            print("Attack is in the 2nd quadrant")
            theta_rad = math.radians(360 - theta_deg)
    else:
        if attack.coordinates[1] < target.coordinates[1]:
            print("Attack is in the 4th quadrant")
            theta_rad = math.radians(180 - theta_deg)
        else:
            print("Attack is in the 1st quadrant")
            theta_rad = math.radians(180 + theta_deg)
        
    intercept_x = attack.coordinates[0] + AI_length*math.cos(theta_rad)
    intercept_y = attack.coordinates[1] + AI_length*math.sin(theta_rad)    

    intercept_coordinates = np.array([intercept_x, intercept_y])
    return intercept_coordinates

intercept_point = intercept(defense, attack, target)
print("Intercept Point:")
print(intercept_point)
intercept_point = intercept(defense, attack, target)
print("Intercept Point")
print(intercept_point)

# 2. Create the space from -10 to 10 in both axes
fig, ax = plt.subplots()
plt.xlim(-10, 10)
plt.ylim(-10, 10)

# 1.1 Draw x and y axes and gridlines
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.grid(True)

plt.scatter(target.coordinates[0], target.coordinates[1], color='red', label='Point 1')
plt.scatter(defense.coordinates[0], defense.coordinates[1], color='yellow', label='Point 2')
plt.scatter(attack.coordinates[0], attack.coordinates[1], color='black', label='Point 3')
plt.scatter(intercept_point[0], intercept_point[1], color='green', label='Point 4')
plt.scatter(adjacent_Rcoordinates[0], adjacent_Rcoordinates[1], color='blue', label='Point 5')

plt.plot([attack.coordinates[0], target.coordinates[0]], [attack.coordinates[1], target.coordinates[1]], color='black', linestyle='-', label='Attack to Target')
plt.plot([defense.coordinates[0], intercept_point[0]], [defense.coordinates[1], intercept_point[1]], color='purple', linestyle='--', label='Defense to Intercept')

plt.text(target.coordinates[0], target.coordinates[1], 'T', ha='right')
plt.text(defense.coordinates[0], defense.coordinates[1], 'D', ha='right')
plt.text(attack.coordinates[0], attack.coordinates[1], 'A', ha='right')
plt.text(intercept_point[0], intercept_point[1], 'I', ha='right')

# offset = 0.3  # Adjust this value as needed
# plt.text(target.coordinates[0], target.coordinates[1] + offset, 'T', ha='center')
# plt.text(defense.coordinates[0], defense.coordinates[1] + offset, 'D', ha='center')
# plt.text(attack.coordinates[0], attack.coordinates[1] + offset, 'A', ha='center')
# plt.text(intercept_point[0], intercept_point[1] + offset, 'I', ha='center')

plt.show()