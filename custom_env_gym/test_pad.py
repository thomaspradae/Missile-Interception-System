# Define a function to calculate the reward based on attack_missile_to_target value
def calculate_reward(attack_missile_to_target):
    return -2 * (1 / attack_missile_to_target)

# Values for attack_missile_to_target from step2 to step20
values = [4.208957, 4.008957, 3.808957, 3.608957, 3.408957, 3.208957, 3.008957, 2.808957, 2.608957, 2.408957, 2.208957, 2.008957, 1.808957, 1.608957, 1.408957, 1.208957, 1.008957, 0.808957, 0.608957]

# Calculate and print the reward for each value
for value in values:
    reward = calculate_reward(value)
    print(f"attack_missile_to_target: {value}, reward: {reward}")
