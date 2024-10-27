import gymnasium as gym 
from gymnasium import Env
import numpy as np
import matplotlib.pyplot as plt
import random
import math
# import tensorflow as tf
import datetime
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env

# # Set the global seed value
# global_seed = 43

# # Set seeds for reproducibility
# np.random.seed(global_seed)
# random.seed(global_seed)
# tf.random.set_seed(global_seed)0.523599

class missile_interception_3d(Env):
    def __init__(self):
        self.action_space = gym.spaces.MultiDiscrete([5, 5])
        self.observation_space = None
        # self.seed(global_seed)  # Initialize the environment with the global seed

        # Target box dimensions
        self.targetbox_x_min = -15000
        self.targetbox_x_max = 15000
        self.targetbox_y_min = -15000
        self.targetbox_y_max = 15000

        self.time_step = 0.5

    def seed(self, seed=None):
        self.seed_value = seed
        np.random.seed(self.seed_value)
        random.seed(self.seed_value)
        # If you have any other random generators, set their seed here too
        return [self.seed_value]

    def generate_enemy_missile(self):
        range_min = 70000 # Minimum range 
        range_max = 1000000 # Maximum range
        self.g = 9.81

        # Generate the target coordinates
        target_x = np.random.uniform(self.targetbox_x_min, self.targetbox_x_max)
        target_y = np.random.uniform(self.targetbox_y_min, self.targetbox_y_max)

        # Choose a random phi and theta
        origin_phi = np.random.uniform(0, 2 * np.pi)
        theta = np.random.uniform(0.523599, 1.0472) # Between 30 and 75 degrees

        # Calculate the upper and lower limits (initial velocity) 
        lower_limit = np.sqrt((range_min * self.g) / np.sin(2 * theta))
        upper_limit = np.sqrt((range_max * self.g) / np.sin(2 * theta))
        initial_velocity = np.random.uniform(lower_limit, upper_limit)
        range = initial_velocity * np.cos(theta) * (2 * initial_velocity * np.sin(theta) / self.g)

        # x and y launch positions 
        launch_x = target_x + range * np.cos(origin_phi)
        launch_y = target_y + range * np.sin(origin_phi)

        # Determine the launch angle based on the quadrant
        if origin_phi <= (np.pi/2) and origin_phi >= 0:
            extra_angle = np.pi - (np.pi/2) - origin_phi
            launch_angle = (3 * np.pi / 2) - extra_angle

        elif origin_phi <= np.pi and origin_phi > (np.pi/2):
            extra_angle = origin_phi - (np.pi/2)
            launch_angle = (3 * np.pi / 2) + extra_angle

        elif origin_phi <= (3 * np.pi / 2) and origin_phi > np.pi:
            extra_angle = 3 * np.pi / 2 - origin_phi
            launch_angle = (np.pi - (np.pi / 2) - extra_angle)

        elif origin_phi <= (2 * np.pi) and origin_phi > (3 * np.pi / 2):
            extra_angle = 2 * np.pi - origin_phi
            extra_angle_2 =  np.pi - (np.pi / 2) - extra_angle
            launch_angle = (np.pi / 2) + extra_angle_2

        return theta, launch_angle, initial_velocity, launch_x, launch_y, origin_phi 

    def generate_defense_missile(self):
        self.defense_launch_x = np.random.uniform(self.targetbox_x_min, self.targetbox_x_max)
        self.defense_launch_y = np.random.uniform(self.targetbox_y_min, self.targetbox_y_max)

        # Choose a random phi based on "origin phi"
        self.defense_azimuth = np.random.uniform((self.origin_phi - 0.785398), (self.origin_phi + 0.785398)) 

        # Choose a random initial theta
        self.defense_theta = 0.785398

        # Initial velocity
        self.defense_initial_velocity = 3000

        # Initial position
        self.defense_x = self.defense_launch_x
        self.defense_y = self.defense_launch_y
        self.defense_z = 0

    def move_defense_missile(self):
        self.defense_v0x = self.defense_initial_velocity * np.cos(self.defense_azimuth) * np.cos(self.defense_theta)
        self.defense_v0y = self.defense_initial_velocity * np.sin(self.defense_azimuth) * np.cos(self.defense_theta)
        self.defense_v0z = self.defense_initial_velocity * np.sin(self.defense_theta)   

        self.defense_x += self.defense_v0x * self.time_step 
        self.defense_y += self.defense_v0y * self.time_step
        print("-----------------------------------")
        print("self.defense_v0z * self.time_step - 0.5 * self.g * self.time_step**2", self.defense_v0z * self.time_step - 0.5 * self.g * self.time_step**2)
        print("self.defense_z", self.defense_z)
        print("- 0.5 * self.g * self.time_step**2", - 0.5 * self.g * self.time_step**2)
        self.defense_z = self.defense_v0z * self.t - 0.5 * self.g * self.t**2

        if self.defense_z < 0:
            print("DEFENSE MISSILE HIT GROUND")
            self.done = True

    def turn_angles_defense_missile(self, action):

        # Turn the azimuth
        if action[0] == 0:
            self.defense_azimuth += 0
        elif action[0] == 1:
            self.defense_azimuth += 0.174532925
        elif action[0] == 2:
            self.defense_azimuth -= 0.174532925
        elif action[0] == 3:
            self.defense_azimuth += 0.523599
        elif action[0] == 4:
            self.defense_azimuth -= 0.523599
        
        # Turn the theta
        if action[1] == 0:
            self.defense_theta += 0
        elif action[1] == 1:
            self.defense_theta += 0.174532925
        elif action[1] == 2:
            self.defense_theta -= 0.174532925
        elif action[1] == 3:
            self.defense_theta += 0.523599
        elif action[1] == 4:
            self.defense_theta -= 0.523599

        if self.defense_azimuth > 2 * np.pi:
            self.defense_azimuth -= 2 * np.pi

        elif self.defense_azimuth < 0:
            self.defense_azimuth += 2 * np.pi
        
        if self.defense_theta > np.pi:
            self.defense_theta -= np.pi
        elif self.defense_theta < 0:
            self.defense_theta += np.pi
        
    def move_enemy_missile(self):

        print("--------------------------------------------------------------")
        print("time:", self.t)

        # THIS HAS TO BE DEFINED OUT SIDE OF OUR FUNCTION, NOT TO BE CALLED AOVER AND OVER AGAIN 
        # enemy missile velocity components
        self.enemy_v0x = self.enemy_initial_velocity * np.cos(self.enemy_azimuth) * np.cos(self.enemy_theta)
        self.enemy_v0y = self.enemy_initial_velocity * np.sin(self.enemy_azimuth) * np.cos(self.enemy_theta)
        self.enemy_v0z = self.enemy_initial_velocity * np.sin(self.enemy_theta) 

        # PRINT VALUES BEFORE
        print("--------------------------------------------------------------")
        print("enemy_v0x:", self.enemy_v0x)
        print("enemy_v0y:", self.enemy_v0y)
        print("enemy_v0z:", self.enemy_v0z)
        print("enemy_x:", self.enemy_x) 
        print("enemy_y:", self.enemy_y)
        print("enemy_z:", self.enemy_z)
        print("")

        # position array
        self.enemy_x = self.enemy_v0x * self.t + self.enemy_launch_x
        self.enemy_y = self.enemy_v0y * self.t + self.enemy_launch_y
        self.enemy_z = self.enemy_v0z * self.t - 0.5 * self.g * self.t**2

        if self.enemy_z < 0:
            self.done = True

    def calculate_distance_missiles(self):
        distance = np.sqrt((self.enemy_x - self.defense_x)**2 + (self.enemy_y - self.defense_y)**2 + (self.enemy_z - self.defense_z)**2)
        return distance

    def reset(self):
        self.done = False 
        self.enemy_path = []
        self.defense_path = []
        self.t = 0
        self.enemy_theta, self.enemy_azimuth, self.enemy_initial_velocity, self.enemy_launch_x, self.enemy_launch_y, self.origin_phi = self.generate_enemy_missile()
        self.generate_defense_missile()
        self.enemy_x = self.enemy_launch_x
        self.enemy_y = self.enemy_launch_y
        self.enemy_z = 0

    def step(self, action):
        # Move the enemy missile
        self.turn_angles_defense_missile(action)
        self.move_enemy_missile()
        self.move_defense_missile()
        self.enemy_path.append([self.enemy_x, self.enemy_y, self.enemy_z])
        self.defense_path.append([self.defense_x, self.defense_y, self.defense_z])
        self.t += 0.5

    def render(self):
        enemy_path_array = np.array(self.enemy_path)
        defense_path_array = np.array(self.defense_path)

        # Extract the x, y, z coordinates
        xe = enemy_path_array[:, 0]
        ye = enemy_path_array[:, 1]
        ze = enemy_path_array[:, 2]

        xd = defense_path_array[:, 0]
        yd = defense_path_array[:, 1]
        zd = defense_path_array[:, 2]

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the trajectory
        ax.plot(xe, ye, ze, label="Enemy missile trajectory")
        ax.plot(xd, yd, zd, label="Defense missile trajectory")

        # Add labels and title
        ax.set_xlabel('X coordinate (m)')
        ax.set_ylabel('Y coordinate (m)')
        ax.set_zlabel('Z coordinate (m)')
        ax.set_title('Missile Trajectory')
        ax.legend()

        # Show the plot
        plt.show()

env = missile_interception_3d()
env.reset()

# Check reset conditions
env.reset()
print("Enemy missile parameters: ")
print("Enemy theta: ", env.enemy_theta)
print("Enemy azimuth: ", env.enemy_azimuth)
print("Enemy initial velocity: ", env.enemy_initial_velocity)
print("Enemy launch x: ", env.enemy_launch_x)
print("Enemy launch y: ", env.enemy_launch_y)
print("Time: ", env.t)
print("Done", env.done)

while env.done is False:
    # carlos = [0, 0]
    carlos = env.action_space.sample()
    print("Action: ", carlos)
    env.step(carlos)
    print("Time after step: ", env.t)
    print("Enemy x", env.enemy_x)
    print("Enemy y", env.enemy_y)
    print("Enemy z", env.enemy_z)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Defense x", env.defense_x)
    print("Defense y", env.defense_y)
    print("Defense z", env.defense_z)

print("####################################################")
print("Final position")
print("enemy_x", env.enemy_x)
print("enemy_y", env.enemy_y)
print("enemy_z", env.enemy_z)

env.render()