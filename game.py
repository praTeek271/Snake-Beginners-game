import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)

# Set up the game variables
snake_size = 20
snake_speed = 15

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

# Function to display score on the screen
def show_score(score):
    text = font.render("Score: " + str(score), True, BLACK)
    win.blit(text, (10, 10))

# Function to display game over message
def game_over():
    text = font.render("Game Over", True, BLACK)
    win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(width / 2, height / 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.color = (0, 255, 0)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        cur = self.get_head_position()
        x, y = cur

        if self.direction == "UP":
            y -= snake_size
        elif self.direction == "DOWN":
            y += snake_size
        elif self.direction == "LEFT":
            x -= snake_size
        elif self.direction == "RIGHT":
            x += snake_size

        self.positions.insert(0, (x, y))

        if len(self.positions) > self.length:
            self.positions.pop()

    def change_direction(self, new_direction):
        if new_direction == "UP" and self.direction != "DOWN":
            self.direction = new_direction
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = new_direction
        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = new_direction
        elif new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = new_direction

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], snake_size, snake_size))

    def check_collision(self):
        head = self.get_head_position()

        # Check if snake hits the boundaries of the window
        if (
            head[0] < 0
            or head[0] >= width
            or head[1] < 0
            or head[1] >= height
        ):
            return True

        # Check if snake hits itself
        if head in self.positions[1:]:
            return True

        return False

    def handle_collision_with_food(self, food):
        if self.get_head_position() == food.position:
            self.length += 1
            self.score += 1
            food.generate_position()

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.generate_position()

    def generate_position(self):
        x = random.randint(0, (width - snake_size) // snake_size) * snake_size
        y = random.randint(0, (height - snake_size) // snake_size) * snake_size
        self.position = (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], snake_size, snake_size))


def main():
    # Initialize the snake and food
    snake = Snake()
    food = Food()

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")

        # Move the snake
        snake.move()

        # Check for collisions
        if snake.check_collision():
            game_over()
            break

        # Handle collision with food
        snake.handle_collision_with_food(food)

        # Clear the screen
        win.fill(BLACK)

        # Draw snake and food
        snake.draw(win)
        food.draw(win)

        # Display the score
        show_score(snake.score)

        # Update the display
        pygame.display.update()

        # Control the snake speed
        clock.tick(snake_speed)

    # Quit the game
    pygame.quit()


if __name__ == "__main__":
    main()
