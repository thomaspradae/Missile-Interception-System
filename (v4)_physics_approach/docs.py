import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

def generate_enemy_missiles(num_simulations):
    # Define the area of interest, a square area of 30km by 30km, centered at the origin
    max_x = 15000  # meters
    min_x = -15000  # meters
    max_y = 15000  # meters
    min_y = -15000  # meters
    r_min = 70000
    r_max = 1000000
    g = 9.81

    # Store results in a list
    results = []

    for _ in range(num_simulations):
        # Choose a random point within this area. This will be the target location.
        target_x = np.random.uniform(min_x, max_x)
        target_y = np.random.uniform(min_y, max_y)

        # Choose a random launch angle between 0 and 2pi radians
        origin_phi = np.random.uniform(0, 2 * np.pi)

        # Choose a random z_launch angle between 30 and 60 degrees
        theta = np.random.uniform(0.523599, 1.0472)

        # Calculate the upper and lower limits (initial velocity) 
        lower_limit = np.sqrt((r_min * g) / np.sin(2 * theta))
        upper_limit = np.sqrt((r_max * g) / np.sin(2 * theta))
        initial_velocity = np.random.uniform(lower_limit, upper_limit)

        # Calculate the launch distances
        r_selected_length = initial_velocity * np.cos(theta) * (2 * initial_velocity * np.sin(theta) / g)
        print("Selected length: ", r_selected_length)

        # Calculate the x and y positions of the launch
        selected_x = target_x + r_selected_length * np.cos(origin_phi)
        selected_y = target_y + r_selected_length * np.sin(origin_phi)

        # Calculate the distance between the target and the launch location
        selected_distance = np.sqrt((selected_x - target_x)**2 + (selected_y - target_y)**2)
        print("Selected distance: ", selected_distance)

        # Determine the launch angle based on the quadrant
        if origin_phi <= (np.pi/2) and origin_phi >= 0:
            extra_angle = np.pi - (np.pi/2) - origin_phi
            launch_angle = (3 * np.pi / 2) - extra_angle

        elif origin_phi <= np.pi and origin_phi > (np.pi/2):
            extra_angle = origin_phi - (np.pi/2)
            launch_angle = (3 * np.pi / 2) + extra_angle

        elif origin_phi <= (3 * np.pi / 2) and origin_phi > np.pi:
            extra_angle = 3 * np.pi / 2 - origin_phi
            launch_angle = (np.pi - (np.pi / 2) - extra_angle)

        elif origin_phi <= (2 * np.pi) and origin_phi > (3 * np.pi / 2):
            extra_angle = 2 * np.pi - origin_phi
            extra_angle_2 =  np.pi - (np.pi / 2) - extra_angle
            launch_angle = (np.pi / 2) + extra_angle_2

        # Store the result of this simulation
        results.append({
            "target_x": target_x,
            "target_y": target_y,
            "launch_x": selected_x,
            "launch_y": selected_y,
            "initial_velocity": initial_velocity,
            "launch_distance": selected_distance,
            "theta": theta,
            "launch_angle": launch_angle
        })

    # Convert the results list to a DataFrame
    df_results = pd.DataFrame(results)

    # Optionally, you can plot the last simulation
    fig, ax = plt.subplots()
    plt.xlim(-1000000, 1000000)
    plt.ylim(-1000000, 1000000)

    # Draw the square in the middle
    square = patches.Rectangle((min_x, min_y), max_x - min_x, max_y - min_y,
                                linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(square)

    # Mark the target location
    ax.plot(df_results.iloc[-1]['target_x'], df_results.iloc[-1]['target_y'], 'bo')  # 'bo' means blue color, circle marker
    ax.plot(df_results.iloc[-1]['launch_x'], df_results.iloc[-1]['launch_y'], 'yo')  # 'yo' means yellow color, circle marker

    # Draw x and y axes
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)

    plt.show()

    return df_results

# Run the simulation for 10 iterations and get the results
results_df = generate_enemy_missiles(20)
print(results_df)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_trajectories(df):
    # Parameters
    g = 9.81  # Acceleration due to gravity (m/s^2)
    t_max = 10000  # Maximum time to simulate (s)
    dt = 0.01  # Time step (s)

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for index, row in df.iterrows():
        # Extract values from the DataFrame
        v0 = row['initial_velocity']
        theta = np.degrees(row['theta'])  # theta in degrees
        phi = np.degrees(row['launch_angle'])  # phi in degrees
        initial_x_position = row['launch_x']
        initial_y_position = row['launch_y']

        # Convert angles to radians
        theta_rad = np.radians(theta)
        phi_rad = np.radians(phi)

        # Initial velocity components
        v0x = v0 * np.cos(theta_rad) * np.cos(phi_rad) 
        v0y = v0 * np.cos(theta_rad) * np.sin(phi_rad)
        v0z = v0 * np.sin(theta_rad)

        # Time array
        t = np.arange(0, t_max, dt)

        # Position arrays
        x = v0x * t + initial_x_position
        y = v0y * t + initial_y_position
        z = v0z * t - 0.5 * g * t**2  # z position

        # Stop the simulation when the projectile hits the ground
        ground_index = np.where(z < 0)[0]
        if ground_index.size > 0:
            flight_time = t[ground_index[0]]
            terminal_x_position = x[ground_index[0]]
            terminal_y_position = y[ground_index[0]]
            apogee = np.max(z)

            x_traveled = terminal_x_position - initial_x_position
            y_traveled = terminal_y_position - initial_y_position

            range_covered = np.sqrt((x_traveled)**2 + (y_traveled)**2)

            print(f"Trajectory {index + 1}:")
            print(f"Total flight time {flight_time} s")
            print(f"Missile traveled {range_covered} m")
            print(f"X traveled {x_traveled} m")
            print(f"Y traveled {y_traveled} m")
            print(f"Apogee at {apogee} m")
            print(f"Average velocity {range_covered / flight_time} m/s\n")

            # Truncate the arrays to the point of impact
            x = x[:ground_index[0]]
            y = y[:ground_index[0]]
            z = z[:ground_index[0]]

        # Plot the trajectory
        ax.plot(x, y, z, label=f"Trajectory {index + 1}")

    # Labels and legend
    ax.set_xlabel("X position (m)")
    ax.set_ylabel("Y position (m)")
    ax.set_zlabel("Z position (m)")
    ax.set_title("3D Projectile Trajectories")
    # ax.legend()

    # Show plot
    plt.show()

# Assuming df_results is the DataFrame obtained from the previous function
plot_trajectories(results_df)

