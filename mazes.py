# Reference: https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.backends.backend_pdf import PdfPages


def create_maze(dim):
    # Create a grid filled with walls
    maze = np.ones((dim * 2 + 1, dim * 2 + 1))

    # Define the starting point
    x, y = (0, 0)
    maze[2 * x + 1, 2 * y + 1] = 0

    # Initialize the stack with the starting point
    stack = [(x, y)]
    while stack:
        x, y = stack[-1]

        # Define possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < dim
                and 0 <= ny < dim
                and maze[2 * nx + 1, 2 * ny + 1] == 1
            ):
                maze[2 * nx + 1, 2 * ny + 1] = 0
                maze[2 * x + 1 + dx, 2 * y + 1 + dy] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()

    # Create an entrance and an exit
    maze[1, 0] = 0
    maze[-2, -1] = 0

    return maze


def draw_maze(maze, ax):
    ax.imshow(maze, cmap=plt.cm.binary, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])

    # Draw entry and exit arrows
    ax.arrow(0, 1, 0.4, 0, fc="green", ec="green", head_width=0.3, head_length=0.3)
    ax.arrow(
        maze.shape[1] - 1,
        maze.shape[0] - 2,
        0.4,
        0,
        fc="blue",
        ec="blue",
        head_width=0.3,
        head_length=0.3,
    )


if __name__ == "__main__":

    # dim = int(input("Enter the dimension of the maze: "))
    # maze = create_maze(dim)
    # draw_maze(maze, "maze.pdf")

    with PdfPages("mazes.pdf") as pdf:
        for dim in range(7, 15):  # For dimensions from 3 to 21
            for _ in range(10):  # Generate 10 mazes for each dimension
                maze = create_maze(dim)
                fig, ax = plt.subplots(figsize=(8, 8))
                draw_maze(maze, ax)
                pdf.savefig(fig)  # Save the current figure into the pdf
                plt.close(fig)  # Close the figure to free up memory
