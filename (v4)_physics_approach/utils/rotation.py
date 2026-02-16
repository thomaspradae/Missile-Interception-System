import matplotlib.pyplot as plt
import numpy as np

# --- 1. DEFINE THE PLAYERS ---
# Origin is (0,0,0)

# INTERCEPTOR (Blue)
# Position: At (1, 1, 0)
r_M = np.array([1.0, 1.0, 0.0])
# Velocity: Moving North (Y-axis) at speed 1
v_M = np.array([0.0, 1.0, 0.0])

# TARGET (Red)
# Position: At (3, 3, 2) - Up and away
r_T = np.array([3.0, 3.0, 2.0])
# Velocity: Moving East (X-axis) at speed 2
v_T = np.array([2.0, 0.0, 0.0])

# --- 2. CALCULATE RELATIVE VECTORS ---

# Relative Position (Line of Sight) - Green
# "The arrow from Interceptor to Target"
r = r_T - r_M

# Relative Velocity - Cyan
# "How the Target moves relative to the Interceptor"
v = v_T - v_M

# --- 3. CALCULATE OMEGA (ROTATION) ---

# Cross Product (The Torque/Axle)
cross_prod = np.cross(r, v)

# Dot Product (Distance Squared)
dot_prod = np.dot(r, r)

# Omega (The Rotation Vector) - Purple
omega = cross_prod / dot_prod

# --- 4. VISUALIZATION ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Helper to draw vectors
def plot_vec(start, vec, color, label, linestyle='-'):
    ax.quiver(
        start[0], start[1], start[2],
        vec[0], vec[1], vec[2],
        color=color, label=label, 
        arrow_length_ratio=0.1, linewidth=2, linestyle=linestyle
    )

# A. DRAW ABSOLUTE POSITIONS (From Origin)
origin = np.array([0, 0, 0])
plot_vec(origin, r_M, 'blue', 'r_M (Interceptor Pos)', ':')
plot_vec(origin, r_T, 'red', 'r_T (Target Pos)', ':')

# B. DRAW VELOCITIES (Attached to their objects)
# We scale them down slightly just so they fit on the plot better visually
scale = 1.0 
plot_vec(r_M, v_M * scale, 'darkblue', 'v_M (Interceptor Vel)')
plot_vec(r_T, v_T * scale, 'darkred', 'v_T (Target Vel)')

# C. DRAW RELATIVE VECTORS
# The Line of Sight (r)
plot_vec(r_M, r, 'green', 'r (Line of Sight)')

# The Relative Velocity (v)
# We draw this starting at the Target to show "where the target is going relative to the LOS"
plot_vec(r_T, v, 'cyan', 'v (Relative Velocity)')

# D. DRAW OMEGA (The Rotation Axis)
# We draw this at the Interceptor to show the axis the missile needs to rotate around
# We scale it up so you can see it easily
omega_scale = 5.0
plot_vec(r_M, omega * omega_scale, 'purple', f'Omega (Rotation Axis) x {omega_scale}')

# Setup Plot Limits
ax.set_xlim([0, 5])
ax.set_ylim([0, 5])
ax.set_zlim([0, 5])
ax.set_xlabel('X (East)')
ax.set_ylabel('Y (North)')
ax.set_zlabel('Z (Up)')
ax.set_title('Full 3D ProNav Geometry')
ax.legend()

plt.show()