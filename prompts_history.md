# Prompts History

Automatically captured prompt log. Entries are appended in chronological order (oldest first).

### 30-03-2026 13:15
- **Prompt**: Read #file:copilot-instructions.md and #file:journal-logger.agent.md and execute the instructions

### 30-03-2026 14:07
- **Prompt**: import pygame import random  pygame.init()  # Screen stufg WIDTH, HEIGHT = 800, 600 screen = pygame.display.set_mode((WIDTH, HEIGHT)) pygame.display.set_caption("Moving Squares")  WHITE = (255, 255, 255) BLUE = (0, 100, 255)  NUM_SQUARES = 10 SQUARE_SIZE = 75  squares = [] for _ in range(NUM_SQUARES):     x = random.randint(0, WIDTH - SQUARE_SIZE)     y = random.randint(0, HEIGHT - SQUARE_SIZE)     dx = random.choice([-3, -2, -1, 1, 2, 3])     dy = random.choice([-3, -2, -1, 1, 2, 3])     squares.append([x, y, dx, dy])  # Game loop running = True clock = pygame.time.Clock()  while running:     screen.fill(WHITE)      for event in pygame.event.get():         if event.type == pygame.QUIT:             running = False      # Update and draw squares     for square in squares:         x, y, dx, dy = square          # Move         x += dx         y += dy          # Bounce off edges         if x <= 0 or x >= WIDTH - SQUARE_SIZE:             dx *= -1         if y <= 0 or y >= HEIGHT - SQUARE_SIZE:             dy *= -1          square[0], square[1], square[2], square[3] = x, y, dx, dy          pygame.draw.rect(screen, BLUE, (x, y, SQUARE_SIZE, SQUARE_SIZE))      pygame.display.flip()     clock.tick(60)  pygame.quit()  Look at this code and tell me how to implement different size squares and colours

### 30-03-2026 14:10
- **Prompt**: We need to store two extra values for each square: its **size** and its **color**, so each square will have `[x, y, dx, dy, size, color]`.  We can use a small set of predefined colors (like red, green, blue) and assign each square a random color from that set.  We can define a few different sizes (e.g., 20, 30, 40) and randomly assign one to each square  These properties (size and color) should be assigned when the squares are first created, inside the loop where we initialize them.

