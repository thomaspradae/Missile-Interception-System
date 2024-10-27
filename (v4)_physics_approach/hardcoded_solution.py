import numpy as np

def hard_coded_nav(azimuth_prime, azimuth):

    print("Azimuth Prime: ", azimuth_prime)
    print("Azimuth: ", azimuth)

    # turn to radians
    azimuth_prime = np.deg2rad(azimuth_prime)
    azimuth = np.deg2rad(azimuth)

    print("Azimuth Prime rads: ", azimuth_prime)
    print("Azimuth rads: ", azimuth)
    
    # correct PHI
    # calculate the difference between azimuth and azimuth prime
    azimuth_diff = azimuth_prime - azimuth
    print("Azimuth Diff: ", azimuth_diff)

    if azimuth_diff < 0:
        azimuth_diff = abs(azimuth_diff)
        print("Fucking inside first az < 0")
        right = True

    else:
        right = False

    if azimuth_diff > np.pi:
        azimuth_diff = 2 * np.pi - azimuth_diff
        right = not right

    # convert to degrees
    azimuth_diff = np.rad2deg(azimuth_diff)

    return azimuth_diff, right
    
azimuth = 30
azimuth_prime = 10

result_1 = hard_coded_nav(azimuth_prime, azimuth)
print("Difference: ", result_1[0])
print("Right: ", result_1[1])
    

    




#     if difference is larger than pi then go the other way, if the difference is positive then turn left, if negative then turn right

#     if azimuth_diff < np.pi:
#         print("Turning A")

#     else:
#         print("Turning B")
#         azimuth_diff = 2 * np.pi - abs(azimuth_diff)
    
#     return azimuth_diff

# hard_coded_nav(azimuth_prime, azimuth)
