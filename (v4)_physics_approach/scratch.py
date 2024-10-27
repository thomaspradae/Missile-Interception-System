theta = 1.5
theta_prime = -1.5

diff = theta_prime - theta
print(diff)

if theta_prime < theta:
    print("The enemy is below the defense")
    big_turn_down = abs(diff) - 0.5
    small_turn_down = abs(diff) - 0.1

    if big_turn_down and small_turn_down > abs(diff):
        print("Still")


    print(min(big_turn_down, small_turn_down, abs(diff)))

else:
    print("The enemy is above the defense")

# diff = -2




# calc = abs(carlos)
# print(calc)
