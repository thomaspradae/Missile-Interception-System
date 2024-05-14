import time
import sys

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.start_time = time.time() - self.elapsed_time
            self.is_running = True
            print("Stopwatch started.")

    def stop(self):
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            self.is_running = False
            print("Stopwatch stopped. Elapsed time:", self.elapsed_time, "seconds")

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        print("Stopwatch reset.")

    def display_elapsed_time(self):
        while True:
            if self.is_running:
                current_time = time.time()
                self.elapsed_time = current_time - self.start_time

            # Clear the console for a clean display
            sys.stdout.write("\rElapsed time: {:.2f} seconds".format(self.elapsed_time))
            sys.stdout.flush()
            time.sleep(0.1)

# Usage example
stopwatch = Stopwatch()

while True:
    print("\n1. Start\n2. Stop\n3. Reset\n4. Quit")
    choice = input("Enter your choice: ")

    if choice == '1':
        stopwatch.start()
        stopwatch.display_elapsed_time()
    elif choice == '2':
        stopwatch.stop()
    elif choice == '3':
        stopwatch.reset()
    elif choice == '4':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
