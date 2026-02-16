import matplotlib.pyplot as plt
import numpy as np

# --- 1. SETUP THE VECTORS ---
# Let's define arbitrary points in 3D space
# M = Interceptor Position (x, y, z)
r_M = np.array([1, 2, 1]) 

# T = Target Position (x, y, z)
r_T = np.array([4, 5, 6])

# r = The Relative Vector (Line of Sight)
# The Math: Target - Interceptor
r_rel = r_T - r_M 

# --- 2. SETUP THE 3D PLOT ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Set the coordinate limits so everything fits nicely
ax.set_xlim([0, 6])
ax.set_ylim([0, 6])
ax.set_zlim([0, 7])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Visualizing Vector Subtraction: r = r_T - r_M')

# Origin point (0,0,0) for reference
origin = np.array([0, 0, 0])

# --- 3. DRAW THE VECTORS ---

# Function to help draw vectors (arrows) easily
def plot_vector(start, vector, color, label):
    # quiver(x, y, z, u, v, w) -> draws arrow from (x,y,z) with direction (u,v,w)
    ax.quiver(
        start[0], start[1], start[2], # Start point
        vector[0], vector[1], vector[2], # Direction components
        color=color, arrow_length_ratio=0.1, linewidth=2, label=label
    )

# Vector 1: Origin -> Interceptor (r_M)
# "Where is the Interceptor relative to the world origin?"
plot_vector(origin, r_M, 'blue', 'r_M (Interceptor Pos)')

# Vector 2: Origin -> Target (r_T)
# "Where is the Target relative to the world origin?"
plot_vector(origin, r_T, 'red', 'r_T (Target Pos)')

# Vector 3: Interceptor -> Target (r)
# "Where is the Target relative to the Interceptor?"
# NOTICE: We start this arrow at r_M, not at the origin!
plot_vector(r_M, r_rel, 'green', 'r (Line of Sight)')

# --- 4. FINISH UP ---
# Add a legend to explain the colors
ax.legend()

# Show the interactive plot
plt.show()