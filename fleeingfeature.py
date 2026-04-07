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
FLEE_BUFFER = 20

squares = []
for _ in range(NUM_SQUARES):
    size = random.randint(1, 100)
    color = random.choice(COLORS)

    x = random.randint(0, WIDTH - size)
    y = random.randint(0, HEIGHT - size)
    
    dx = int((20/size) * 5)
    dy = int((20/size) * 5)

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
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            s1 = squares[i]
            s2 = squares[j]

            x1, y1, dx1, dy1, size1, _ = s1
            x2, y2, dx2, dy2, size2, _ = s2

            # centers
            cx1, cy1 = x1 + size1 / 2, y1 + size1 / 2
            cx2, cy2 = x2 + size2 / 2, y2 + size2 / 2

            # distance
            dist = math.sqrt((cx2 - cx1)**2 + (cy2 - cy1)**2)

            # flee threshold
            threshold = size1 + size2 + FLEE_BUFFER

            if dist < threshold:
                if size1 < size2:
                    s1[2] *= -1
                    s1[3] *= -1
                elif size2 < size1:
                    s2[2] *= -1
                    s2[3] *= -1

    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
