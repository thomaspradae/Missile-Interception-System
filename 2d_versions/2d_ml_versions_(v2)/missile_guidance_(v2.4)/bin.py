import numpy as np
distance = 0.001

# generate 10 random numbers between 0 and pi
angles = np.random.uniform(0, np.pi, 10)

for angle in angles:
    reward = 1 / angle
    print(f"reward: {reward}, angle: {angle}")