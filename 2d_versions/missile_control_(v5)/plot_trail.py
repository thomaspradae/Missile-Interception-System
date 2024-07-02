import numpy as np
import matplotlib.pyplot as plt

# Initial position
initial_position = np.array([0.09415721, -0.47996359])

# Number of positions to simulate
num_positions = 50

# Simulating slight random movements from the initial position
np.random.seed(40)  # For reproducibility
defense_positions = [initial_position]
for _ in range(1, num_positions):
    new_position = defense_positions[-1] + np.random.normal(0, 0.01, 2)  # Small random changes
    defense_positions.append(new_position)

print(defense_positions)

# Function to plot the trail
def plot_defense_trail(defense_positions):
    fig, ax = plt.subplots()
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)

    # Extracting x and y coordinates
    defense_xs, defense_ys = zip(*defense_positions)

    # Plotting the trail
    ax.plot(defense_xs, defense_ys, 'b-', label='Defense Trail')  # Blue line for defense trail
    ax.scatter(defense_xs[-1], defense_ys[-1], color='red', s=100, label='Current Position')  # Current position

    ax.set_aspect('equal')
    ax.legend()
    plt.show()

# Plot the simulated trail
plot_defense_trail(defense_positions)

