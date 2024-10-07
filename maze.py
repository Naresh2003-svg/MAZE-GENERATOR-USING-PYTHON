import random
import pygame
import numpy as np
import matplotlib.pyplot as plt  # Import matplotlib

# Maze generation
def create_maze(width, height):
    maze = [['#'] * (2 * width + 1) for _ in range(2 * height + 1)]

    def carve(x, y):
        maze[y][x] = ' '
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < 2 * width and 1 <= ny < 2 * height and maze[ny][nx] == '#':
                maze[y + dy // 2][x + dx // 2] = ' '
                carve(nx, ny)

    carve(1, 1)
    return maze

# Draw maze using matplotlib
def visualize_maze(mat_maze):
    plt.imshow(mat_maze, cmap='binary', origin='upper')
    plt.axis('off')
    plt.show()

# Pygame for manual solving
def manual_solve(maze):
    cell_size = 20
    width = len(maze[0])
    height = len(maze)
    
    pygame.init()
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption("Manual Maze Solver")
    
    # Starting position
    player_pos = [1, 1]  # Entrance
    path = []  # To store the path taken
    path_index = -1  # To track the current position in the path
    running = True

    while running:
        screen.fill((255, 255, 255))
        
        # Draw the maze
        for y in range(height):
            for x in range(width):
                color = (255, 255, 255) if maze[y][x] == ' ' else (0, 0, 0)
                pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
        
        # Draw the player
        pygame.draw.rect(screen, (255, 0, 0), (player_pos[0] * cell_size, player_pos[1] * cell_size, cell_size, cell_size))
        
        # Draw the path taken
        for (px, py) in path:
            pygame.draw.rect(screen, (0, 255, 0), (px * cell_size, py * cell_size, cell_size, cell_size))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Movement controls
                if event.key == pygame.K_UP and maze[player_pos[1] - 1][player_pos[0]] == ' ':
                    player_pos[1] -= 1
                    path.append(tuple(player_pos))
                    path_index += 1
                elif event.key == pygame.K_DOWN and maze[player_pos[1] + 1][player_pos[0]] == ' ':
                    player_pos[1] += 1
                    path.append(tuple(player_pos))
                    path_index += 1
                elif event.key == pygame.K_LEFT and maze[player_pos[1]][player_pos[0] - 1] == ' ':
                    player_pos[0] -= 1
                    path.append(tuple(player_pos))
                    path_index += 1
                elif event.key == pygame.K_RIGHT and maze[player_pos[1]][player_pos[0] + 1] == ' ':
                    player_pos[0] += 1
                    path.append(tuple(player_pos))
                    path_index += 1
                
                # Backward movement
                if event.key == pygame.K_BACKSPACE and path_index > 0:
                    path_index -= 1
                    player_pos = list(path[path_index])  # Move back in the path
                elif event.key == pygame.K_DELETE and path_index < len(path) - 1:
                    path_index += 1
                    player_pos = list(path[path_index])  # Move forward in the path

                # Ensure player position is recorded in path if it's a new move
                if tuple(player_pos) not in path:
                    path.append(tuple(player_pos))
                    path_index += 1

    pygame.quit()

# Example usage
width, height = 20, 20  # Increased size for a bigger maze
maze = create_maze(width, height)

# Convert maze for visualization
mat_maze = np.array([[1 if cell == '#' else 0 for cell in row] for row in maze])

# Visualize the generated maze using matplotlib
visualize_maze(mat_maze)

# Allow manual solving of the maze using pygame
manual_solve(maze)
