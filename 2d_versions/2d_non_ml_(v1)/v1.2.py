# -------------------------------------------------------------------------------
# This is the second version of the algorithm. In this case the attacker can have 
# a different y value thatn the defense. 
# -------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import math
import random 
import pandas as pd

# 1. Create Points
# Set seed for reproducibility
# random.seed(42) 

class Point: 
    def __init__(self, type):
        self.type = type
        self.coordinates = np.array([0, 0])

    def create_target(self):
        x = random.uniform(-3.0, 3.0)
        y = random.uniform(2.0, 6.0)
        self.coordinates = np.array([x, y])
        return self.coordinates
    
    def create_defense(self, target):
        x = random.uniform(target.coordinates[0] - 1.5, target.coordinates[0] + 1.5)
        y = random.uniform(target.coordinates[1] - 1.5, target.coordinates[1]-0.1)
        self.coordinates = np.array([x, y])
        return self.coordinates
    
    def create_attack(self, target, defense):
        x_side1 = random.uniform(-9.0, target.coordinates[0] - 2)
        x_side2 = random.uniform(target.coordinates[0] + 2, 9.0)
        y_deep = random.uniform(-9.0, target.coordinates[1] - 0.1)
        x_below = random.uniform(target.coordinates[0] - 2, target.coordinates[0] + 2)
        y_below = random.uniform(-9.0, target.coordinates[1] - 2)

        coord_side1 = np.array([x_side1, y_deep])
        coord_side2 = np.array([x_side2, y_deep])
        coord_below = np.array([x_below, y_below])

        self.coordinates = random.choice([coord_side1, coord_side2, coord_below])
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

    if attack.coordinates[0] < defense.coordinates[0]:
        # If the attack is to the left of the defense, then the angle of interest is theta
        intercept_y = attack.coordinates[1] + AI_length*math.sin(theta_rad)
        intercept_x = attack.coordinates[0] + AI_length*math.cos(theta_rad)

    else: 
        # If the attack is to the right of the defense, then the angle of interest is 180 - theta
        intercept_y = attack.coordinates[1] + AI_length*math.sin(math.pi - theta_rad)
        intercept_x = attack.coordinates[0] + AI_length*math.cos(math.pi - theta_rad)

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

# # Create an empty DataFrame to store the results
# columns = ['Target_X', 'Target_Y', 'Defense_X', 'Defense_Y', 'Attack_X', 'Attack_Y', 'Intercept_X', 'Intercept_Y']
# df = pd.DataFrame(columns=columns)

# # Number of iterations
# num_iterations = 50000

# for i in range(num_iterations):
#     target = Point("target")
#     target.create_target()

#     defense = Point("defense")
#     defense.create_defense(target)

#     attack = Point("attack")
#     attack.create_attack(target, defense)

#     intercept_point = intercept(defense, attack, target)
#     print("Itteration no:", i)

#     # Append data to the DataFrame
#     df = df.append({
#         'Target_X': target.coordinates[0],
#         'Target_Y': target.coordinates[1],
#         'Defense_X': defense.coordinates[0],
#         'Defense_Y': defense.coordinates[1],
#         'Attack_X': attack.coordinates[0],
#         'Attack_Y': attack.coordinates[1],
#         'Intercept_X': intercept_point[0],
#         'Intercept_Y': intercept_point[1],
#     }, ignore_index=True)


# # Now df contains your data for 10,000 iterations
# print(df)

# df.to_csv("50k_iterations_v2.csv")
