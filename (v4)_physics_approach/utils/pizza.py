import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# --- 1. SETUP VECTORS ---
# Origin
O = np.array([0, 0, 0])

# Position Vector (r) - The "String" (Let's put it on X axis for clarity)
r = np.array([3.0, 0.0, 0.0])

# Velocity Vector (v) - Moving "Up and Forward"
# This has a mix of parallel and perpendicular movement
v = np.array([1.0, 2.0, 0.0]) 

# --- 2. CALCULATE THE CROSS PRODUCT (THE AREA) ---
cross_prod = np.cross(r, v)
area = np.linalg.norm(cross_prod)

# --- 3. VISUALIZATION ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Helper to draw vectors
def plot_vec(start, vec, color, label):
    ax.quiver(
        start[0], start[1], start[2],
        vec[0], vec[1], vec[2],
        color=color, label=label, 
        arrow_length_ratio=0.1, linewidth=2
    )

# A. Draw the Main Vectors
plot_vec(O, r, 'blue', 'r (Position/String)')
# Draw v starting from r (Actual motion)
plot_vec(r, v, 'red', 'v (Target Motion)')

# B. Draw "Ghost" v at origin to show the Math Definition
plot_vec(O, v, 'red', '', ) # No label, just geometry
ax.plot([v[0], r[0]+v[0]], [v[1], r[1]+v[1]], [v[2], r[2]+v[2]], 'k--', alpha=0.5)

# C. DRAW THE PARALLELOGRAM (THE CROSS PRODUCT AREA)
# Vertices: Origin -> r -> (r+v) -> v -> Origin
verts = [np.array([O, r, r+v, v])]
# Create the 3D polygon
poly = Poly3DCollection(verts, alpha=0.4, facecolor='cyan', edgecolor='k')
ax.add_collection3d(poly)

# D. Draw the Cross Product Vector (The "Axle")
# It sticks straight up, perpendicular to the parallelogram
# Its height is equal to the Area of the cyan parallelogram
plot_vec(O, cross_prod, 'purple', f'r x v (Cross Product)\nLength = Area = {area:.2f}')

# Formatting
ax.set_xlim([-1, 5])
ax.set_ylim([-1, 5])
ax.set_zlim([-1, 6])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title(f'Geometric Intuition: Cross Product = Parallelogram Area\nShaded Area = {area:.2f}')
ax.legend()

plt.show()