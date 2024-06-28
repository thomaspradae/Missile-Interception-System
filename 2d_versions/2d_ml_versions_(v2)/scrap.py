import numpy as np

# Define coordinates and actions
coord_attack = np.array([0, 0])
coord_defend = np.array([1, 1])
coord_target = np.array([2, 2])

coords = [coord_attack, coord_defend, coord_target]
actions = [
    ((0, None), 1),
    ((1, None), 2),
    ((2, None), 3)
]

# Create a dictionary entry with coordinates and actions
my_dict = {"1": coords + actions}

print(my_dict["1"])
print(my_dict["1"][3][0][0])

episode = my_dict["1"]
print(episode)

def debugger(episode):
    coord_attacking = episode[0]
    coord_defending = episode[1]
    coord_target = episode[2]

    print(coord_attacking)
    print(coord_defending)
    print(coord_target)

    actions = episode[3:]
    print(actions)

debugger(episode)