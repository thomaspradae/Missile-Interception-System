import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters
g = 9.81  # Acceleration due to gravity (m/s^2)
v0 = 1000.0  # Initial velocity (m/s)
theta = 45.0 # (xy plane vs z) Launch angle (degrees)
phi = 45.0  # (x v y plane) Launch angle (degrees)
t_max = 10000  # Maximum time to simulate (s)
dt = 0.01  # Time step (s)

initial_x_position = -100000
initial_y_position = -100000  

# Convert angle to radians
theta_rad = np.radians(theta)
phi_rad = np.radians(phi)

# Initial velocity components
v0x = v0 * np.cos(theta_rad) * np.cos(phi_rad)
v0y = v0 * np.cos(theta_rad) * np.sin(phi_rad)
v0z = v0 * np.sin(theta_rad)

# Time array    
t = np.arange(0, t_max, dt)     

# Position arrays (Can adjust for initial values)
x = v0x * t + initial_x_position
y = v0y * t + initial_y_position
z = v0z * t - 0.5 * g * t**2  # z position

# Stop the simulation when the projectile hits the ground
index = np.where(z < 0)[0]
if index.size > 0:
    flight_time = t[index[0]]
    terminal_x_position = x[index[0]]
    terminal_y_position = y[index[0]]
    apogee = np.max(z)

    x_traveled = terminal_x_position - initial_x_position
    y_traveled = terminal_y_position - initial_y_position

    range = np.sqrt((x_traveled)**2 + (y_traveled)**2) 

    print(f"Total flight time {flight_time} s")
    print(f"Missile traveled {range} m")
    print(f"X traveled {x_traveled} m")
    print(f"Y traveled {y_traveled} m")
    print(f"Apogee at {apogee} m")
    print(f"Average velocity {range / flight_time} m/s")

    x = x[:index[0]]
    y = y[:index[0]]
    z = z[:index[0]]

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot trajectory
ax.plot(x, y, z, label="Projectile trajectory")

# Labels and legend
ax.set_xlabel("X position (m)")
ax.set_ylabel("Y position (m)")
ax.set_zlabel("Z position (m)")
ax.set_title("3D Projectile Trajectory")
ax.legend()

# Show plot
plt.show()
