import time

num_prints = 100  # Number of prints you want
start_time = time.time()

for _ in range(num_prints):
    elapsed_time = time.time() - start_time

    print("Start time:", start_time)
    print("Elapsed time:", elapsed_time)
    print()  # Print an empty line for separation