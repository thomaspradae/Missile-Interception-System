import numpy as np

def get_state_array(global_time, reward, target_coords, defense_coords, attack_coords, attack_missile_info, fired_defense_missiles, armed_defense_missiles):

    print("Before the cut")
    print("Len bof fired_defense_missiles BEFORE:", len(fired_defense_missiles))
    print("Len of armed_defense_missiles BEFORIO:", len(armed_defense_missiles))

    if len(fired_defense_missiles) + len(armed_defense_missiles) > 15:
        if len(fired_defense_missiles) > 15:
            fired_defense_missiles = fired_defense_missiles[:15]
        if len(armed_defense_missiles) + len(fired_defense_missiles) > 15:
            armed_defense_missiles = armed_defense_missiles[:15 - len(fired_defense_missiles)]

    print("MADE THE CUT")
    print("Len bof fired_defense_missiles:", len(fired_defense_missiles))
    print("Len of armed_defense_missiles:", len(armed_defense_missiles))

    # Base state setup
    base_state = np.array([
        global_time,
        reward,
        target_coords[0],
        target_coords[1],
        defense_coords[0],
        defense_coords[1],
        attack_coords[0],
        attack_coords[1],
        attack_missile_info['coords'][0],
        attack_missile_info['coords'][1],
        attack_missile_info['theta'],
        attack_missile_info['to_target']
    ])

    # Process fired missiles
    for missile in fired_defense_missiles:
        fired_missile_state = np.array([
            1,  # Missile created
            int(missile['fired']),
            missile['coords'][0],
            missile['coords'][1],
            missile['theta'],
            missile['fired_time'],
            global_time - missile['fired_time'],
            missile['start_distance'],
            missile['to_attack_missile'],
            missile['reward_diff']
        ])
        base_state = np.concatenate((base_state, fired_missile_state))

    # Process armed missiles
    for missile in armed_defense_missiles:
        armed_missile_state = np.array([
            1,  # Missile created
            int(missile['fired']),
            missile['coords'][0],
            missile['coords'][1],
            missile['theta'],
            -9999,  # Placeholder for fired_time
            -9999,  # Placeholder for global_time - fired_time
            -9999,  # Placeholder for start_distance
            missile['to_attack_missile'],
            0       # Placeholder for reward_diff
        ])
        base_state = np.concatenate((base_state, armed_missile_state))

    # Padding for consistency
    max_missiles = 15
    num_missiles = len(fired_defense_missiles) + len(armed_defense_missiles)
    missiles_to_add = max_missiles - num_missiles
    if missiles_to_add > 0:
        print("Still valid")
        print("Current missikes:", num_missiles)
        empty_missile = np.array([0, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, 0])
        empty_missiles = np.tile(empty_missile, (missiles_to_add, 1)).flatten()
        print("Empty missiles MUDAFUGGIN:", empty_missiles)
        base_state = np.concatenate((base_state, empty_missiles))
    else:
        print("Warning: Number of missiles exceeds maximum limit")


    return base_state

# Example usage
global_time = 100
reward = 50
target_coords = [10, 20]
defense_coords = [30, 40]
attack_coords = [50, 60]
attack_missile_info = {'coords': [70, 80], 'theta': 90, 'to_target': 100}
fired_defense_missiles = [
    {'fired': True, 'coords': [5, 10], 'theta': 45, 'fired_time': 95, 'start_distance': 300, 'to_attack_missile': 50, 'reward_diff': 5},
    {'fired': True, 'coords': [15, 20], 'theta': 90, 'fired_time': 90, 'start_distance': 350, 'to_attack_missile': 60, 'reward_diff': 10},
    {'fired': True, 'coords': [25, 30], 'theta': 135, 'fired_time': 85, 'start_distance': 400, 'to_attack_missile': 70, 'reward_diff': 15},
    {'fired': True, 'coords': [35, 40], 'theta': 180, 'fired_time': 80, 'start_distance': 450, 'to_attack_missile': 80, 'reward_diff': 20},
    {'fired': True, 'coords': [45, 50], 'theta': 225, 'fired_time': 75, 'start_distance': 500, 'to_attack_missile': 90, 'reward_diff': 25},
    {'fired': True, 'coords': [55, 60], 'theta': 270, 'fired_time': 70, 'start_distance': 550, 'to_attack_missile': 100, 'reward_diff': 30},
    {'fired': True, 'coords': [65, 70], 'theta': 315, 'fired_time': 65, 'start_distance': 600, 'to_attack_missile': 110, 'reward_diff': 35},
    {'fired': True, 'coords': [75, 80], 'theta': 360, 'fired_time': 60, 'start_distance': 650, 'to_attack_missile': 120, 'reward_diff': 40},
    {'fired': True, 'coords': [85, 90], 'theta': 405, 'fired_time': 55, 'start_distance': 700, 'to_attack_missile': 130, 'reward_diff': 45},
    {'fired': True, 'coords': [95, 100], 'theta': 450, 'fired_time': 50, 'start_distance': 750, 'to_attack_missile': 140, 'reward_diff': 50},
    {'fired': True, 'coords': [105, 110], 'theta': 495, 'fired_time': 45, 'start_distance': 800, 'to_attack_missile': 150, 'reward_diff': 55},
    {'fired': True, 'coords': [115, 120], 'theta': 540, 'fired_time': 40, 'start_distance': 850, 'to_attack_missile': 160, 'reward_diff': 60},
    {'fired': True, 'coords': [125, 130], 'theta': 585, 'fired_time': 35, 'start_distance': 900, 'to_attack_missile': 170, 'reward_diff': 65},
    {'fired': True, 'coords': [135, 140], 'theta': 630, 'fired_time': 30, 'start_distance': 950, 'to_attack_missile': 180, 'reward_diff': 70},
    {'fired': True, 'coords': [145, 150], 'theta': 675, 'fired_time': 25, 'start_distance': 1000, 'to_attack_missile': 190, 'reward_diff': 75},
    {'fired': True, 'coords': [155, 160], 'theta': 720, 'fired_time': 20, 'start_distance': 1050, 'to_attack_missile': 200, 'reward_diff': 80},
    {'fired': True, 'coords': [165, 170], 'theta': 765, 'fired_time': 15, 'start_distance': 1100, 'to_attack_missile': 210, 'reward_diff': 85}
]
armed_defense_missiles = [
    {'fired': False, 'coords': [25, 30], 'theta': 135, 'to_attack_missile': 70},
    {'fired': False, 'coords': [35, 40], 'theta': 180, 'to_attack_missile': 80},
    {'fired': False, 'coords': [45, 50], 'theta': 225, 'to_attack_missile': 90},
    {'fired': False, 'coords': [55, 60], 'theta': 270, 'to_attack_missile': 100},
    {'fired': False, 'coords': [65, 70], 'theta': 315, 'to_attack_missile': 110},
    {'fired': False, 'coords': [75, 80], 'theta': 360, 'to_attack_missile': 120},
    {'fired': False, 'coords': [85, 90], 'theta': 405, 'to_attack_missile': 130},
    {'fired': False, 'coords': [95, 100], 'theta': 450, 'to_attack_missile': 140},
    {'fired': False, 'coords': [105, 110], 'theta': 495, 'to_attack_missile': 150},
    {'fired': False, 'coords': [115, 120], 'theta': 540, 'to_attack_missile': 160},
    {'fired': False, 'coords': [125, 130], 'theta': 585, 'to_attack_missile': 170},
    {'fired': False, 'coords': [135, 140], 'theta': 630, 'to_attack_missile': 180},
    {'fired': False, 'coords': [145, 150], 'theta': 675, 'to_attack_missile': 190}
]

state_array = get_state_array(global_time, reward, target_coords, defense_coords, attack_coords, attack_missile_info, fired_defense_missiles, armed_defense_missiles)
print("Array length:", len(state_array))
print("Array:", state_array)
print("Len bof fired_defense_missiles:", len(fired_defense_missiles))
print("Len of armed_defense_missiles:", len(armed_defense_missiles))
