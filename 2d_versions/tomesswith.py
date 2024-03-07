import matplotlib.pyplot as plt
import numpy as np
import math


def intercept(defense, attack, target):
    TD_length = math.hypot(target.coordinates[0] - defense.coordinates[0], target.coordinates[1] - defense.coordinates[1])
    TA_length = math.hypot(target.coordinates[0] - attack.coordinates[0], target.coordinates[1] - attack.coordinates[1])
    DA_length = math.hypot(defense.coordinates[0] - attack.coordinates[0], defense.coordinates[1] - attack.coordinates[1])
    td_angle = math.acos((TA_length**2 + DA_length**2 - TD_length**2)/(2*TA_length*DA_length)) 
    ad_angle = 180 - 2*td_angle
    AI_length = DA_length*(math.sin(td_angle)/math.sin(ad_angle)) 

    if attack.coordinates[0] > defense.coordinates[0]:
        theta = 180 - td_angle
        intercept_y = attack.coordinates[1] + AI_length*math.sin(theta)
        if attack.coordinates[0] >= target.coordinates[0]:
            intercept_x = attack.coordinates[0] - AI_length*math.cos(theta)
        else:
            intercept_x = attack.coordinates[0] + AI_length*math.cos(theta)
    
    else:
        theta = td_angle
        intercept_y = attack.coordinates[1] + AI_length*math.sin(theta)
        if attack.coordinates[0] >= target.coordinates[0]:
            intercept_x = attack.coordinates[0] - AI_length*math.cos(theta)
        else:
            intercept_x = attack.coordinates[0] + AI_length*math.cos(theta)

    intercept_coordinates = np.array([intercept_x, intercept_y])
    return intercept_coordinates

class Point: 
    def __init__(self, type):
        self.type = type
        self.coordinates = np.array([0, 0])

# Create instances of Point representing defense, attack, and target
defense = Point("defense")
attack = Point("attack")
target = Point("target")

# Assign coordinates for defense, attack, and target
defense.coordinates = np.array([-3, -3])
attack.coordinates = np.array([2, 5])
target.coordinates = np.array([-1, -1])

# Calculate intercept
intercept_distance = intercept(defense, attack, target)
print("Intercept Distance:", intercept_distance)

# Plotting
plt.scatter(defense.coordinates[0], defense.coordinates[1], color='blue', label='Defense')
plt.scatter(attack.coordinates[0], attack.coordinates[1], color='red', label='Attack')
plt.scatter(target.coordinates[0], target.coordinates[1], color='green', label='Target')

# Draw lines connecting points
plt.plot([defense.coordinates[0], attack.coordinates[0]], [defense.coordinates[1], attack.coordinates[1]], color='black', linestyle='--')
plt.plot([target.coordinates[0], attack.coordinates[0]], [target.coordinates[1], attack.coordinates[1]], color='black', linestyle='--')
plt.plot([target.coordinates[0], defense.coordinates[0]], [target.coordinates[1], defense.coordinates[1]], color='black', linestyle='--')

# Add text for intercept distance
plt.text(target.coordinates[0] - 0.5, target.coordinates[1] - 0.5, f'Intercept = {intercept_distance:.2f}', color='purple')

# Customize plot
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Intercept Visualization')
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.legend()

# Show plot
plt.show()
