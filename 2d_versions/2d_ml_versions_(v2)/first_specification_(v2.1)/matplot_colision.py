import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

# Initialize the figure
fig, ax = plt.subplots()
ax.set_xlim(0, 5)
ax.set_ylim(-1, 4)
ax.set_aspect( 1 )

# Initialize the plot elements
point1, = ax.plot([], [], 'bo')  # Point to represent first agent
point2, = ax.plot([], [], 'ro')  # Point to represent second agent
collision_text = ax.text(0.05, 0.8, '', transform=ax.transAxes)  # Text to indicate collision

# Global clock
start_time = time.time()

# Function to initialize the plot
def init():
    point1.set_data([], [])
    point2.set_data([], [])
    collision_text.set_text('')
    return point1, point2, collision_text

# Initialize the plot elements
point1, = ax.plot([], [], 'bo')  # Point to represent first agent
point2, = ax.plot([], [], 'ro')  # Point to represent second agent

# Get the marker size of point1
marker_size_point1 = point1.get_markersize()

# Get the marker size of point2
marker_size_point2 = point2.get_markersize()

print("Marker size of point1:", marker_size_point1)
print("Marker size of point2:", marker_size_point2)

# Function to update the plot at each frame
def update(frame):
    # Get the current time in seconds and milliseconds
    current_time = time.time() - start_time
    seconds = int(current_time)
    milliseconds = int((current_time - seconds) * 1000)

    # Update the positions of the points
    x1 = current_time * 0.1  # Example: x = 0.1 * time for the first point
    y1 = 0  # Example: y = sin(x) * 5 for the first point
    point1.set_data(x1, y1)

    x2 = 5 - current_time * 0.1  # Example: x = 10 - 0.1 * time for the second point (opposite direction)
    y2 = 0  # Example: y = sin(x) * 5 for the second point
    point2.set_data(x2, y2)

    # Check for collision
    collision = check_collision(x1, y1, x2, y2, marker_size=0.1)  # Adjust marker size as needed
    if collision:
        collision_text.set_text('Collision Detected!')
    else:
        collision_text.set_text('')

    return point1, point2, collision_text

# Function to check for collision between two points
def check_collision(x1, y1, x2, y2, marker_size):
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance <= marker_size * 2  # Assuming marker size is the diameter

# Create the animation
ani = FuncAnimation(fig, update, frames=None, init_func=init, interval=10, blit=True)

# Show the animation
plt.show()
