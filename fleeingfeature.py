import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Squares")

NUM_SQUARES = 10

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

FLEE_BUFFER = 20

squares = []
for _ in range(NUM_SQUARES):
    size = random.randint(1, 100)
    color = random.choice(COLORS)

    x = random.uniform(0, WIDTH - size)
    y = random.uniform(0, HEIGHT - size)
    
    speed = (20 / size) * 120  # ✅ pixels per second
    angle = random.uniform(0, 2 * math.pi)

    dx = math.cos(angle) * speed
    dy = math.sin(angle) * speed

    squares.append([x, y, dx, dy, size, color])

running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

while running:
    dt = clock.tick(60) / 1000  # ✅ delta time

    screen.fill((75, 30, 75))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for square in squares:
        x, y, dx, dy, size, color = square

        speed = math.hypot(dx, dy)  # ✅ preserve speed

        # smoother jitter
        if random.random() < 0.4 * dt * 60:
            angle = random.uniform(-0.3, 0.3)  # smaller rotation
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            dx, dy = (
                dx * cos_a - dy * sin_a,
                dx * sin_a + dy * cos_a
            )

            # ✅ normalize back to original speed (prevents drift)
            length = math.hypot(dx, dy)
            if length != 0:
                dx = (dx / length) * speed
                dy = (dy / length) * speed

        # ✅ time-based movement
        x += dx * dt
        y += dy * dt

        # smoother wall bounce (clamp position)
        if x <= 0:
            x = 0
            dx *= -1
        elif x >= WIDTH - size:
            x = WIDTH - size
            dx *= -1

        if y <= 0:
            y = 0
            dy *= -1
        elif y >= HEIGHT - size:
            y = HEIGHT - size
            dy *= -1

        square[0], square[1], square[2], square[3] = x, y, dx, dy
        pygame.draw.rect(screen, color, (int(x), int(y), size, size))  # ✅ clean rendering

    # interactions
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            s1 = squares[i]
            s2 = squares[j]

            x1, y1, dx1, dy1, size1, _ = s1
            x2, y2, dx2, dy2, size2, _ = s2

            cx1, cy1 = x1 + size1 / 2, y1 + size1 / 2
            cx2, cy2 = x2 + size2 / 2, y2 + size2 / 2

            dist = math.hypot(cx2 - cx1, cy2 - cy1)

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

pygame.quit()
