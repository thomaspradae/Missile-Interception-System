def distance_reward(reward, defense_missiles):
    payment_ponderations = [1, 0.9, 0.85, 0.75, 0.65, 0.55, 0.35, 0.25, 0.15, 0.05]
    max_index = len(payment_ponderations) - 1

    for i, missile in enumerate(defense_missiles):
        missile.reward_diff = missile.start_distance - missile.defense_missile_to_attack_missile
        if missile.reward_diff > 0:
            ponderation = payment_ponderations[i] if i <= max_index else 0
            missile.reward_diff *= ponderation
        reward += missile.reward_diff
    
    return reward


