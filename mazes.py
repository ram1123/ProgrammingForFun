from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random


def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]

    def dfs(x, y):
        maze[y][x] = 0
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0
                dfs(nx, ny)

    # Start DFS from a cell that does not affect the outer walls
    dfs(1, 1)
    # Ensure the borders remain intact
    for i in range(width):
        maze[0][i] = 1
        maze[height - 1][i] = 1
    for i in range(height):
        maze[i][0] = 1
        maze[i][width - 1] = 1

    # Create entry and exit
    maze[1][0] = 0  # Entry at top just after the corner
    maze[height - 2][width - 1] = 0  # Exit at bottom just before the corner
    return maze


def save_maze_to_pdf(maze, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    cell_size = 20  # Adjust cell size as needed
    maze_width = len(maze[0])
    maze_height = len(maze)

    # Center the maze on the page
    page_width, page_height = letter
    x_offset = (page_width - maze_width * cell_size) / 2
    y_offset = (page_height - maze_height * cell_size) / 2

    # Draw walls
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                c.rect(
                    x * cell_size + x_offset,
                    page_height - (y + 1) * cell_size - y_offset,
                    cell_size,
                    cell_size,
                    fill=1,
                )

    c.save()


# Example usage:
maze = generate_maze(20, 20)  # Adjust size as needed
save_maze_to_pdf(maze, "maze.pdf")
