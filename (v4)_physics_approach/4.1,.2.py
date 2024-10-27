import gymnasium as gym 
from gymnasium import Env
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import datetime
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env


# Set the global seed value
global_seed = 43

# Set seeds for reproducibility
np.random.seed(global_seed)
# random.seed(global_seed)

random_numbers = np.random.rand(5)
print(random_numbers)


class missile_interception_3d(gym.Env):
    def __init__(self):
        self.action_space = gym.spaces.MultiDiscrete([5, 5])
        self.observation_space = None
        self.np_random = np.random.RandomState(global_seed)
        random.seed(global_seed)  # For any usage of the random module

        # Target box dimensions
        self.targetbox_x_min = -15000
        self.targetbox_x_max = 15000
        self.targetbox_y_min = -15000
        self.targetbox_y_max = 15000

        self.time_step = 0.5
        self.g = 9.81

    # def seed(self, seed=None):
    #     self.seed_value = seed or np.random.randint(0, 10000)
    #     np.random.seed(self.seed_value)
    #     random.seed(self.seed_value)
    #     return [self.seed_value]

    def generate_enemy_missile(self):
        range_min = 70000 
        range_max = 1000000 

        # Generate the target coordinates using self.np_random
        self.attack_target_x = self.np_random.uniform(self.targetbox_x_min, self.targetbox_x_max)
        self.attack_target_y = self.np_random.uniform(self.targetbox_y_min, self.targetbox_y_max)

        # Choose a random phi and theta using self.np_random
        origin_phi = self.np_random.uniform(0, 2 * np.pi)
        theta = self.np_random.uniform(0.523599, 1.0472)

        # Calculate the upper and lower limits (initial velocity) 
        lower_limit = np.sqrt((range_min * self.g) / np.sin(2 * theta))
        upper_limit = np.sqrt((range_max * self.g) / np.sin(2 * theta))
        initial_velocity = self.np_random.uniform(lower_limit, upper_limit)
        range = initial_velocity * np.cos(theta) * (2 * initial_velocity * np.sin(theta) / self.g)

        # x and y launch positions 
        launch_x = self.attack_target_x + range * np.cos(origin_phi)
        launch_y = self.attack_target_y + range * np.sin(origin_phi)

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
        self.defense_launch_x = self.np_random.uniform(self.targetbox_x_min, self.targetbox_x_max)
        self.defense_launch_y = self.np_random.uniform(self.targetbox_y_min, self.targetbox_y_max)

        # Choose a random phi based on "origin phi"
        self.defense_azimuth = self.np_random.uniform((self.origin_phi - 0.785398), (self.origin_phi + 0.785398))

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
        # print("self.defense_v0z * self.time_step - 0.5 * self.g * self.time_step**2", self.defense_v0z * self.time_step - 0.5 * self.g * self.time_step**2)
        # print("self.defense_z", self.defense_z)
        # print("- 0.5 * self.g * self.time_step**2", - 0.5 * self.g * self.time_step**2)
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
            self.defense_theta += 0.0872665
        elif action[1] == 2:
            self.defense_theta -= 0.0872665
        elif action[1] == 3:
            self.defense_theta += 0.174532925
        elif action[1] == 4:
            self.defense_theta -= 0.174532925

        if self.defense_azimuth > 2 * np.pi:
            self.defense_azimuth -= 2 * np.pi

        elif self.defense_azimuth < 0:
            self.defense_azimuth += 2 * np.pi
        
        if self.defense_theta > np.pi:
            self.defense_theta -= np.pi
        elif self.defense_theta < 0:
            self.defense_theta += np.pi
        
    def move_enemy_missile(self):
        # print("\n--------------------------------------------------------------")
        # print("time:", self.t)

        # THIS HAS TO BE DEFINED OUT SIDE OF OUR FUNCTION, NOT TO BE CALLED AOVER AND OVER AGAIN 
        # enemy missile velocity components
        self.enemy_v0x = self.enemy_initial_velocity * np.cos(self.enemy_azimuth) * np.cos(self.enemy_theta)
        self.enemy_v0y = self.enemy_initial_velocity * np.sin(self.enemy_azimuth) * np.cos(self.enemy_theta)
        self.enemy_v0z = self.enemy_initial_velocity * np.sin(self.enemy_theta) 

        # PRINT VALUES BEFORE
        # print("--------------------------------------------------------------")
        # print("enemy_v0x:", self.enemy_v0x)
        # print("enemy_v0y:", self.enemy_v0y)
        # print("enemy_v0z:", self.enemy_v0z)
        # print("enemy_x:", self.enemy_x) 
        # print("enemy_y:", self.enemy_y)
        # print("enemy_z:", self.enemy_z)
        # print("")

        # position array
        self.enemy_x = self.enemy_v0x * self.t + self.enemy_launch_x
        self.enemy_y = self.enemy_v0y * self.t + self.enemy_launch_y
        self.enemy_z = self.enemy_v0z * self.t - 0.5 * self.g * self.t**2

        if self.enemy_z < 0:
            print("ENEMY MISSILE HIT TARGET")
            self.done = True

    def calculate_distance_missiles(self):
        distance = np.sqrt((self.enemy_x - self.defense_x)**2 + (self.enemy_y - self.defense_y)**2 + (self.enemy_z - self.defense_z)**2)
        return distance
    
    def calculate_defense_azimuth_prime(self):
        self.defense_azimuth_prime = np.arctan((self.enemy_y - self.defense_y) / (self.enemy_x - self.defense_x))
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print("Checking: azimuth prime calculation ##########################")
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print("Enemy coordinates:", (self.enemy_x, self.enemy_y))
        # print("Defense coordinates:", (self.defense_x, self.defense_y))
        # print("Adjacent Point: ", (self.enemy_x, self.defense_y))
        # print("self.defense_azimuth_prime RAD", self.defense_azimuth_prime)
        # print("self.defense_azimuth_prime DEG", np.degrees(self.defense_azimuth_prime))
        self.defense_azimuth_prime = abs(self.defense_azimuth_prime)
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        if self.enemy_y > self.defense_y and self.enemy_x > self.defense_x:
            print("Enemy is in the first quadrant")
            self.defense_azimuth_prime = self.defense_azimuth_prime
         
        elif self.enemy_y > self.defense_y and self.enemy_x < self.defense_x:
            print("Enemy is in the second quadrant")
            self.defense_azimuth_prime = np.pi - self.defense_azimuth_prime

        elif self.enemy_y < self.defense_y and self.enemy_x < self.defense_x:
            print("Enemy is in the third quadrant")
            self.defense_azimuth_prime = np.pi + self.defense_azimuth_prime

        elif self.enemy_y < self.defense_y and self.enemy_x > self.defense_x:
            print("Enemy is in the fourth quadrant")
            self.defense_azimuth_prime = 2 * np.pi - self.defense_azimuth_prime

        # print("Final azimuth prime", self.defense_azimuth_prime)
        # print("Final azimuth deg", np.degrees(self.defense_azimuth_prime))

        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    def calculate_defense_theta_prime(self):
        self.defense_theta_prime = np.arctan((np.sqrt((self.enemy_x - self.defense_x)**2 + (self.enemy_y - self.defense_y)**2)) / (self.enemy_z - self.defense_z))
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Checking: theta prime calculation ##########################")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Length on xy plane:", np.sqrt((self.enemy_x - self.defense_x)**2 + (self.enemy_y - self.defense_y)**2))
        print("Height difference:", self.enemy_z - self.defense_z)
        print("Enemy coordinates:", (self.enemy_x, self.enemy_y, self.enemy_z))
        print("Defense coordinates:", (self.defense_x, self.defense_y, self.defense_z))
        print("Adjacent Point: ", (self.enemy_x, self.defense_y, self.enemy_z))
        print("self.defense_theta_prime RAD", self.defense_theta_prime)
        print("self.defense_theta_prime DEG", np.degrees(self.defense_theta_prime))
        print("self.defense_theta", self.defense_theta)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    def hard_coded_nav(self):
        # correct PHI
        # calculate the difference between azimuth and azimuth prime
        self.azimuth_diff = self.defense_azimuth_prime - self.defense_azimuth

        if self.azimuth_diff < 0:
            self.azimuth_diff = abs(self.azimuth_diff)
            self.defense_turn_right = True

        else:
            self.defense_turn_right = False

        if self.azimuth_diff > np.pi:
            self.azimuth_diff = 2 * np.pi - self.azimuth_diff
            self.defense_turn_right = not self.defense_turn_right

        if self.defense_turn_right:
            hard_turn = (abs(self.azimuth_diff - 0.523599))
            soft_turn = (abs(self.azimuth_diff - 0.174532925))

            if hard_turn and soft_turn > self.azimuth_diff:
                print("STILL")
                self.defense_turn_action = 0

            elif hard_turn < soft_turn:
                print("HARD TURN RIGHT")
                self.defense_turn_action = 4
            else:
                print("SOFT TURN RIGHT")
                self.defense_turn_action = 2

        else:
            hard_turn = (abs(self.azimuth_diff - 0.523599)) #SLOOOOOOOOOOOOOP? LOOK AT THE CONDITIONS ABOVE, PLUS IT'S A SUBTRACTION
            soft_turn = (abs(self.azimuth_diff - 0.174532925))

            if hard_turn and soft_turn > self.azimuth_diff:
                print("STILL")
                self.defense_turn_action = 0

            elif hard_turn < soft_turn:
                print("HARD TURN LEFT")
                self.defense_turn_action = 3
            else:
                print("SOFT TURN LEFT")
                self.defense_turn_action = 1

        # find the right theta turn
        print("\n-/-/-/-/-/-/-/-/-/-/")
        print("Defense theta prime:", self.defense_theta_prime)
        print("Defense theta:", self.defense_theta)

        self.theta_diff = self.defense_theta_prime - self.defense_theta
        print("self.theta_diff", self.theta_diff)

        if self.defense_theta_prime < self.defense_theta:
            print("Enemy is below defense missile")
            hard_pitch_down = abs((abs(self.theta_diff) - 0.523599))
            soft_pitch_down = abs((abs(self.theta_diff) - 0.174532925))

            if hard_pitch_down and soft_pitch_down > abs(self.theta_diff):
                print("STILL")
                self.defense_pitch_action = 0

            elif hard_pitch_down < soft_pitch_down:
                print("HARD PITCH DOWN")
                self.defense_pitch_action = 4
            
            else:
                print("SOFT PITCH DOWN")
                self.defense_pitch_action = 2

        else:
            print("Enemy is above defense missile")
            hard_pitch_up =  abs((abs(self.theta_diff) - 0.523599))
            soft_pitch_up = abs((abs(self.theta_diff) - 0.174532925))

            if hard_pitch_up and soft_pitch_up > self.theta_diff:
                print("STILL")
                self.defense_pitch_action = 0

            elif hard_pitch_up < soft_pitch_up:
                print("HARD PITCH UP")
                self.defense_pitch_action = 3
            else:
                print("SOFT PITCH UP")
                self.defense_pitch_action = 1

        print("-/-/-/-/-/-/-/-/-/-/\n")

    def reset(self):
        self.done = False 
        self.enemy_path = []
        self.defense_path = []
        self.t = 0
        self.enemy_theta, self.enemy_azimuth, self.enemy_initial_velocity, self.enemy_launch_x, self.enemy_launch_y, self.origin_phi = self.generate_enemy_missile()
        print("Attack Target:", (self.attack_target_x, self.attack_target_y))
        self.generate_defense_missile()
        self.enemy_x = self.enemy_launch_x
        self.enemy_y = self.enemy_launch_y
        self.enemy_z = 0

    def step(self, action):
        try:
            print("\n")
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("TIME IS ", self.t)
            print("###################################################################")
            print("Before step:")
            print("Defense azimuth", self.defense_azimuth)
            print("Defense azimuth prime:", self.defense_azimuth_prime)
            print("Defense Azimuth DEG:", np.degrees(self.defense_azimuth))
            print("Defense azimuth prime DEG:", np.degrees(self.defense_azimuth_prime))
            print("--------")
            print("Defense theta", self.defense_theta)
            print("Defense theta prime:", self.defense_theta_prime)
            print("Defense theta DEG:", np.degrees(self.defense_theta))
            print("Defense theta prime DEG:", np.degrees(self.defense_theta_prime))
            print("--------")
            print("Defense x, y and z", (self.defense_x, self.defense_y, self.defense_z))
            print("Enemy x, y and z", (self.enemy_x, self.enemy_y, self.enemy_z))
            print("###################################################################")
        except:
            print("Skill issue")

        # Move the enemy missile
        self.turn_angles_defense_missile(action)
        self.move_enemy_missile()
        self.move_defense_missile()
        self.enemy_path.append([self.enemy_x, self.enemy_y, self.enemy_z])
        self.defense_path.append([self.defense_x, self.defense_y, self.defense_z])
        self.calculate_defense_azimuth_prime()
        self.calculate_defense_theta_prime()
        self.hard_coded_nav()
        self.t += 1
        
        try:
            print("\n###################################################################")
            print("Before step:")
            print("Defense azimuth", self.defense_azimuth)
            print("Defense azimuth prime:", self.defense_azimuth_prime)
            print("Defense Azimuth DEG:", np.degrees(self.defense_azimuth))
            print("Defense azimuth prime DEG:", np.degrees(self.defense_azimuth_prime))
            print("--------")
            print("Defense theta", self.defense_theta)
            print("Defense theta prime:", self.defense_theta_prime)
            print("Defense theta DEG:", np.degrees(self.defense_theta))
            print("Defense theta prime DEG:", np.degrees(self.defense_theta_prime))
            print("--------")
            print("Defense x, y and z", (self.defense_x, self.defense_y, self.defense_z))
            print("Enemy x, y and z", (self.enemy_x, self.enemy_y, self.enemy_z))
            print("###################################################################")
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("\n")
            print("\n")
        except:
            print("Skill issue")

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

        # Plot the starting points
        ax.scatter(xe[0], ye[0], ze[0], color='blue', s=50, label="Enemy Start")  # Enemy start point
        ax.scatter(xd[0], yd[0], zd[0], color='red', s=50, label="Defense Start")  # Defense start point

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
# print("Enemy missile parameters: ")
# print("Enemy theta: ", env.enemy_theta)
# print("Enemy azimuth: ", env.enemy_azimuth)
# print("Enemy initial velocity: ", env.enemy_initial_velocity)
# print("Enemy launch x: ", env.enemy_launch_x)
# print("Enemy launch y: ", env.enemy_launch_y)
# print("Time: ", env.t)
# print("Done", env.done)

while env.done is False:
    carlos = [0, 0]
    try:
        # If defense_turn_action exists, assign it to carlos[0]
        carlos[0] = env.defense_turn_action
        carlos[1] = env.defense_pitch_action
    except AttributeError:
        print("AttributeError: 'defense_turn_action' not found in 'env', setting carlos[0] to default")
        carlos[0] = 0  # Or some default action when the attribute is not available

    # print("Action: ", carlos)
    env.step(carlos)
    # print("Time after step: ", env.t)
    # print("Enemy x", env.enemy_x)
    # print("Enemy y", env.enemy_y)
    # print("Enemy z", env.enemy_z)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # print("Defense x", env.defense_x)
    # print("Defense y", env.defense_y)
    # print("Defense z", env.defense_z)
    # print("Defense azimuth", env.defense_azimuth)
    # print("Defense azimuth deg", np.degrees(env.defense_azimuth))   

# print("####################################################")
# print("Final position")
# print("enemy_x", env.enemy_x)
# print("enemy_y", env.enemy_y)
# print("enemy_z", env.enemy_z)
# print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------")
# print("-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/\n")

env.render()     
