import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
import time
import math

# Set a mudafuggin seed
random.seed(0)

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
    
    def fire_attack_missile(self, global_time):
        self.fired = True
        self.fired_time = global_time
        return self.fired, self.fired_time
    
    def fire_defense_missile(self, global_time):
        self.fired = True
        self.fired_time = global_time
        self.start_distance = self.distance_defense_to_attack()
        return self.fired, self.fired_time
    
    def create_defense_missile(self, defense, global_time, defense_missiles, theta):
        self.speed = 1
        self.theta = theta
        self.coordinates = defense.coordinates
        self.fired = False
        self.fired_time = 0 
        self.missile_clock = global_time - self.fired_time
        self.defense_missile_to_attack_missile = None
        self.start_distance = None

class Environment:
    def __init__(self):
        self.global_time = 0

        self.target = None
        self.defense = None
        self.attack = None
        self.attack_missile = None
        self.defense_missiles = []

        self.attack_missile_to_target = None

    def set_episode(self, global_time):
        self.target = Point('target')
        self.defense = Point('defense')
        self.attack = Point('attack')

        self.target.create_target()
        self.defense.create_defense(self.target)
        self.attack.create_attack(self.target)

        self.attack_missile = Missile('attack')
        self.attack_missile.create_attack_missile(self.attack)
        self.attack_missile.fire_attack_missile(global_time)
        self.attack_missile_to_target = self.distance_attack_to_target()

        self.defense_missiles = []

    def calculate_distance(self, point1, point2):
        return math.hypot(point1[0] - point2[0], point1[1] - point2[1])
    
    def distance_attack_to_target(self):
        self.attack_missile_to_target = self.calculate_distance(self.attack_missile.coordinates, self.target.coordinates)
        return self.attack_missile_to_target
    
    def distance_defense_to_attack(self):
        for missile in self.defense_missiles:
            missile.defense_missile_to_attack_missile = self.calculate_distance(missile.coordinates, self.attack.coordinates)

    def create_defense_missile(self, defense, global_time, defense_missiles, theta):
        defense_missile = Missile('defense')
        defense_missile.create_defense_missile(defense, global_time, defense_missiles, theta)
        defense_missiles.append(defense_missile)
        return defense_missile
    
    def update_attack_missile_position(self):
        self.attack_missile_coordinates[0] = self.attack.coordinates[0] + self.attack_missile.speed * self.global_time * math.cos(self.attack_missile.theta)
        self.attack_missile_coordinates[1] = self.attack.coordinates[1] + self.attack_missile.speed * self.global_time * math.sin(self.attack_missile.theta)
    
    def update_defense_missile_positions(self):
        for missile in self.defense_missiles:
            missile.coordinates[0] = self.defense.coordinates[0] + missile.speed * missile.missile_clock * math.cos(missile.theta)
            missile.coordiantes[1] = self.defense.coordinates[1] + missile.speed * missile.missile_clock * math.sin(missile.theta)

    def check_impact(self):
        for missile in self.defense_missiles:
            if missile.defense_missile_to_attack_missile < missile.radius + self.attack.radius:
                return 100, True
        
        if env.attack_missile_to_target < self.attack_missile.radius + self.target.radius:
            return -100, True

        return 0, False

    def update_defense_missiles(self):
        if len(self.defense_missiles) > 0:
            self.update_defense_missile_positions()
            self.distance_defense_to_attack()

    def update_world(self):
        self.update_attack_missile_position()
        self.distance_attack_to_target()
        self.update_defense_missiles()

    def step(self, action):
        create_missile, theta, fire_now = action

        if create_missile:
            self.create_defense_missile(self.defense, self.global_time, self.defense_missiles, theta)

        if fire_now:
            self.defense_missiles[0].fire_defense_missile(self.global_time)
            
        if len(self.defense_missiles) > 0:
            self.update_defense_missile_positions()
            self.distance_defense_to_attack()

        self.update_attack_missile_position()

        reward, done = self.check_impact()

        self.global_time += 0.01

        return reward, done


# (0.2) Create the environment. -------------------------------------------------------
env = Environment()
env.set_episode(env.global_time)

print("\n")
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
print("Attack to target:", env.attack_missile_to_target)

print("\n")
print("global_time:", env.global_time)
print("Attack Missile Coordinates:", env.attack_missile.coordinates)
env.step((True, 0, True))
print("\n")
print("global_time:", env.global_time)
print("Attack Missile Coordinates:", env.attack_missile.coordinates)
print("\nEnvironment init time:", env.global_time)
print("Attack Missile Coordinates:", env.attack_missile.coordinates)

for missile in env.defense_missiles:
    print("Defense Missile Corrdinates:", missile.coordinates)
    print("Defense Missile Theta:", missile.theta)
    print("Defense Missile Fired:", missile.fired)
    print("Defense Missile Fired Time:", missile.fired_time)
    print("Defense Missile Missile Clock:", missile.missile_clock)
    print("Defense Missile to Attack Missile:", missile.defense_missile_to_attack_missile)
    print("Defense Missile Start Distance:", missile.start_distance, "\n")
    
env.step((True, 0, True))
print("\nEnvironment init time:", env.global_time)
print("Attack Missile Coordinates:", env.attack_missile.coordinates)

for missile in env.defense_missiles:
    print("Defense Missile Corrdinates:", missile.coordinates)
    print("Defense Missile Theta:", missile.theta)
    print("Defense Missile Fired:", missile.fired)
    print("Defense Missile Fired Time:", missile.fired_time)
    print("Defense Missile Missile Clock:", missile.missile_clock)
    print("Defense Missile to Attack Missile:", missile.defense_missile_to_attack_missile)
    print("Defense Missile Start Distance:", missile.start_distance, "\n")

env.step((True, 0, True))
print("\nEnvironment init time:", env.global_time)
print("Attack Missile Coordinates:", env.attack_missile.coordinates)

for missile in env.defense_missiles:
    print("\nDefense Missile Corrdinates:", missile.coordinates)
    print("Defense Missile Theta:", missile.theta)
    print("Defense Missile Fired:", missile.fired)
    print("Defense Missile Fired Time:", missile.fired_time)
    print("Defense Missile Missile Clock:", missile.missile_clock)
    print("Defense Missile to Attack Missile:", missile.defense_missile_to_attack_missile)
    print("Defense Missile Start Distance:", missile.start_distance, "\n")


print("\n")
print("Environment init time:", env.global_time)
print("Attack Missile Coordinates:", env.attack_missile.coordinates)