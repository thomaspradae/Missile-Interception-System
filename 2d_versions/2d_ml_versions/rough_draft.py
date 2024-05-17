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
            if self.coordinates[1] < target.coordinates[1]:
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
    def __init__(self, type):
        self.type = type
        self.coordinates = np.array([0, 0])
        self.radius = 0.2
    
    def create_attack_missile(self, attack):
        self.speed = 1
        self.theta = attack.attack_theta_rad
        self.coordinates = attack.coordinates
        self.fired = False
        return self.coordinates, self.theta, self.speed, self.fired
    
    def fire_missile(self, global_time):
        self.fired = True
        self.fired_time = global_time
        return self.fired, self.fired_time
    
    def create_defense_missile(self, defense, global_time, defense_missiles):
        self.speed = 1
        self.theta = None
        self.coordinates = defense.coordinates
        self.fired = False
        self.fired_time = None 
        self.missile_clock = global_time - self.fired_time
        self.append(defense_missiles)

class Environment:
    def __init__(self):
        self.global_time = 0
        pass

    def calculate_distance(self, point1, point2):
        np.sqrt(np.sum((point1 - point2) ** 2))

    def check_impact(self, missile, target):
        for missile in self.defense_missiles:
            if self.calculate_distance(self.attack_missile.coordinates, missile.coordinates) < missile.radius + target.radius:
                return 100, True
            
        if self.calculate_distance(self.attack_missile.coordinates, target.coordinates) < missile.radius + target.radius:
            return -100, True

    def update_missile_positions(self):
        self.attack_missile.coordinates[0] += self.attack_missile.speed * self.global_time * math.cos(self.attack_missile.theta)
        self.attack_missile.coordinates[1] += self.attack_missile.speed * self.global_time * math.sin(self.attack_missile.theta)
        for missile in self.defense_missiles:
            missile.coordinates[0] += missile.speed * missile.missile_clock * math.cos(missile.theta)
            missile.coordinates[1] += missile.speed * missile.missile_clock * math.sin(missile.theta)
    
    def set_episode(self, global_time):
        self.target = Point("target")
        self.defense = Point("defense")
        self.attack = Point("attack")
        
        self.target.create_target()
        self.defense.create_defense(self.target)
        self.attack.create_attack(self.target)

        self.attack_missile = Missile("attack")
        self.attack_missile.create_attack_missile(self.attack)
        self.attack_missile.fire_missile(self.global_time)

        self.defense_missiles = []

        self.global_time = 0

        self.iteration_over = False
        self.episode_over = False

    # Retrying the iteration is simply resetting the attack and defense missiles (all other points are the same)
    def retry_iteration(self):
        self.attack_missile = Missile("attack", self.attack.coordinates, self.target.coordinates)
        self.attack_missile.create_missile()
        self.attack_missile.fire_missile()

        self.attack_missiles = []

        self.global_time = 0

        self.iteration_over = False
        self.episode_over = False

    def step(self):
        self.global_time += 0.01
        self.update_missile_positions()
        self.attack_missile_to_target = self.calculate_distance(self.attack_missile.coordinates, self.target.coordinates)


# (0.2) Create the environment. -------------------------------------------------------
env = Environment()
env.set_episode(env.global_time)
print("Environment created.")
print("Environment init time:", env.global_time)
print("Target coordinates:", env.target.coordinates)
print("Defense coordinates:", env.defense.coordinates)
print("Attack coordinates:", env.attack.coordinates)
print("Attack missile coordinates:", env.attack_missile.coordinates)
print("Attack missile theta:", env.attack_missile.theta)
print("Attack missile speed:", env.attack_missile.speed)
print("Attack missile fired:", env.attack_missile.fired)
print("Attack missile fired time:", env.attack_missile.fired_time)
print("Defense missiles:", env.defense_missiles)
print("Global time:", env.global_time)

env.step()
print("Environment init time:", env.global_time)
env.update_missile_positions()
print("Attack missile updated coordinates:", env.attack_missile.coordinates)

for i in range(100):
    env.step()
    print("Attack missile updated coordinates:", env.attack_missile.coordinates)
    print("Environment init time:", env.global_time)
