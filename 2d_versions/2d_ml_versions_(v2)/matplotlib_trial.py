import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

# Initialize the figure
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')

# Initialize the plot elements
point, = ax.plot([], [], 'bo')  # Point to represent agent
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)  # Text to display time

# Global clock
start_time = time.time()

# Function to initialize the plot
def init():
    point.set_data([], [])
    time_text.set_text('')
    return point, time_text

# Function to update the plot at each frame
def update(frame):
    # Get the current time in seconds and milliseconds
    current_time = time.time() - start_time
    seconds = int(current_time)
    milliseconds = int((current_time - seconds) * 1000)

    # Update the position of the point
    x = current_time * 1  # Example: x = 0.1 * time
    y = 0  # Example: y = sin(x) * 5
    point.set_data(x, y)

    # Update the time text
    time_text.set_text('Time: {:02d}:{:03d}'.format(seconds, milliseconds))

    return point, time_text

# Create the animation
ani = FuncAnimation(fig, update, frames=None, init_func=init, interval=10, blit=True)

# Show the animation
plt.show()
