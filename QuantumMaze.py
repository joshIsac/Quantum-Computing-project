import qiskit 
from qiskit_aer import AerSimulator 
from qiskit import QuantumCircuit
import pygame
import random
from qiskit.visualization import plot_histogram
from IPython.display import display



#Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Maze")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Quantum Maze Variables
quantum_state = [1, 0]  # Initial state (superposition of 0 and 1)
maze_size = 10
maze = []

# Player Position
player_pos = [0, 0]  # Start position at the top-left of the maze
player_size = 30

# Quantum Maze Generator (for simplicity, a grid of walls and paths)
def generate_maze():
    maze = []
    for y in range(maze_size):
        row = []
        for x in range(maze_size):
            if random.random() > 0.3:  # 70% chance of path
                row.append(1)  # 1 represents a path
            else:
                row.append(0)  # 0 represents a wall
        maze.append(row)
    maze[0][0] = 1  # Ensure start is always open
    maze[maze_size - 1][maze_size - 1] = 1  # Ensure exit is open
    return maze



# Quantum Operation to modify the player's quantum state (superposition collapse)
def apply_quantum_move():
    global quantum_state

    # Simulating a quantum measurement
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply a Hadamard gate to create superposition
    qc.measure(0, 0)
    simulator=AerSimulator()
    result = simulator.run(qc).result()
    counts = result.get_counts()
    # Display the measurement results
    print("Measurement results:", counts)
    # Plot the measurement results
    display(plot_histogram(counts))
    
    if '1' in counts:
     quantum_state = [0, 1]  # Collapse to state 1
    else:
     quantum_state = [1, 0]  # Collapse to state 0

# Draw the maze on the screen
def draw_maze():
    block_size = WIDTH // maze_size
    for y in range(maze_size):
        for x in range(maze_size):
            if maze[y][x] == 0:
                pygame.draw.rect(screen, BLACK, (x * block_size, y * block_size, block_size, block_size))
            else:
                pygame.draw.rect(screen, WHITE, (x * block_size, y * block_size, block_size, block_size))

# Draw the player
def draw_player():
    pygame.draw.rect(screen, GREEN, (player_pos[0] * (WIDTH // maze_size), player_pos[1] * (HEIGHT // maze_size), player_size, player_size))

# Main game loop
def main():
    global player_pos, maze, quantum_state

    maze = generate_maze()

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(BLACK)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Player Movement (Using Arrow Keys)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0 and maze[player_pos[1]][player_pos[0] - 1] == 1:
            player_pos[0] -= 1
            apply_quantum_move()  # Apply quantum effect
        if keys[pygame.K_RIGHT] and player_pos[0] < maze_size - 1 and maze[player_pos[1]][player_pos[0] + 1] == 1:
            player_pos[0] += 1
            apply_quantum_move()  # Apply quantum effect
        if keys[pygame.K_UP] and player_pos[1] > 0 and maze[player_pos[1] - 1][player_pos[0]] == 1:
            player_pos[1] -= 1
            apply_quantum_move()  # Apply quantum effect
        if keys[pygame.K_DOWN] and player_pos[1] < maze_size - 1 and maze[player_pos[1] + 1][player_pos[0]] == 1:
            player_pos[1] += 1
            apply_quantum_move()  # Apply quantum effect

        # Draw Maze and Player
        draw_maze()
        draw_player()

        # Check for exit
        if player_pos == [maze_size - 1, maze_size - 1]:
            font = pygame.font.SysFont(None, 55)
            text = font.render("You Win!", True, GREEN)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
