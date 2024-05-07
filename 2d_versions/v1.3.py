# -------------------------------------------------------------------------------
# This is the third version of the algorithm (2D Version (v.1.3)). In this case the attacker is only
# limited by his length to the target. Meaning, he isn't limited to being under the target (y value).
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
        y = random.uniform(-2.0, 2.0)
        self.coordinates = np.array([x, y])
        return self.coordinates
    
    def create_defense(self, target):
        x = random.uniform(target.coordinates[0] - 1.5, target.coordinates[0] + 1.5)
        y = random.uniform(target.coordinates[1] - 1.5, target.coordinates[1] + 1.5)
        self.coordinates = np.array([x, y])
        return self.coordinates
    
    def create_attack(self, target, defense):
        x_side_left = random.uniform(-9.5, target.coordinates[0] - 2)
        x_side_right = random.uniform(target.coordinates[0] + 2, 9.5)
        y_below = random.uniform(target.coordinates[1] - 2, -9.5)
        y_above = random.uniform(target.coordinates[1] + 2, 9.5)
        x_inclusive = random.uniform(-9.5, 9.5)
        y_inclusive = random.uniform(-9.5, 9.5)
        y_below_x_inclusive = np.array([x_inclusive, y_below])
        y_above_x_inclusive = np.array([x_inclusive, y_above])
        x_left_y_inclusive = np.array([x_side_left, y_inclusive])
        x_right_y_inclusive = np.array([x_side_right, y_inclusive])

        self.coordinates = random.choice([y_below_x_inclusive, y_above_x_inclusive, x_left_y_inclusive, x_right_y_inclusive])
        return self.coordinates