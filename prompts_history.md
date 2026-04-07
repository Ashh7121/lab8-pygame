# Prompts History

Automatically captured prompt log. Entries are appended in chronological order (oldest first).

### 30-03-2026 13:15
- **Prompt**: Read #file:copilot-instructions.md and #file:journal-logger.agent.md and execute the instructions

### 30-03-2026 14:07
- **Prompt**: import pygame import random  pygame.init()  # Screen stufg WIDTH, HEIGHT = 800, 600 screen = pygame.display.set_mode((WIDTH, HEIGHT)) pygame.display.set_caption("Moving Squares")  WHITE = (255, 255, 255) BLUE = (0, 100, 255)  NUM_SQUARES = 10 SQUARE_SIZE = 75  squares = [] for _ in range(NUM_SQUARES):     x = random.randint(0, WIDTH - SQUARE_SIZE)     y = random.randint(0, HEIGHT - SQUARE_SIZE)     dx = random.choice([-3, -2, -1, 1, 2, 3])     dy = random.choice([-3, -2, -1, 1, 2, 3])     squares.append([x, y, dx, dy])  # Game loop running = True clock = pygame.time.Clock()  while running:     screen.fill(WHITE)      for event in pygame.event.get():         if event.type == pygame.QUIT:             running = False      # Update and draw squares     for square in squares:         x, y, dx, dy = square          # Move         x += dx         y += dy          # Bounce off edges         if x <= 0 or x >= WIDTH - SQUARE_SIZE:             dx *= -1         if y <= 0 or y >= HEIGHT - SQUARE_SIZE:             dy *= -1          square[0], square[1], square[2], square[3] = x, y, dx, dy          pygame.draw.rect(screen, BLUE, (x, y, SQUARE_SIZE, SQUARE_SIZE))      pygame.display.flip()     clock.tick(60)  pygame.quit()  Look at this code and tell me how to implement different size squares and colours

### 30-03-2026 14:10
- **Prompt**: We need to store two extra values for each square: its **size** and its **color**, so each square will have `[x, y, dx, dy, size, color]`.  We can use a small set of predefined colors (like red, green, blue) and assign each square a random color from that set.  We can define a few different sizes (e.g., 20, 30, 40) and randomly assign one to each square  These properties (size and color) should be assigned when the squares are first created, inside the loop where we initialize them.

### 02-04-2026 14:08
- **Prompt**: Are you logging all this in the journal?

### 02-04-2026 14:08
- **Prompt**: Please append entries to JOURNAL.md for the following interactions. Use the template from .github/agents/journal-logger.agent.md:  1. First entry: User asked how to make squares jitter when they move by implementing a 'small rotation of the speed vector'. I explained two approaches: (a) rotating velocity by a small angle every frame for smooth continuous jitter, or (b) randomly rotating velocity each frame for choppy jitter. Provided the math formula using cos/sin rotation and example code snippets for both strategies.  2. Second entry: User asked if I'm logging to the journal. No code changes occurred.  Please log both entries chronologically at the end of JOURNAL.md.

### 02-04-2026 14:11
- **Prompt**: Okay cool, now I want to really understand what it means to apply a small rotation to the vectors to make it look like they are jittering

### 02-04-2026 14:14
- **Prompt**: if dx = 5 and dy = 0, it's basically moving 5 on the horizontal axis and nothing in the vertical axis.  The line now points to east, line length does not change.   Speed stays the same cause it just rotates.  Hmmmm it would look like me when I'm lost in Paris. Going back and forth. I assume that when this happens really fast, it looks like the squares are shaking.

### 02-04-2026 14:23
- **Prompt**: Add these to the journal cmon how many times do i gotta remind

### 02-04-2026 14:23
- **Prompt**: Please append the following entries to JOURNAL.md in chronological order at the end:  1. User demonstrated deep understanding of velocity vector rotation for jittering: explained that dx=5, dy=0 moves purely horizontal, rotation preserves speed but changes direction, and rapid direction changes create visual jitter. Used brilliant analogy of walking lost in Paris. I confirmed their understanding and offered implementation choice (smooth vs. choppy jitter).  2. User reminded me to log to journal. No code changes.  Please log both entries using the template from .github/agents/journal-logger.agent.md with timestamps.

### 07-04-2026 11:32
- **Prompt**: Read the main.py. I need to add a new feature that makes the smaller squares flee away from the bigger ones. Here is what I am thinking: I think that we can approach this like a collision but instead of having the smaller squares moving in the opposite direction when they HIT the bigger squares, we can adjust the code so that they flee BEFORE they even hit the square so it looks like they are fleeing from the bigger squares. It's just an idea for now but that's what I got for now. Don't tell me the solution outright. Progressively move to the solution as I understand the logic

