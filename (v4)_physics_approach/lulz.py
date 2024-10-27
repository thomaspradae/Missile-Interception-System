from manim import *

class GradientDescentScene(Scene):
    def construct(self):
        # Define the axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 8, 1],
            axis_config={"color": WHITE}
        ).add_coordinates()

        # Define the quadratic function
        def function(x):
            return x**2

        # Create the graph of the quadratic function
        graph = axes.plot(function, color=BLUE)

        # Label the axes and function
        graph_label = axes.get_graph_label(graph, label="x^2")

        # Starting point for gradient descent
        start_x = 2
        start_y = function(start_x)

        # Create the dot representing the point
        dot = Dot(axes.c2p(start_x, start_y), color=YELLOW)

        # Define gradient descent parameters
        learning_rate = 0.1
        num_iterations = 10

        # Function to calculate gradient (derivative of x^2 is 2x)
        def gradient(x):
            return 2 * x

        # Create an animation for gradient descent
        def update_dot(dot, dt):
            nonlocal start_x
            for _ in range(num_iterations):
                start_x -= learning_rate * gradient(start_x)
                new_y = function(start_x)
                dot.move_to(axes.c2p(start_x, new_y))

        # Add the elements to the scene
        self.play(Create(axes), Create(graph), Write(graph_label))
        self.play(FadeIn(dot))

        # Run the gradient descent animation
        for _ in range(num_iterations):
            new_x = start_x - learning_rate * gradient(start_x)
            new_y = function(new_x)
            self.play(dot.animate.move_to(axes.c2p(new_x, new_y)), run_time=0.5)
            start_x = new_x

        self.wait(2)

