import math
reward = 0
theta = 0.05 
missile_angle = 0.05
theta_deg = math.degrees(theta)
missile_angle_deg = math.degrees(missile_angle)
print("theta: ", theta)
print("missile_angle: ", missile_angle)
print("theta deg: ", theta_deg)
print("missile_angle deg: ", missile_angle_deg)

angle_diff = abs(theta - missile_angle)
angle_diff_deg = math.degrees(angle_diff)
print("angle_diff: ", angle_diff)
print("angle_diff deg: ", angle_diff_deg)
print("2*math.pi - angle_diff: ", 2*math.pi - angle_diff)
angle_diff = min(angle_diff, 2*math.pi - angle_diff)
angle_diff_deg = math.degrees(angle_diff)

if angle_diff < 0.05:
    try:
        if 1 / angle_diff < 100:
            reward += 1 / angle_diff
        else:
            100
    except ZeroDivisionError:
        reward += 100
    print("reward: ", reward)
else:
    reward -= (2 * angle_diff)
    print("0.1 * angle_diff: ", 0.1 * angle_diff)
    print("reward: ", reward)