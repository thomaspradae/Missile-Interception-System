import pygame
import sys
import numpy as np
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDING = 50  
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 36)


class Point: 
    def __init__(self, type):
        self.type = type
        self.coordinates = np.array([0, 0])

    def create_target(self):
        x = random.uniform(-3.0, 3.0)
        y = random.uniform(-2.0, 2.0)
        self.coordinates = np.array([x, y])
        return self.coordinates
    
    def create_defense(self, target):
        x = random.uniform(target.coordinates[0] - 1.5, target.coordinates[0] + 1.5)
        y = random.uniform(target.coordinates[1] - 1.5, target.coordinates[1] + 1.5)
        self.coordinates = np.array([x, y])
        return self.coordinates
    
    def create_attack(self, target, defense):
        x_side_left = random.uniform(-9.5, target.coordinates[0] - 2)
        x_side_right = random.uniform(target.coordinates[0] + 2, 9.5)
        y_below = random.uniform(target.coordinates[1] - 2, -9.5)
        y_above = random.uniform(target.coordinates[1] + 2, 9.5)
        x_inclusive = random.uniform(-9.5, 9.5)
        y_inclusive = random.uniform(-9.5, 9.5)
        y_below_x_inclusive = np.array([x_inclusive, y_below])
        y_above_x_inclusive = np.array([x_inclusive, y_above])
        x_left_y_inclusive = np.array([x_side_left, y_inclusive])
        x_right_y_inclusive = np.array([x_side_right, y_inclusive])

        self.coordinates = random.choice([y_below_x_inclusive, y_above_x_inclusive, x_left_y_inclusive, x_right_y_inclusive])
        return self.coordinates

# Create instances of Point class
target = Point("target")
defense = Point("defense")
attack = Point("attack")

# Generate points
target.create_target()
defense.create_defense(target)
attack.create_attack(target, defense)

# Print
print("Target Coordinates:", target.coordinates)
print("Defense Coordinates:", defense.coordinates)
print("Attack Coordinates:", attack.coordinates)

# Set the coordinates to a given value
target.coordinates = np.array([1, 1])
defense.coordinates = np.array([2, 2])
attack.coordinates = np.array([3, 3])

# Main game loop
def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Fill the screen with white color
        screen.fill(WHITE)

        # Draw grid lines
        draw_grid()

        draw_point(target, RED)
        draw_point(defense, GREEN)
        draw_point(attack, BLUE)

        # Display mouse coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text_surface = font.render(f"Mouse Coordinates: ({mouse_x}, {mouse_y})", True, BLACK)
        screen.blit(text_surface, (10, 10))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def draw_point(point, color):
    # Scale and shift coordinates to fit within the screen with padding
    scaled_x = int((point.coordinates[0] + 10) * (SCREEN_WIDTH - 2 * PADDING) / 20) + PADDING
    scaled_y = int((point.coordinates[1] + 10) * (SCREEN_HEIGHT - 2 * PADDING) / 20) + PADDING
    pygame.draw.circle(screen, color, (scaled_x, SCREEN_HEIGHT - scaled_y), 5)

def draw_grid():
    # Draw horizontal lines
    for y in range(-10, 11):
        if y == 0 or y == 10 or y == -10:
            pygame.draw.line(screen, BLACK, (PADDING, SCREEN_HEIGHT // 2 + y * (SCREEN_HEIGHT - 2 * PADDING) // 20 + PADDING), 
                                             (SCREEN_WIDTH - PADDING, SCREEN_HEIGHT // 2 + y * (SCREEN_HEIGHT - 2 * PADDING) // 20 + PADDING), 3)
        else:
            pygame.draw.line(screen, GRAY, (PADDING, SCREEN_HEIGHT // 2 + y * (SCREEN_HEIGHT - 2 * PADDING) // 20 + PADDING), 
                                            (SCREEN_WIDTH - PADDING, SCREEN_HEIGHT // 2 + y * (SCREEN_HEIGHT - 2 * PADDING) // 20 + PADDING))

    # Draw vertical lines
    for x in range(-10, 11):
        if x == 0 or x == 10 or x == -10:
            pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2 + x * (SCREEN_WIDTH - 2 * PADDING) // 20 + PADDING, PADDING), 
                                             (SCREEN_WIDTH // 2 + x * (SCREEN_WIDTH - 2 * PADDING) // 20 + PADDING, SCREEN_HEIGHT - PADDING), 3)
        else:
            pygame.draw.line(screen, GRAY, (SCREEN_WIDTH // 2 + x * (SCREEN_WIDTH - 2 * PADDING) // 20 + PADDING, PADDING), 
                                            (SCREEN_WIDTH // 2 + x * (SCREEN_WIDTH - 2 * PADDING) // 20 + PADDING, SCREEN_HEIGHT - PADDING))


if __name__ == "__main__":
    main()
