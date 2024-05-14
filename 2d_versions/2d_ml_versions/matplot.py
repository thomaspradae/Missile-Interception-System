import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Create a grid from -10 to 10 in both axes
x_grid = range(-10, 11)
y_grid = range(-10, 11)

# Define the coordinates of the points
x = [1, 2, 3]
y = [1, 2, 3]

# Define the radii of the points
radii = [0.2, 0.2, 0.2]

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the grid
ax.plot(x_grid, [0]*len(x_grid), color='grey', linestyle='-', linewidth=0.5)
ax.plot([0]*len(y_grid), y_grid, color='grey', linestyle='-', linewidth=0.5)

# Plot each point as a circle with specified radius
for i in range(len(x)):
    circle = Circle((x[i], y[i]), radii[i], edgecolor='black', facecolor='None')
    ax.add_patch(circle)

# Add labels
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Show the plot
plt.grid(True)
plt.axis('equal')
plt.show()
