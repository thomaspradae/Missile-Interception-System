# import numpy as np
# import matplotlib.pyplot as plt

# # Parameters
# m0 = 1000  # Initial mass (kg)
# mf = 500   # Final mass (kg)
# ve = 3000  # Effective exhaust velocity (m/s)
# V0 = 0     # Initial velocity (m/s)
# x0 = 0     # Initial position (m)
# burn_time = 100  # Burn time (s)
# dt = 0.1   # Time step (s)

# # Mass flow rate
# mdot = (m0 - mf) / burn_time

# # Time array
# t = np.arange(0, burn_time, dt)

# # Initialize arrays for velocity and position
# V = np.zeros_like(t)
# x = np.zeros_like(t)

# # Set initial values
# V[0] = V0
# x[0] = x0

# # Simulation loop
# for i in range(1, len(t)):
#     m = m0 - mdot * t[i]
#     if m < mf:
#         break  # Stop if fuel is exhausted
#     V[i] = V0 + ve * np.log(m0 / m)
#     x[i] = x[i-1] + V[i] * dt

# # Plotting position vs time
# plt.plot(t, x)
# plt.xlabel('Time (s)')
# plt.ylabel('Position (m)')
# plt.title('Missile Position vs Time')
# plt.grid(True)
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Parameters
m0 = 5000  # Initial mass (kg)
mf = 1500   # Final mass (kg)
ve = 3000  # Effective exhaust velocity (m/s)
V0 = 1000   # Initial speed (m/s)
theta = 45  # Launch angle (degrees)
g = 9.81   # Gravity (m/s^2)
burn_time = 100  # Burn time (s)
dt = 0.1   # Time step (s)

# Initial velocity components
V0x = V0 * np.cos(np.radians(theta))
V0y = V0 * np.sin(np.radians(theta))

# Mass flow rate
mdot = (m0 - mf) / burn_time

# Time array
t = np.arange(0, burn_time, dt)

# Initialize arrays for velocity and position
Vx = np.zeros_like(t)
Vy = np.zeros_like(t)
x = np.zeros_like(t)
y = np.zeros_like(t)

# Set initial values
Vx[0] = V0x
Vy[0] = V0y
x[0] = 0
y[0] = 0

# Simulation loop
for i in range(1, len(t)):
    m = m0 - mdot * t[i]
    if m < mf:
        break  # Stop if fuel is exhausted

    # Update velocities
    Vx[i] = V0x  # Horizontal velocity remains constant (no air resistance)
    Vy[i] = V0y - g * t[i]  # Vertical velocity changes due to gravity

    print(Vx[i], Vy[i])

    # Update positions
    x[i] = x[i-1] + Vx[i] * dt
    y[i] = y[i-1] + Vy[i] * dt

    if y[i] < 0:
        break  # Stop if the missile hits the ground

# Plotting (x, y) trajectory
plt.plot(x, y)
plt.xlabel('Horizontal Distance (m)')
plt.ylabel('Altitude (m)')
plt.title('Missile Trajectory (x vs y)')
plt.grid(True)
plt.show()
