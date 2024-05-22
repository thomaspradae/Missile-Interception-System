import numpy as np
global_time = 0
reward = 0
target_coordinates = [0, 0]
defense_coordinates = [0, 0]
attack_coordinates = [0, 0]
attack_missile_coordinates = [0, 0]
attack_missile_theta = 0
attack_missile_to_target = 0

armed_missiles = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
fired_missiles = []


base_state = np.array(
            [
                global_time,
                reward,
                target_coordinates[0],
                target_coordinates[1],
                defense_coordinates[0],
                defense_coordinates[1],
                attack_coordinates[0],
                attack_coordinates[1],
                attack_missile_coordinates[0],
                attack_missile_coordinates[1],
                attack_missile_theta,
                attack_missile_to_target,
            ]
        )

# for missile in armed_missiles:
#     print("Hello")


# for i, missile in enumerate(armed_missiles):
#     missile_state = np.array(

#     )
# m

print(True)