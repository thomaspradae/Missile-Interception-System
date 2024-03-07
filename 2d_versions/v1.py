import matplotlib.pyplot as plt
import numpy as np
import math
import random 

# 1. Create Points

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
        x1 = random.uniform(-9.0, target.coordinates[0] - 1.6)
        x2 = random.uniform(target.coordinates[0] + 1.6, 9.0)
        x = random.choice([x1, x2])
        y = defense.coordinates[1]
        self.coordinates = np.array([x, y])
        return self.coordinates


if __name__ == "__main__":

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
        
        td_angle_rad = math.acos((TA_length**2 + DA_length**2 - TD_length**2)/(2*TA_length*DA_length)) 
        td_angle_deg = math.degrees(td_angle_rad)
        ad_angle_deg = 180 - 2*td_angle_deg
        ad_angle_rad = math.radians(ad_angle_deg)
        AI_length = DA_length*(math.sin(td_angle_rad)/math.sin(ad_angle_rad)) 

        if attack.coordinates[0] > defense.coordinates[0]:
            print("Attack is to the right of defense")
            print("td_angle_deg:", td_angle_deg)
            theta_deg = 180 - td_angle_deg
            print("theta_deg:", theta_deg)
            theta_rad = math.radians(theta_deg)
            intercept_y = attack.coordinates[1] + AI_length*math.sin(theta_rad)
            intercept_x = attack.coordinates[0] + AI_length*math.cos(theta_rad)
        
        else:
            theta_deg = td_angle_deg
            theta_rad = math.radians(theta_deg)
            intercept_y = attack.coordinates[1] + AI_length*math.sin(theta_rad)
            intercept_x = attack.coordinates[0] + AI_length*math.cos(theta_rad)

        intercept_coordinates = np.array([intercept_x, intercept_y])
        return intercept_coordinates

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

    # plt.text(target.coordinates[0], target.coordinates[1], 'T', ha='right')
    # plt.text(defense.coordinates[0], defense.coordinates[1], 'D', ha='right')
    # plt.text(attack.coordinates[0], attack.coordinates[1], 'A', ha='right')
    # plt.text(intercept_point[0], intercept_point[1], 'I', ha='right')

    offset = 0.3  # Adjust this value as needed
    plt.text(target.coordinates[0], target.coordinates[1] + offset, 'T', ha='center')
    plt.text(defense.coordinates[0], defense.coordinates[1] + offset, 'D', ha='center')
    plt.text(attack.coordinates[0], attack.coordinates[1] + offset, 'A', ha='center')
    plt.text(intercept_point[0], intercept_point[1] + offset, 'I', ha='center')

    plt.show()