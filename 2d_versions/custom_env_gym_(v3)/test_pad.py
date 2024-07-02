distance = 0.095
distance_t_minus_one = 0.90

diff = -1
print(diff)

if diff < 0:
    print("diff < 0")
    reward_sin = -1 * diff
    reward = -1 * (diff * (0.01 + 1/distance))
    print("reward_sin", reward_sin)
    print("reward con", reward)
else:
    reward_sin = -1 * diff
    reward = -5 * (diff * 1 + 1 * (1 * distance**2))
    print("reward_sin", reward_sin)
    print("reward con", reward)
