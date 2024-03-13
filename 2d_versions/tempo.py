from manim import *

class RotateLine(Scene):
    def construct(self):
        # Define the angle theta
        theta = PI / 4  # 45 degrees

        # Create a line DE on the x-axis
        D = LEFT * 2  # Point D at (-2, 0)
        E = RIGHT * 2  # Point E at (2, 0)
        line_DE = Line(D, E, color=BLUE)

        # Add the line and a dot at the origin to the scene
        self.add(line_DE)
        self.add(Dot(ORIGIN))

        # Rotate the line counterclockwise around the origin by theta
        self.play(Rotate(line_DE, angle=theta, about_point=ORIGIN))

        # Keep the final frame for a short while
        self.wait(2)
