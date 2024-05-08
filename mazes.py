# Reference: https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96
import argparse
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

def main():
    parser = argparse.ArgumentParser(description="Generate and save mazes as PDF.")
    parser.add_argument(
        "--mode",
        choices=["single", "multiple"],
        required=True,
        help="Choose 'single' for one maze or 'multiple' for multiple mazes.",
    )
    parser.add_argument(
        "--dimension", type=int, help="Dimension of the maze if single mode."
    )
    parser.add_argument(
        "--range_start", type=int, help="Start of dimension range for multiple mazes."
    )
    parser.add_argument(
        "--range_end", type=int, help="End of dimension range for multiple mazes."
    )
    parser.add_argument(
        "--number", type=int, help="Number of mazes per dimension in multiple mode."
    )
    args = parser.parse_args()

    if args.mode == "single":
        if args.dimension is None:
            raise ValueError("Dimension is required for single maze mode.")
        maze = create_maze(args.dimension)
        fig, ax = plt.subplots(figsize=(8, 8))
        draw_maze(maze, ax)
        plt.savefig("single_maze.pdf")
        plt.close(fig)
        print("Generated single maze saved to single_maze.pdf")
    elif args.mode == "multiple":
        if None in (args.range_start, args.range_end, args.number):
            raise ValueError(
                "Range start, range end, and number are required for multiple mazes mode."
            )
        with PdfPages("multiple_mazes.pdf") as pdf:
            for dim in range(args.range_start, args.range_end + 1):
                for _ in range(args.number):
                    maze = create_maze(dim)
                    fig, ax = plt.subplots(figsize=(8, 8))
                    draw_maze(maze, ax)
                    pdf.savefig(fig)
                    plt.close(fig)
            print("Generated multiple mazes saved to multiple_mazes.pdf")


if __name__ == "__main__":
    main()
