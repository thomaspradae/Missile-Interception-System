import numpy as np
import matplotlib.pyplot as plt

def calculate_final(z, dist):
    if z > 0:
        finalcon = -1 * (0.5 * ((10 * (z**2))) * (1 + 0.001*(dist**2)))
        # finalsin = -1 * (0.5 * (10 * (z**2)))
    else:
        finalcon = 0.5 * (10 * (z**2) * (1 + (1/dist)))
        # finalsin = 0.5 * (10 * (z**2))
    return finalcon#, finalsin

print(calculate_final(-0.7, 0.1))
print(calculate_final(1.7, 0.1))


# z_range = np.linspace(-0.9, 3, 100)
# dist_range = np.linspace(0.1, 12, 100)

# Z, DIST = np.meshgrid(z_range, dist_range)

# FINALCON = np.zeros_like(Z)
# FINALSIN = np.zeros_like(Z)

# for i in range(Z.shape[0]):
#     for j in range(Z.shape[1]):
#         FINALCON[i,j], FINALSIN[i,j] = calculate_final(Z[i,j], DIST[i,j])

# fig = plt.figure(figsize=(15, 5))

# ax1 = fig.add_subplot(121, projection='3d')
# surf1 = ax1.plot_surface(Z, DIST, FINALCON, cmap='viridis')
# ax1.set_xlabel('z')
# ax1.set_ylabel('dist')
# ax1.set_zlabel('finalcon')
# ax1.set_title('Surface plot of finalcon')
# fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=5)

# ax2 = fig.add_subplot(122, projection='3d')
# surf2 = ax2.plot_surface(Z, DIST, FINALSIN, cmap='viridis')
# ax2.set_xlabel('z')
# ax2.set_ylabel('dist')
# ax2.set_zlabel('finalsin')
# ax2.set_title('Surface plot of finalsin')
# fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=5)

# plt.tight_layout()
# plt.show()