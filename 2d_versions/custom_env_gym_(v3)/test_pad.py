distance = 0.02
distance_t_minus_one = 0.04

diff = distance - distance_t_minus_one
print(diff)

if diff < 0:
    print("diff < 0")
    reward_sin = -10 * diff
    reward = -10 * (diff * (0.01 + 1/distance))
    print("reward_sin", reward_sin)
    print("reward con", reward)
else:
    reward_sin = -10 * diff
    reward = -10 * (diff * 1 + 1 * (distance**2))
    print("reward_sin", reward_sin)
    print("reward con", reward)
