import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
CELL_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1],  # I-shape
     [0, 1, 0]],
    
    [[1, 1],  # O-shape
     [1, 1]],
    
    [[0, 1, 0],  # T-shape
     [1, 1, 1]],
    
    [[1, 1, 0],  # S-shape
     [0, 1, 1]],
    
    [[0, 1, 1],  # Z-shape
     [1, 1, 0]],
    
    [[1, 1, 1],  # J-shape
     [0, 0, 1]],
    
    [[1, 1, 1],  # L-shape
     [1, 0, 0]]
]

# Corresponding colors for each shape
SHAPE_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

# Clock and speed
clock = pygame.time.Clock()
FPS = 60
fall_time = 0
fall_speed = 500  # Milliseconds

# Grid to track occupied cells
grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def can_move(self, dx, dy, shape=None):
        if shape is None:
            shape = self.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (new_y >= 0 and grid[new_y][new_x] != BLACK):
                        return False
        return True

    def place(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[self.y + y][self.x + x] = self.color


def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[y][x], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == BLACK for cell in row)]
    cleared_lines = GRID_HEIGHT - len(new_grid)
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(cleared_lines)] + new_grid
    return cleared_lines


def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


# Game variables
current_tetromino = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))
next_tetromino = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))
score = 0
game_over = False

# Main Game Loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic Tetris")

while True:
    screen.fill(BLACK)
    time_delta = clock.tick(FPS)
    fall_time += time_delta

    if fall_time >= fall_speed:
        if current_tetromino.can_move(0, 1):
            current_tetromino.y += 1
        else:
            current_tetromino.place()
            cleared_lines = clear_lines()
            score += cleared_lines * 100
            current_tetromino = next_tetromino
            next_tetromino = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))
            if not current_tetromino.can_move(0, 0):
                game_over = True
        fall_time = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_tetromino.can_move(-1, 0):
                current_tetromino.x -= 1
            if event.key == pygame.K_RIGHT and current_tetromino.can_move(1, 0):
                current_tetromino.x += 1
            if event.key == pygame.K_DOWN and current_tetromino.can_move(0, 1):
                current_tetromino.y += 1
            if event.key == pygame.K_UP:
                rotated_shape = [list(row) for row in zip(*current_tetromino.shape[::-1])]
                if current_tetromino.can_move(0, 0, rotated_shape):
                    current_tetromino.rotate()

    if game_over:
        draw_text("GAME OVER", 50, WHITE, WIDTH // 4, HEIGHT // 2)
        pygame.display.flip()
        continue

    draw_grid()
    for y, row in enumerate(current_tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_tetromino.color, ((current_tetromino.x + x) * CELL_SIZE, (current_tetromino.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    draw_text(f"Score: {score}", 30, WHITE, 10, 10)
    pygame.display.flip()
