import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Time array (in seconds)
t = np.linspace(3, 7, 100)  # Starts at 3 seconds

# Assume linear horizontal distance for simplicity
x = 1100 * (t - 3)  # Adjusted to start from 3 seconds
y = 1100 * (t - 3)  # Adjusted to start from 3 seconds

# Simulate height with initial height at 3 seconds
initial_height = 510  # meters at 3 seconds
z = initial_height + 1000 * np.sin(np.pi * (t - 3) / 4)  # Adjusted to start from 3 seconds

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotting the trajectory
ax.plot(x, y, z, 'b')

# Adding labels
ax.set_xlabel('X Distance (meters)')
ax.set_ylabel('Y Distance (meters)')
ax.set_zlabel('Height (meters)')
ax.set_title('Fateh-110 Missile Trajectory Starting at 3 Seconds')

plt.show()
