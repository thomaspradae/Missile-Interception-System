import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
import time
import math


class Point: 
    def __init__(self, type):
        self.type = type
        self.coordinates = np.array([0, 0])
        self.radius = 0.2

    def create_target(self):
        x = random.uniform(-3.0, 3.0)
        y = random.uniform(-2.0, 2.0)
        self.coordinates = np.array([x, y])
        self.theta = 0
        return self.coordinates, self.theta
    
    def create_defense(self, target):
        x = random.uniform((target.coordinates[0] - self.radius) - 1.5, (target.coordinates[0] + self.radius) + 1.5)
        y = random.uniform((target.coordinates[1] - self.radius) - 1.5, (target.coordinates[1] + self.radius) + 1.5)
        self.coordinates = np.array([x, y])
        return self.coordinates
    
    def create_attack(self, target, defense):
        x_side_left = random.uniform(-9.5, (target.coordinates[0] - self.radius) - 2)
        x_side_right = random.uniform((target.coordinates[0] + self.radius) + 2, 9.5)
        y_below = random.uniform((target.coordinates[1] - self.radius) - 2, -9.5)
        y_above = random.uniform((target.coordinates[1] + self.radius) + 2, 9.5)
        x_inclusive = random.uniform(-9.5, 9.5)
        y_inclusive = random.uniform(-9.5, 9.5)
        y_below_x_inclusive = np.array([x_inclusive, y_below])
        y_above_x_inclusive = np.array([x_inclusive, y_above])
        x_left_y_inclusive = np.array([x_side_left, y_inclusive])
        x_right_y_inclusive = np.array([x_side_right, y_inclusive])

        self.coordinates = random.choice([y_below_x_inclusive, y_above_x_inclusive, x_left_y_inclusive, x_right_y_inclusive])
        return self.coordinates


class Environment:
    def __init__(self):
        self.target = Point("target")
        self.defense = Point("defense")
        self.attack = Point("attack")

        self.target.create_target()
        self.defense.create_defense(self.target)
        self.attack.create_attack(self.target, self.defense)

        # Define absolute lengths (from center to center)
        self.AT_abs_length = math.hypot(self.attack.coordinates[0] - self.target.coordinates[0], self.attack.coordinates[1] - self.target.coordinates[1])
        self.AD_abs_length = math.hypot(self.attack.coordinates[0] - self.defense.coordinates[0], self.attack.coordinates[1] - self.defense.coordinates[1])
        self.TD_abs_length = math.hypot(self.target.coordinates[0] - self.defense.coordinates[0], self.target.coordinates[1] - self.defense.coordinates[1])

        # Define attack theta
        self.length_adjacent_r = abs(self.target.coordinates[0] - self.attack.coordinates[0])
        self.attack_theta_rad = math.acos(self.length_adjacent_r / self.AT_abs_length)

        if self.attack.coordinates[0] < self.target.coordinates[0]:
            if self.attack.coordinates[1] < self.target.coordinates[1]:
                print("Attack is in the 3rd quadrant")
            else:
                print("Attack is in the 2nd quadrant")
                self.attack_theta_rad = ((2 * math.pi) - self.attack_theta_rad)
            
        else:
            if self.attack.coordinates[1] < self.target.coordinates[1]:
                print("Attack is in the 4th quadrant")
                self.attack_theta_rad = ((math.pi) - self.attack_theta_rad)
            else:
                print("Attack is in the 1st quadrant")
                self.attack_theta_rad = ((math.pi) + self.attack_theta_rad)

        self.coords = [self.target.coordinates, self.defense.coordinates, self.attack.coordinates]
        self.radii = [self.target.radius, self.defense.radius, self.attack.radius]

env_instance = Environment()
print("Target Coordinates:", env_instance.target.coordinates)
print("Defense Coordinates:", env_instance.defense.coordinates)
print("Attack Coordinates:", env_instance.attack.coordinates)
print("attack_theta:", env_instance.attack_theta_rad)

# target = Point("target")
# target.create_target()
# print("Target Coordinates:", target.coordinates)

# defense = Point("defense")
# defense.create_defense(target)
# print("Defense Coordinates:", defense.coordinates)

# attack = Point("attack")
# attack.create_attack(target, defense)
# print("Attack Coordinates:", attack.coordinates)

# ----------------------------------------------------------------------------------------------------------------------------

# coords = [target.coordinates, defense.coordinates, attack.coordinates]
# radii = [target.radius, defense.radius, attack.radius]

fig, ax = plt.subplots()
plt.xlim(-10, 10)
plt.ylim(-10, 10)
ax.set_aspect( 1 )

plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.grid(True)

target_area = plt.Circle((env_instance.target.coordinates[0], env_instance.target.coordinates[1]), env_instance.target.radius, color='red', fill=False)
defense_area = plt.Circle((env_instance.defense.coordinates[0], env_instance.defense.coordinates[1]), env_instance.defense.radius, color='yellow', fill=False)
attack_area = plt.Circle((env_instance.attack.coordinates[0], env_instance.attack.coordinates[1]), env_instance.attack.radius, color='black', fill=False)

ax.add_artist(target_area)
ax.add_artist(defense_area)
ax.add_artist(attack_area)

time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)  # Text to display time

# Global Clock
start_time = time.time()

def init():
    target_area.set_center((env_instance.target.coordinates[0], env_instance.target.coordinates[1]))
    target_area.set_radius(env_instance.target.radius)

    defense_area.set_center((env_instance.defense.coordinates[0], env_instance.defense.coordinates[1]))
    defense_area.set_radius(env_instance.defense.radius)

    attack_area.set_center((env_instance.attack.coordinates[0], env_instance.attack.coordinates[1]))
    attack_area.set_radius(env_instance.attack.radius)
    time_text.set_text('')
    return attack_area, time_text

def update(frame):
    current_time = time.time() - start_time
    seconds = int(current_time)
    milliseconds = int((current_time - seconds) * 1000)

    attack_coordinates_var_x = env_instance.attack.coordinates[0] + (current_time * 1) * math.cos(env_instance.attack_theta_rad)
    attack_coordinates_var_y = env_instance.attack.coordinates[1] + (current_time * 1) * math.sin(env_instance.attack_theta_rad)

    attack_area.set_center((attack_coordinates_var_x, attack_coordinates_var_y))
    attack_area.set_radius(env_instance.attack.radius)

    time_text.set_text('Time: {:02d}:{:03d}'.format(seconds, milliseconds))

    return attack_area, time_text

ani = FuncAnimation(fig, update, frames=None, init_func=init, interval=10, blit=True)

plt.show()

# # Initialize the plot elements
# target_circle = plt.Circle((0, 0), 1, color='red', fill=False)
# defense_circle = plt.Circle((0, 0), 1, color='yellow', fill=False)

# circle = plt.Circle((0, 0), 1, color='blue', fill=False)
# ax.add_artist(circle)
# ax.add_artist(target_circle)
# ax.add_artist(defense_circle)
# time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)  # Text to display time

# # Global clock
# start_time = time.time()

# def init():
#     circle.set_center((attack.coordinates[0], attack.coordinates[1])) 

#     target_circle.set_center((target.coordinates[0], target.coordinates[1])) 
#     target_circle.set_radius(target.radius)

#     defense_circle.set_center((defense.coordinates[0], defense.coordinates[1]))
#     defense_circle.set_radius(defense.radius)

#     time_text.set_text('')
#     return circle, time_text

# def update(frame):
#     current_time = time.time() - start_time
#     seconds = int(current_time)
#     milliseconds = int((current_time - seconds) * 1000)

#     attack.coordinates[0] = current_time * 1
#     attack.coordinates[1] = attack.coordinates[1]


#     circle.set_center((attack.coordinates[0], attack.coordinates[1]))  # Set the center of the circle to the new coordinates    
#     circle.set_radius(attack.radius)  # Set the radius of the circle to the new radius

#     time_text.set_text('Time: {:02d}:{:03d}'.format(seconds, milliseconds))

#     return circle, time_text

# ani = FuncAnimation(fig, update, frames=None, init_func=init, interval=10, blit=True)

# plt.show()

# # Global clock
# start_time = time.time()



# def init():
#     for i in range(len(coords)):
#         circle = plt.Circle((coords[i][0], coords[i][1]), radii[i], fill=False)
#         ax.add_artist(circle)
#         time_text.set_text('')
#     return circle, time_text

# def update(frame):
#     current_time = time.time() - start_time
#     seconds = int(current_time)
#     milliseconds = int((current_time - seconds) * 1000)

#     target.coordinates[0] = current_time * 1
#     target.coordinates[1] = 0

#     circle = plt.Circle((target.coordinates[0], target.coordinates[1]), target.radius, fill=False)

#     time_text.set_text('Time: {:02d}:{:03d}'.format(seconds, milliseconds))

#     return circle, time_text

# ani = FuncAnimation(fig, update, frames=None, init_func=init, interval=10, blit=True)


# for i in range(len(coords)):
#     circle = plt.Circle((coords[i][0], coords[i][1]), radii[i], fill=False)
#     ax.set_aspect( 1 )
#     ax.add_artist(circle)

# def update(frame):
#     current_time = time.time() - start_time
#     seconds = int(current_time)
#     milliseconds = int((current_time - seconds) * 1000)

#     time_text.set_text('Time: {:02d}:{:03d}'.format(seconds, milliseconds))
#     target.coordinates[0] = current_time * 1
#     target.coordinates[1] = 0

#     circle = plt.Circle((target.coordinates[0], target.coordinates[1]), target.radius, fill=False)

#     time_text.set_text('Time: {:02d}:{:03d}'.format(seconds, milliseconds))

#     return circle, time_text

# ani = FuncAnimation(fig, update, frames=None, init_func=None, interval=10, blit=True)


# for i in range(len(coords)):
#     circle = Circle((coords[i][0], coords[i][1]), 5, edgecolor='black', facecolor='None')

# plt.scatter(target.coordinates[0], target.coordinates[1], color='red', label='Point 1', s=10)
# plt.scatter(defense.coordinates[0], defense.coordinates[1], color='yellow', label='Point 2', s=10)
# plt.scatter(attack.coordinates[0], attack.coordinates[1], color='black', label='Point 3', s=10)


# plt.show()
