import pygame
import random
import math
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Squares")

NUM_SQUARES = 15

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

FLEE_BUFFER = 20

squares = []
for _ in range(NUM_SQUARES):
    size = random.randint(1, 100)
    color = random.choice(COLORS)

    x = random.uniform(0, WIDTH - size)
    y = random.uniform(0, HEIGHT - size)
    
    speed = (20 / size) * 120
    angle = random.uniform(0, 2 * math.pi)

    dx = math.cos(angle) * speed
    dy = math.sin(angle) * speed

    # lifedpan
    birth_time = time.time()
    lifespan = random.uniform(10, 15)

    squares.append([x, y, dx, dy, size, color, birth_time, lifespan])  # ✅ MODIFIED

running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

while running:
    dt = clock.tick(60) / 1000

    screen.fill((75, 30, 75))

    current_time = time.time()  # ✅ ADDED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    new_squares = []

    for square in squares:
        x, y, dx, dy, size, color, birth_time, lifespan = square  # ✅ MODIFIED

        age = current_time - birth_time
        fade_duration = 1.5  # seconds

        # alpha stuff
        if age < lifespan - fade_duration:
            alpha = 255
        else:
            fade_progress = (age - (lifespan - fade_duration)) / fade_duration
            fade_progress = max(0, min(1, fade_progress))
            alpha = int(255 * (1 - fade_progress))

        # if dead, replace
        if age >= lifespan:
            size = random.randint(1, 100)
            color = random.choice(COLORS)

            x = random.uniform(0, WIDTH - size)
            y = random.uniform(0, HEIGHT - size)

            speed = (20 / size) * 120
            angle = random.uniform(0, 2 * math.pi)

            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed

            birth_time = current_time
            lifespan = random.uniform(10, 15)

            new_squares.append([x, y, dx, dy, size, color, birth_time, lifespan])
            continue  # skip rest of old square

        speed = math.hypot(dx, dy)

        if random.random() < 0.4 * dt * 60:
            angle = random.uniform(-0.3, 0.3)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            dx, dy = (
                dx * cos_a - dy * sin_a,
                dx * sin_a + dy * cos_a
            )

            length = math.hypot(dx, dy)
            if length != 0:
                dx = (dx / length) * speed
                dy = (dy / length) * speed

        x += dx * dt
        y += dy * dt

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

        
        temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        temp_surface.fill((*color, alpha))
        screen.blit(temp_surface, (int(x), int(y)))

        new_squares.append([x, y, dx, dy, size, color, birth_time, lifespan])  # ✅ MODIFIED

    squares = new_squares

    # interactions (UNCHANGED)
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            s1 = squares[i]
            s2 = squares[j]

            x1, y1, dx1, dy1, size1, _, _, _ = s1
            x2, y2, dx2, dy2, size2, _, _, _ = s2 

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