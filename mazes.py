# Reference: https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96
import matplotlib.pyplot as plt
import numpy as np
import random


def create_maze(dim):
    # Create a grid filled with walls
    maze = np.ones((dim * 2 + 1, dim * 2 + 1))

    # Define the starting point
    x, y = (0, 0)
    maze[2 * x + 1, 2 * y + 1] = 0

    # Initialize the stack with the starting point
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]

        # Define possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                nx >= 0
                and ny >= 0
                and nx < dim
                and ny < dim
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


def draw_maze(maze, filename="maze.pdf"):
    fig, ax = plt.subplots(figsize=(10, 10))
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

    plt.savefig(filename, format="pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    dim = int(input("Enter the dimension of the maze: "))
    maze = create_maze(dim)
    draw_maze(maze, "maze.pdf")
