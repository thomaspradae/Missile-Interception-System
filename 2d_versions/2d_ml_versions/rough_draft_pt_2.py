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
        self.initial_position = np.array([self.coordinates[0], self.coordinates[1]])
        return self.fired, self.fired_time
    
    def create_defense_missile(self, defense, global_time, theta):
        self.speed = 1
        self.theta = theta
        self.coordinates = defense.coordinates
        self.fired = False
        self.fired_time = 0 
        self.missile_clock = global_time - self.fired_time
        self.defense_missile_to_attack_missile = None
        self.start_distance = None
        self.reward_diff = None

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
        self.reward = 0
        self.target = Point('target')
        self.defense = Point('defense')
        self.attack = Point('attack')

        self.target.create_target()
        self.defense.create_defense(self.target)
        self.attack.create_attack(self.target)

        self.attack_missile = Missile('attack')
        self.attack_missile.create_attack_missile(self.attack)
        self.attack_missile.fire_attack_missile(global_time)
        self.attack_missile_to_target = self.distance_attack_to_target(self.attack_missile)

        self.defense_missiles = []

    def calculate_distance(self, point1, point2):
        return math.hypot(point1[0] - point2[0], point1[1] - point2[1])
    
    def distance_attack_to_target(self, attack_missile):
        # print("//////////////////////////////////////////")
        # print("Attack Missile PRINTING:", attack_missile)
        # print("Attack Missile Coordinates:", attack_missile.coordinates)
        # print("Static Attack Coordinates:", self.attack.coordinates)
        # print("self.target.coordinates:", self.target.coordinates)
        # print("self.attack.coordinates:", attack_missile.coordinates)
        # print("self.calculate_distance(attack_missile.coordinates, self.target.coordinates):", self.calculate_distance(attack_missile.coordinates, self.target.coordinates))
        # print("Global Time:", self.global_time)
        # print("------------------------------------------")
        self.attack_missile_to_target = (self.calculate_distance(attack_missile.coordinates, self.target.coordinates) - (attack_missile.radius + self.target.radius))
        # print("Attack Missile PRINTING:", attack_missile)
        # print("Attack Missile Coordinates:", attack_missile.coordinates)
        # print("Static Attack Coordinates:", self.attack.coordinates)
        # print("self.target.coordinates:", self.target.coordinates)
        # print("self.attack.coordinates:", attack_missile.coordinates)
        # print("self.calculate_distance(attack_missile.coordinates, self.target.coordinates):", self.calculate_distance(attack_missile.coordinates, self.target.coordinates))
        # print("Global Time:", self.global_time)
        return self.attack_missile_to_target
    
    def indv_distance_defense_to_attack(self, missile, attack_missile):
        missile.defense_missile_to_attack_missile = (self.calculate_distance(missile.coordinates, attack_missile.coordinates) - (missile.radius + attack_missile.radius))
        return missile.defense_missile_to_attack_missile

    def distance_defense_to_attack(self, attack_missile):
        for missile in self.defense_missiles:
            # print("\n############################################")
            # print("Defense Coordinates:", missile.coordinates)
            # print("Attack Coordinates:", attack_missile.coordinates)
            missile.defense_missile_to_attack_missile = (self.calculate_distance(missile.coordinates, attack_missile.coordinates) - (missile.radius + attack_missile.radius))
            # print("Defense Missile to Attack Missile:", missile.defense_missile_to_attack_missile)
            # print("self.calculate_distance(missile.coordinates, attack_missile.coordinates):", self.calculate_distance(missile.coordinates, attack_missile.coordinates))
            # print("Defense Coordinates:", missile.coordinates)
            # print("Attack Coordinates:", attack_missile.coordinates)
            # print("############################################\n")

    def local_create_defense_missile(self, defense, global_time, defense_missiles, theta):
        defense_missile = Missile('defense')
        defense_missile.create_defense_missile(defense, global_time, theta)
        defense_missiles.append(defense_missile)
        return defense_missile 

    def update_attack_missile_position(self, attack_missile):
        new_coordx = self.attack.coordinates[0] + self.attack_missile.speed * self.global_time * math.cos(self.attack_missile.theta)
        new_coordy = self.attack.coordinates[1] + self.attack_missile.speed * self.global_time * math.sin(self.attack_missile.theta)
        print("\n++++++++++++++++++++++++++++++++++++++++")
        print("Attack Missile PRINTING:", attack_missile)
        print("Attack Missile Coordinates:", attack_missile.coordinates)
        print("Attack Missile Theta:", attack_missile.theta)
        print("Attack Missile Speed:", attack_missile.speed)
        print("Attack Missile Fired Time:", attack_missile.fired_time)
        print("Attack Missile to Target:", self.attack_missile_to_target)
        print("--")
        print("Original Attack Stationary Coordinates:", self.attack.coordinates)
        print("Global Time:", self.global_time)
        print("Distance to target:", self.attack_missile_to_target)
        print("New coord baby:", new_coordx, new_coordy)
        print("Missile x:", new_coordx)
        print("Missile y:", new_coordy)
        print("Missile coords old:", self.attack_missile.coordinates)
        print("----------------------------------------")
        attack_missile.coordinates = np.array([new_coordx, new_coordy])
        self.attack_missile.coordinates = np.array([new_coordx, new_coordy])
        print("Original Attack Stationary Coordinates:", self.attack.coordinates)
        print("Chaning Coords", attack_missile.coordinates)
        print("Global Time:", self.global_time)
        print("Missile coords new:", self.attack_missile.coordinates)
        print("Missile coords x", self.attack_missile.coordinates[0])
        print("Missile coords y", self.attack_missile.coordinates[1])
        print("Distance to target:", self.attack_missile_to_target)
        print("++++++++++++++++++++++++++++++++++++++++\n")
        # self.attack_missile.coordinates[0] = self.attack.coordinates[0] + self.attack_missile.speed * self.global_time * math.cos(self.attack_missile.theta)
        # self.attack_missile.coordinates[1] = self.attack.coordinates[1] + self.attack_missile.speed * self.global_time * math.sin(self.attack_missile.theta)
    
    def update_defense_missile_positions(self):
        for missile in self.defense_missiles:
            new_coordx = missile.initial_position[0] + missile.speed * (self.global_time - missile.fired_time) * math.cos(missile.theta)
            new_coordy = missile.initial_position[1] + missile.speed * (self.global_time - missile.fired_time) * math.sin(missile.theta)
            print("New coord baby:", new_coordx, new_coordy)
            print("Missile x:", new_coordx)
            print("Missile y:", new_coordy)
            missile.coordinates = np.array([new_coordx, new_coordy])
            print("Missile coords new:", missile.coordinates)

    def distance_reward(self, reward):
        print("\n********************************")
        print("DEBUGGING DISTANE REWARD AS PART OF REWARD")
        print("Missiles: ", self.defense_missiles)
        for missile in self.defense_missiles:
            print("Missile Coordinates:", missile.coordinates)
            print("Missile.start_distance:", missile.start_distance)
            print("Missile.defense_missile_to_attack_missile:", missile.defense_missile_to_attack_missile)
            print("missile.start_distance - missile.defense_missile_to_attack_missile:", missile.start_distance - missile.defense_missile_to_attack_missile)
            missile.reward_diff = missile.start_distance - missile.defense_missile_to_attack_missile
            print("Missile.reward_diff:", missile.reward_diff)
            print("Reward:", reward)
            reward += missile.reward_diff
            print("Reward after missile.reward_diff:", reward)
        print("********************************\n")
            
        return reward

    def check_impact(self):
        for missile in self.defense_missiles:
            if missile.defense_missile_to_attack_missile < 0:
                return 100, True
        
        if env.attack_missile_to_target < 0:
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
        create_missile, fire_now = action
        create_missile_condition, theta = create_missile

        self.update_attack_missile_position(self.attack_missile)
        self.distance_attack_to_target(self.attack_missile)

        if create_missile_condition:
            self.local_create_defense_missile(self.defense, self.global_time, self.defense_missiles, theta)

        if fire_now:
            self.defense_missiles[-1].fire_defense_missile(self.global_time)
            self.defense_missiles[-1].start_distance = self.indv_distance_defense_to_attack(self.defense_missiles[-1], self.attack_missile)
            
        if len(self.defense_missiles) > 0:
            self.update_defense_missile_positions()
            self.distance_defense_to_attack(self.attack_missile)

        print("\n............................................")
        print("DEBUGGING REWARD")
        print("Global Time:", self.global_time)
        print("Reward before:", self.reward)
        print("distance_reward:", self.distance_reward(self.reward))
        print("--------------\n")
        distance_reward = self.distance_reward(self.reward)
        self.reward += distance_reward
        impact_reward, done = self.check_impact()
        self.reward += impact_reward
        print("Reward after:", self.reward)
        print("............................................\n")

        self.global_time += 0.1

        return self.reward, done
    
    def debugging_get_state(self, steps):
        print("\n--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/-")
        print("Environment created.")
        print("-------------------------------------------------------------------")
        print("ENVIRONMENT CONSTANTS")
        print("global_time:", self.global_time)
        print("Target coordinates:", self.target.coordinates)
        print("Defense coordinates:", self.defense.coordinates)
        print("Attack coordinates:", self.attack.coordinates)
        print("Reward:", self.reward)
        print("-------------------------------------------------------------------")
        print("ATTACK MISSILE")
        print("Attack Missile Fired:", self.attack_missile.fired)
        print("Attack Missile Coordinates:", self.attack_missile.coordinates)
        print("Attack Missile Theta:", self.attack_missile.theta)
        print("Attack Missile Speed:", self.attack_missile.speed)
        print("Attack Missile Fired Time:", self.attack_missile.fired_time)
        print("Attack Missile to Target:", self.attack_missile_to_target)
        print("-------------------------------------------------------------------")
        print("DEFENSE MISSILES")
        if len(self.defense_missiles) > 0:
            i = 0
            for missile in self.defense_missiles:
                print("Defense Missile", i)
        else:
            print("No defense missiles created.")

        step_num = 1
        for step in steps:
            print("\n--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/-")
            print("Step", step_num)
            print("BEFORE STEP: Environment recieved to make step")
            print("global_time:", self.global_time)
            print("Attack Missile Coordinates:", self.attack_missile.coordinates)
            print("Reward:", self.reward)
            print("-------------------------------------------------------------------")
            print("STEP")
            self.step(step)
            print(f"Step = Create a missile: {step[0][0]}, theta: {step[0][1]}, fire_now: {step[1]}")
            print("-------------------------------------------------------------------")
            print("AFTER STEP: Environment after step")
            print("global_time:", self.global_time)
            print("Attack Missile Coordinates:", self.attack_missile.coordinates)
            print("Reward:", self.reward)
            print("-------------------------------------------------------------------")
            print("DEFENSE MISSILES")
            print("Defense Missiles Count:", len(self.defense_missiles))
            print("Defense Missiles:", self.defense_missiles)

            i = 0
            for missile in self.defense_missiles:
                i += 1
                print("\n~~~~~~~~~~~~~~~~~")
                print("Defense Missile", i)
                print("Defense Missile Corrdinates:", missile.coordinates)
                print("Defense Missile Theta:", missile.theta)
                print("Defense Missile Fired:", missile.fired)
                print("Defense Missile Fired Time:", missile.fired_time)
                print("Defense Missile Missile Clock:", missile.missile_clock)
                print("Global Time:", self.global_time)
                print("Fired Time:", missile.fired_time)
                print("Global Time - Fired Time:", self.global_time - missile.fired_time)
                print("Defense Missile to Attack Missile:", missile.defense_missile_to_attack_missile)
                print("Defense Missile Start Distance:", missile.start_distance)
                print("Reward Difference:", missile.reward_diff)
                print("~~~~~~~~~~~~~~~~~\n")

            print("-------------------------------------------------------------------")
            print("IMPACT CHECK & SUMMARY")
            print("Attack Coordinates:", self.attack.coordinates)
            print("Target Coordinates:", self.target.coordinates)
            print("Defense Coordinates:", self.defense.coordinates)
            print("Attack Missile to Target:", self.attack_missile_to_target)
            print("Reward:", self.reward)
            print("Impact Check:", self.check_impact())
            print("--")
            print("Attack Missile Coordinates:", self.attack_missile.coordinates)
            print("Attack distance to target:", self.attack_missile_to_target)
            print("--")
            for missile in self.defense_missiles:
                print("Defense Missile Coordinates:", missile.coordinates)
                print("Defense Missile to Attack Missile:", missile.defense_missile_to_attack_missile)
                print("Reward Difference:", missile.reward_diff)
                print("--")

            print("--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/--/-\n")
            step_num += 1

# (0.2) Create the environment. -------------------------------------------------------
env = Environment()
env.set_episode(env.global_time)

# (0.3) Create the steps. --------------------------------------------------------------
steps = [((True, 1.867502), True), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False), ((False, None), False)]
# (0.4) Debugging the environment. -----------------------------------------------------
env.debugging_get_state(steps)

