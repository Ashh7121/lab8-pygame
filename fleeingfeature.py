import pygame
import random
import math

pygame.init()

# Screen stuff
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Squares")


NUM_SQUARES = 10


COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

SIZES = []

# TODO: Add a constant for the flee threshold buffer
# FLEE_BUFFER = ?

squares = []
for _ in range(NUM_SQUARES):
    size = random.randint(1, 100)
    color = random.choice(COLORS)

    x = random.randint(0, WIDTH - size)
    y = random.randint(0, HEIGHT - size)
    
    dx = int((20/size) * 10)
    dy = int((20/size) * 10)

    squares.append([x, y, dx, dy, size, color])


running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

while running:
    screen.fill((75, 30, 75))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for square in squares:
        x, y, dx, dy, size, color = square

        # jitteringg
        if random.random() < 0.4:  # happens sometimes, not every frame
            angle = random.uniform(-0.5, 0.5) # angle change
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            new_dx = dx * cos_a - dy * sin_a
            new_dy = dx * sin_a + dy * cos_a

            dx, dy = new_dx, new_dy

        x += dx
        y += dy

        # Bouncy bouncy
        if x <= 0 or x >= WIDTH - size:
            dx *= -1
        if y <= 0 or y >= HEIGHT - size:
            dy *= -1

        square[0], square[1], square[2], square[3] = x, y, dx, dy
        pygame.draw.rect(screen, color, (x, y, size, size))

    # TODO: NESTED LOOP SECTION
    # Add a nested loop here to check all pairs of squares
    # Outer loop: for i in range(len(squares)):
    # Inner loop: for j in range(i+1, len(squares)):
    #     Inside the loops:
    #     1. Extract data from squares[i] and squares[j]
    #     2. Calculate center coordinates for both squares
    #     3. Calculate distance between centers using Pythagorean theorem
    #     4. Calculate the flee threshold (sum of sizes + buffer)
    #     5. Check if distance < threshold
    #     6. If yes, determine which is smaller and which is bigger
    #     7. If square[i] is smaller than square[j], reverse square[i]'s velocity
    #     8. If square[j] is smaller than square[i], reverse square[j]'s velocity

    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
