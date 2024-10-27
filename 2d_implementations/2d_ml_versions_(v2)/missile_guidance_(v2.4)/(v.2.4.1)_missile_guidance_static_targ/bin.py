import numpy as np
import math
angle = 6.5
angle_before = angle

if angle < 0:
    angle = 2*math.pi + angle

elif angle > 2*math.pi:
    angle = angle - 2*math.pi

print("angle: ", angle)
print("angle_before: ", angle_before)
print("angle_deg: ", math.degrees(angle))
print("angle_before_deg: ", math.degrees(angle_before))

# angle_2 = 6.5
# angle = -0.1310406
# angle_deg = math.degrees(angle)
# angle_2_deg = math.degrees(angle_2)

# print("angle: ", angle)
# print("angle_deg: ", angle_deg)
# print("360-angle: ", 360 - angle_deg)

# print("angle_2: ", angle_2)
# print("angle_2_deg: ", angle_2_deg)
# print("360-angle_2: ", 360 - angle_2_deg)

# angle_non_neg = 2*math.pi - angle
# print("2pi-angle:", angle_non_neg)
# angle_non_neg_deg = math.degrees(angle_non_neg)
# print("2pi-angle_deg:", angle_non_neg_deg)

# defense[0] += (0.02 * math.cos(missile_angle)) # gotta test this




# non_neg = math.cos(missile_angle)
# neg = math.cos(missile_angle_neg)