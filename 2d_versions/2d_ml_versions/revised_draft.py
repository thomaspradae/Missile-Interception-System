import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
import time
import math

# (0.1) Create the attack, target and defense starting positions. ---------------------

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
    
    def create_attack(self, target):
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
        
        # Create attack_theta
        self.AT_abs_length = math.hypot(self.coordinates[0] - target.coordinates[0], self.coordinates[1] - target.coordinates[1])
        self.length_adjacent_r = abs(target.coordinates[0] - self.coordinates[0])
        self.attack_theta_rad = math.acos(self.length_adjacent_r / self.AT_abs_length)

        if self.coordinates[0] < target.coordinates[0]:
            if self.attack.coordinates[1] < self.target.coordinates[1]:
                self.attack_theta_rad = self.attack_theta_rad
            else:
                self.attack_theta_rad = ((2 * math.pi) - self.attack_theta_rad)
            
        else:
            if self.coordinates[1] < target.coordinates[1]:
                self.attack_theta_rad = ((math.pi) - self.attack_theta_rad)
            else:
                self.attack_theta_rad = ((math.pi) + self.attack_theta_rad)

        return self.coordinates, self.attack_theta_rad
    

class Missile:
    def __init__(self, type, target, attack):
        self.type = type
        self.coordinates = np.array([0, 0])
        self.radius = 0.2
    
    def create_missile(self, attack):
        self.speed = 1
        self.theta = attack.attack_theta_rad
        self.coordinates = attack.coordinates
        self.fired = False
        return self.coordinates, self.theta, self.speed, self.fired
    
    def fire_missile(self):
        self.fired = True
        return self.fired
        


# (0.2) Create the environment. -------------------------------------------------------

class Environment:
    def __init__(self):
        pass

    def reset(self):
        self.target = Point("target")
        self.defense = Point("defense")
        self.attack = Point("attack")
        
        self.target.create_target()
        self.defense.create_defense(self.target)
        self.attack.create_attack(self.target)

        self.attack_missile = Missile("attack", self.attack.coordinates, self.target.coordinates)
        self.attack_missile.create_missile()
        self.attack_missile.fire_missile()


        
        
#     def retry():