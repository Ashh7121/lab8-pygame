# JavaScript/HTML5 Canvas Port Plan
## Cross-Language Porting: Python/Pygame → Vanilla JavaScript

**Project:** Moving Squares Simulation  
**Target Platform:** Browser (Single `index.html`)  
**Educational Goal:** Maintain 1-to-1 logical parity with Python original  
**Status:** Plan Only (No Implementation)

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Pygame → JavaScript/Canvas API Mapping](#pygame--javascriptcanvas-api-mapping)
3. [Data Structure Translation](#data-structure-translation)
4. [Simulation Loop Redesign](#simulation-loop-redesign)
5. [Class & Function Structure](#class--function-structure)
6. [Graphics Implementation](#graphics-implementation)
7. [Module Layout in index.html](#module-layout-in-indexhtml)
8. [Implementation Checklist](#implementation-checklist)

---

## Architecture Overview

### Current Python Structure
The `main.py` follows a procedural game loop pattern:
- **Initialization Phase:** Create pygame display, initialize squares
- **Game Loop:** 60 FPS target with delta time (dt) from `clock.tick(60)`
- **Per-Frame Operations:**
  1. Handle events (quit)
  2. Respawn system (age-based)
  3. Interaction system (collision + steering)
  4. Movement & wrapping
  5. Rendering (trails + squares + UI)
- **Cleanup:** `pygame.quit()`

### Translated JavaScript Structure
The browser version will replace pygame components with equivalent web APIs:
- **Initialization:** Canvas setup, context binding, animation frame setup
- **Animation Loop:** Replace `while running: ... clock.tick(60)` with `requestAnimationFrame(gameLoop)`
- **Per-Frame Operations:** Identical logic, same variable names, same data flow
- **Delta Time:** Calculate from `DOMHighResTimeStamp` to match `dt = clock.tick(60) / 1000`
- **Cleanup:** Browser handles window cleanup (no manual `pygame.quit()` equivalent needed)

---

## Pygame → JavaScript/Canvas API Mapping

### Event Handling

| Pygame | JavaScript |
|--------|------------|
| `pygame.event.get()` loop | `addEventListener('keydown', ...)`, `addEventListener('mousemove', ...)`, etc. |
| `event.type == pygame.QUIT` | `beforeunload` event or close button (browser-native) |
| `pygame.key.get_pressed()` | `keyboardState` object or `addEventListener` tracking |
| `pygame.mouse.get_pos()` | `mousemove` event listener |

**Note:** The current `main.py` only handles `pygame.QUIT`, so we only need a quit handler.

### Display & Rendering

| Pygame | JavaScript/Canvas |
|--------|-------------------|
| `pygame.display.set_mode((WIDTH, HEIGHT))` | `<canvas id="canvas" width="800" height="600"></canvas>` |
| `pygame.display.set_caption("...")` | `<title>` tag or `document.title` |
| `screen.fill(color_tuple)` | `ctx.fillStyle = rgbString; ctx.fillRect(0, 0, WIDTH, HEIGHT)` |
| `pygame.display.flip()` | Automatic at end of `requestAnimationFrame` callback |

### Drawing Primitives

| Pygame | JavaScript/Canvas |
|--------|-------------------|
| `pygame.draw.rect(surface, color, rect)` | `ctx.fillRect(x, y, width, height)` with `ctx.fillStyle` |
| `pygame.draw.circle(surface, color, center, radius)` | `ctx.beginPath(); ctx.arc(...); ctx.fill()` |
| `pygame.draw.lines(surface, color, closed, points, width)` | `ctx.strokeStyle = color; ctx.lineWidth = width; ctx.moveTo(...); ctx.lineTo(...)` loop |
| `pygame.Surface(..., pygame.SRCALPHA)` + alpha channel | `ctx.globalAlpha = (alpha / 255)` before drawing |
| `screen.blit(surface, (x, y))` | `ctx.drawImage(canvas, x, y)` or draw directly to main ctx |

### Text Rendering

| Pygame | JavaScript/Canvas |
|--------|-------------------|
| `pygame.font.SysFont(None, 24)` | `ctx.font = "24px sans-serif"` |
| `font.render(text, True, color)` → `screen.blit(...)` | `ctx.fillStyle = color; ctx.fillText(text, x, y)` |

### Time & Timing

| Pygame | JavaScript |
|--------|------------|
| `import time; time.time()` | `Date.now() / 1000` or `performance.now() / 1000` |
| `clock.tick(60)` returns ms elapsed | Store previous `timestamp` from `requestAnimationFrame`, calculate delta |
| `dt = clock.tick(60) / 1000` (seconds) | `dt = (currentTimestamp - lastTimestamp) / 1000` |

### Randomness

| Pygame | JavaScript |
|--------|------------|
| `import random; random.random()` | `Math.random()` |
| `random.uniform(a, b)` | `Math.random() * (b - a) + a` |
| `random.randint(a, b)` | `Math.floor(Math.random() * (b - a + 1)) + a` |
| `random.choice(list)` | `array[Math.floor(Math.random() * array.length)]` |

### Math Functions

| Pygame/Python | JavaScript |
|--------|------------|
| `import math` | `Math` object (built-in) |
| `math.pi` | `Math.PI` |
| `math.cos(angle)`, `math.sin(angle)` | `Math.cos(angle)`, `Math.sin(angle)` |
| `math.hypot(dx, dy)` | `Math.hypot(dx, dy)` (ES6+) |
| `min()`, `max()` | `Math.min()`, `Math.max()` |

---

## Data Structure Translation

### Global Configuration Constants

```python
# PYTHON
WIDTH, HEIGHT = 800, 600
COLORS = [(255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 50)]
FLEE_DISTANCE = 150
STEER_FORCE = 0.05
MAX_SQUARE_SIZE = 100
TRAILS_LENGTH = 30
GROWTH_DURATION = 0.5
POPULATION_MIX = [(5, 25), (10, 10), (30, 4)]
```

```javascript
// JAVASCRIPT
const WIDTH = 800;
const HEIGHT = 600;
const COLORS = [
  'rgb(255, 50, 50)',   // red
  'rgb(50, 255, 50)',   // green
  'rgb(50, 50, 255)',   // blue
  'rgb(255, 255, 50)'   // yellow
];
const FLEE_DISTANCE = 150;
const STEER_FORCE = 0.05;
const MAX_SQUARE_SIZE = 100;
const TRAILS_LENGTH = 30;
const GROWTH_DURATION = 0.5;
const POPULATION_MIX = [[5, 25], [10, 10], [30, 4]];
```

### Square Object (Dictionary → Object)

```python
# PYTHON - Dictionary with string keys
{
    'pos': [x, y],                     # list (x, y position)
    'vel': [dx, dy],                   # list (velocity vector)
    'size': size,                      # number (current visual size)
    'target_size': size,               # number (goal size after eating)
    'start_growth_size': size,         # number (size when growth started)
    'growth_timer': 0,                 # number (countdown to growth completion)
    'original_type_size': size,        # number (respawn size from POPULATION_MIX)
    'color': color_tuple,              # tuple (r, g, b)
    'birth': timestamp,                # number (creation time)
    'life': lifespan,                  # number (seconds until respawn)
    'max_speed': speed,                # number (velocity magnitude limit)
    'history': []                      # list of (x, y) tuples for trail
}
```

```javascript
// JAVASCRIPT - Object with same property names
{
  pos: [x, y],                        // array [x, y]
  vel: [dx, dy],                      // array [vx, vy]
  size: size,                         // number
  targetSize: size,                   // CONVERTED TO camelCase
  startGrowthSize: size,              // CONVERTED TO camelCase
  growthTimer: 0,                     // CONVERTED TO camelCase
  originalTypeSize: size,             // CONVERTED TO camelCase
  color: 'rgb(r, g, b)',              // string (CSS color)
  birth: timestamp,                   // number (milliseconds from Date.now())
  life: lifespan,                     // number (seconds)
  maxSpeed: speed,                    // CONVERTED TO camelCase
  history: []                         // array of [x, y] arrays
}
```

**Naming Convention Decision:**
- **Python uses `snake_case`:** `target_size`, `growth_timer`, etc.
- **JavaScript conventions:** Prefer `camelCase` for consistency with JS ecosystem
- **Approach:** Convert to `camelCase` in the JavaScript version while maintaining identical logic

### Color Representation

```python
# PYTHON: tuple of integers
color = (255, 50, 50)
screen.fill(color)
```

```javascript
// JAVASCRIPT: CSS color string
const color = 'rgb(255, 50, 50)';
ctx.fillStyle = color;
ctx.fillRect(...);

// OR use an object for future flexibility:
const color = { r: 255, g: 50, b: 50 };
const colorString = `rgb(${color.r}, ${color.g}, ${color.b})`;
```

---

## Simulation Loop Redesign

### Python Event Loop Model
```python
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000      # Block until 60 FPS, get elapsed time
    screen.fill((30, 20, 40))        # Clear frame
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # ... game logic here ...
    
    pygame.display.flip()            # Render to screen
```

### JavaScript AnimationFrame Model
```javascript
let lastTimestamp = performance.now();
let running = true;

// Equivalent to: while (running) { ... }
function gameLoop(currentTimestamp) {
  if (!running) return;
  
  // Calculate delta time (in seconds)
  const dt = (currentTimestamp - lastTimestamp) / 1000;
  lastTimestamp = currentTimestamp;
  
  // Clear frame (equivalent to screen.fill)
  ctx.fillStyle = 'rgb(30, 20, 40)';
  ctx.fillRect(0, 0, WIDTH, HEIGHT);
  
  // Game logic here (same structure as Python)
  
  // Render to screen (automatic in requestAnimationFrame)
  requestAnimationFrame(gameLoop);
}

// Start the loop
requestAnimationFrame(gameLoop);

// Quit handler
window.addEventListener('beforeunload', () => {
  running = false;
});
```

### Key Differences & Mapping

| Aspect | Python `clock.tick(60)` | JavaScript `requestAnimationFrame()` |
|--------|------------------------|--------------------------------------|
| **Frame Rate Control** | Blocking call that locks to 60 FPS | Browser-synced (typically 60 FPS on 60 Hz displays) |
| **Return Value** | Milliseconds elapsed since last call | `DOMHighResTimeStamp` (total elapsed since page load) |
| **Delta Time Calc** | `dt = ms_elapsed / 1000` | `dt = (current - last) / 1000` |
| **Loop Structure** | Imperative `while` loop | Recursive callback pattern |
| **Stopping the Loop** | `running = False` breaks loop | Return early from `gameLoop()` or don't call `requestAnimationFrame()` again |

### Timestamp Management in JavaScript

```javascript
let lastTimestamp;

function gameLoop(currentTimestamp) {
  // First frame: initialize last timestamp
  if (lastTimestamp === undefined) {
    lastTimestamp = currentTimestamp;
  }
  
  // Calculate dt in seconds (same as Python)
  const dt = (currentTimestamp - lastTimestamp) / 1000;
  lastTimestamp = currentTimestamp;
  
  // ... rest of game logic ...
  
  requestAnimationFrame(gameLoop);
}

// Kick off the loop
requestAnimationFrame(gameLoop);
```

---

## Class & Function Structure

### Python Functions → JavaScript Functions

#### `createSquare(size, initialMixSize = null)`

**Python:**
```python
def create_square(size, initial_mix_size=None):
    """Generate a square dict based on a specific size"""
    color = random.choice(COLORS)
    x = random.uniform(0, WIDTH - size)
    y = random.uniform(0, HEIGHT - size)
    
    speed = (30 / size) * 150
    
    angle = random.uniform(0, 2 * math.pi)
    dx = math.cos(angle) * speed
    dy = math.sin(angle) * speed

    return {
        'pos': [x, y],
        'vel': [dx, dy],
        'size': size,
        'target_size': size,
        'start_growth_size': size,
        'growth_timer': 0,
        'original_type_size': initial_mix_size if initial_mix_size else size,
        'color': color,
        'birth': time.time(),
        'life': random.uniform(12, 18),
        'max_speed': speed,
        'history': []
    }
```

**JavaScript:**
```javascript
/**
 * Equivalent to Python create_square()
 * @param {number} size - Initial size of the square
 * @param {number|null} initialMixSize - Original type size for respawning
 * @returns {Object} Square object with all properties initialized
 */
function createSquare(size, initialMixSize = null) {
  const color = COLORS[Math.floor(Math.random() * COLORS.length)];
  const x = Math.random() * (WIDTH - size);
  const y = Math.random() * (HEIGHT - size);
  
  const speed = (30 / size) * 150;
  
  const angle = Math.random() * 2 * Math.PI;
  const dx = Math.cos(angle) * speed;
  const dy = Math.sin(angle) * speed;
  
  const now = Date.now() / 1000; // Convert ms to seconds
  
  return {
    pos: [x, y],
    vel: [dx, dy],
    size: size,
    targetSize: size,
    startGrowthSize: size,
    growthTimer: 0,
    originalTypeSize: initialMixSize !== null ? initialMixSize : size,
    color: color,
    birth: now,
    life: Math.random() * (18 - 12) + 12,  // random.uniform(12, 18)
    maxSpeed: speed,
    history: []
  };
}
```

#### `checkCollision(s1, s2)`

**Python:**
```python
def check_collision(s1, s2):
    """Uses pygame.Rect to detect overlap between two square dicts"""
    rect1 = pygame.Rect(s1['pos'][0], s1['pos'][1], s1['size'], s1['size'])
    rect2 = pygame.Rect(s2['pos'][0], s2['pos'][1], s2['size'], s2['size'])
    return rect1.colliderect(rect2)
```

**JavaScript:**
```javascript
/**
 * Equivalent to Python check_collision()
 * Detects AABB (Axis-Aligned Bounding Box) overlap
 * @param {Object} s1 - First square
 * @param {Object} s2 - Second square
 * @returns {boolean} True if squares overlap
 */
function checkCollision(s1, s2) {
  // AABB collision: check if rectangles overlap
  const x1 = s1.pos[0];
  const y1 = s1.pos[1];
  const w1 = s1.size;
  const h1 = s1.size;
  
  const x2 = s2.pos[0];
  const y2 = s2.pos[1];
  const w2 = s2.size;
  const h2 = s2.size;
  
  return x1 < x2 + w2 && x1 + w1 > x2 &&
         y1 < y2 + h2 && y1 + h1 > y2;
}
```

#### `updateSpeedForSize(s)`

**Python:**
```python
def update_speed_for_size(s):
    """Recalculate speed based on new size (Bigger = Slower)"""
    s['max_speed'] = (30 / s['target_size']) * 150
```

**JavaScript:**
```javascript
/**
 * Equivalent to Python update_speed_for_size()
 * Recalculates max speed based on target_size
 * @param {Object} s - Square object to update
 */
function updateSpeedForSize(s) {
  s.maxSpeed = (30 / s.targetSize) * 150;
}
```

### Initialization Code

**Python:**
```python
squares = []
for count, size in POPULATION_MIX:
    for _ in range(count):
        squares.append(create_square(size, initial_mix_size=size))
```

**JavaScript:**
```javascript
/**
 * Equivalent to Python initialization loop
 * Creates the initial population of squares
 */
let squares = [];
for (const [count, size] of POPULATION_MIX) {
  for (let i = 0; i < count; i++) {
    squares.push(createSquare(size, size));
  }
}
```

---

## Graphics Implementation

### Color & Alpha Handling

**Python:**
```python
# Color tuple
color = (255, 50, 50)

# Drawing with alpha
age = now - s['birth']
alpha = int(255 * (s['life'] - age) / 2) if age > s['life'] - 2 else 255
alpha = max(0, min(255, alpha))

surf = pygame.Surface((int(s['size']), int(s['size'])), pygame.SRCALPHA)
surf.fill((*s['color'], alpha))
screen.blit(surf, (int(s['pos'][0]), int(s['pos'][1])))
```

**JavaScript:**
```javascript
// Color as RGB string
const color = 'rgb(255, 50, 50)';

// Drawing with alpha
const age = now - s.birth;
let alpha = 255;
if (age > s.life - 2) {
  alpha = Math.round(255 * (s.life - age) / 2);
}
alpha = Math.max(0, Math.min(255, alpha));

// Use globalAlpha for transparency
ctx.globalAlpha = alpha / 255;
ctx.fillStyle = s.color;
ctx.fillRect(Math.round(s.pos[0]), Math.round(s.pos[1]), 
             Math.round(s.size), Math.round(s.size));
ctx.globalAlpha = 1.0; // Reset for next drawing
```

### Trail Rendering

**Python:**
```python
# Draw Trail
if len(s['history']) > 1:
    pygame.draw.lines(screen, s['color'], False, s['history'], 1)
```

**JavaScript:**
```javascript
/**
 * Equivalent to pygame.draw.lines()
 * Draws the trail of past positions
 */
if (s.history.length > 1) {
  ctx.strokeStyle = s.color;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(s.history[0][0], s.history[0][1]);
  for (let i = 1; i < s.history.length; i++) {
    ctx.lineTo(s.history[i][0], s.history[i][1]);
  }
  ctx.stroke();
}
```

### Text Rendering (FPS Counter)

**Python:**
```python
fps_text = font.render(f"Total: {len(squares)} | FPS: {int(clock.get_fps())}", 
                       True, (200, 200, 200))
screen.blit(fps_text, (10, 10))
```

**JavaScript:**
```javascript
/**
 * Equivalent to pygame font.render() + screen.blit()
 * Displays FPS counter and square count
 */
// Calculate FPS (store frame count and time)
const fpsText = `Total: ${squares.length} | FPS: ${Math.round(1 / dt)}`;
ctx.fillStyle = 'rgb(200, 200, 200)';
ctx.font = '24px sans-serif';
ctx.fillText(fpsText, 10, 10);
```

---

## Module Layout in index.html

The final `index.html` will have this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Moving Squares - JavaScript Port</title>
  <style>
    /* Minimal CSS: center canvas and set background */
    body {
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #1a1a1a;
      font-family: sans-serif;
    }
    canvas {
      border: 2px solid #444;
      background-color: #1e1428;
    }
  </style>
</head>
<body>
  <canvas id="canvas" width="800" height="600"></canvas>
  
  <script>
    // ==================== SECTION 1: CONSTANTS & CONFIG ====================
    // Equivalent to Python global constants
    const WIDTH = 800;
    const HEIGHT = 600;
    const COLORS = [/* ... */];
    const FLEE_DISTANCE = 150;
    // ... etc ...
    
    // ==================== SECTION 2: UTILITY FUNCTIONS ====================
    // - createSquare()
    // - checkCollision()
    // - updateSpeedForSize()
    // - randomUniform()
    // - etc.
    
    // ==================== SECTION 3: INITIALIZATION ====================
    // - Get canvas & context
    // - Create initial squares array
    // - Set up event listeners
    
    // ==================== SECTION 4: MAIN GAME LOOP ====================
    // - requestAnimationFrame callback
    // - Per-frame: respawn, interaction, movement, rendering
    // - Delta time calculation
    
    // ==================== SECTION 5: EVENT LISTENERS ====================
    // - quit handler (if needed)
  </script>
</body>
</html>
```

---

## Implementation Checklist

### Phase 1: Setup & Primitives ✓ (Planning Only)
- [ ] Create `web/index.html` file structure
- [ ] Set up canvas and context
- [ ] Implement `createSquare()` function
- [ ] Implement `checkCollision()` function
- [ ] Implement `updateSpeedForSize()` function
- [ ] Verify color constants are converted to RGB strings

### Phase 2: Initialization ✓ (Planning Only)
- [ ] Initialize `squares` array from `POPULATION_MIX`
- [ ] Verify all squares have correct properties
- [ ] Test random distribution (position, velocity, color)

### Phase 3: Main Loop Structure ✓ (Planning Only)
- [ ] Set up `requestAnimationFrame()` callback
- [ ] Implement delta time calculation
- [ ] Verify FPS is approximately 60

### Phase 4: Game Logic ✓ (Planning Only)
- [ ] **Respawn System:** Age-based removal and creation
- [ ] **Collision Detection:** Check all pairs, mark eaten squares
- [ ] **Eating Mechanics:** Size growth with animation
- [ ] **Steering Behavior:** Flee from larger, chase smaller
- [ ] **Movement:** Apply velocity, handle random jitter
- [ ] **Screen Wrapping:** Handle off-screen positions

### Phase 5: Rendering ✓ (Planning Only)
- [ ] Clear frame with background color
- [ ] Draw trails (lines from history)
- [ ] Draw squares (with alpha fade at end of life)
- [ ] Draw FPS counter and square count

### Phase 6: Polish & Testing ✓ (Planning Only)
- [ ] Verify visual output matches Python version
- [ ] Compare simulation behavior (speeds, collisions, growth)
- [ ] Add JSDoc comments explaining Pygame equivalents
- [ ] Test responsiveness on different screen sizes
- [ ] Optimize canvas rendering (no unnecessary redraws)

### Phase 7: Educational Documentation ✓ (Planning Only)
- [ ] Add comments above major code sections
- [ ] Document function equivalencies
- [ ] Provide Pygame→Canvas API cross-reference in code

---

## Key Implementation Notes

### 1. **Data Structure & Naming**
- Use `camelCase` for JavaScript (e.g., `targetSize`, `growthTimer`)
- Keep logic and flow identical to Python original
- All property names map directly (with case conversion)

### 2. **Timing & Performance**
- `requestAnimationFrame()` is browser-synced (usually 60 FPS)
- Calculate `dt` from timestamp delta to handle variable frame times
- Target FPS counter should show ~60

### 3. **Collision Detection**
- AABB (Axis-Aligned Bounding Box) is sufficient
- No physics engine needed—simple Rect overlap check

### 4. **Color Representation**
- Python: tuple `(r, g, b)` with integers 0-255
- JavaScript: CSS string `'rgb(r, g, b)'` or `'rgb(r, g, b)'`
- Alpha: Use `ctx.globalAlpha = alpha / 255` before drawing

### 5. **Canvas Context API Summary**
- **Clearing:** `ctx.fillRect(0, 0, WIDTH, HEIGHT)` with `fillStyle` set
- **Rectangles:** `ctx.fillRect(x, y, w, h)`
- **Lines:** `ctx.moveTo()`, `ctx.lineTo()`, `ctx.stroke()`
- **Text:** `ctx.font`, `ctx.fillText()`
- **Transparency:** `ctx.globalAlpha = value` (0-1)

### 6. **Avoiding Common Pitfalls**
- Don't forget to reset `ctx.globalAlpha = 1.0` after drawing transparent shapes
- Use `Math.round()` for pixel-perfect positioning
- Ensure `lastTimestamp` is defined before using in dt calculation
- Keep trail history trimmed to `TRAILS_LENGTH` to prevent memory leaks

---

## Expected Behavior Matching

### Python → JavaScript Equivalence Table

| Feature | Python Code | JavaScript Code | Status |
|---------|-------------|-----------------|--------|
| **Initialization** | `pygame.init()` + display setup | Canvas context creation | Ready to implement |
| **Main Loop** | `while running: ... clock.tick(60)` | `requestAnimationFrame()` with dt | Ready to implement |
| **Events** | `pygame.event.get()` loop | `addEventListener()` (quit only) | Ready to implement |
| **Respawning** | Age check, remove, recreate | Same logic, same vars | Ready to implement |
| **Collisions** | `pygame.Rect.colliderect()` | AABB overlap check | Ready to implement |
| **Steering** | Distance check + steering calc | Identical logic, camelCase | Ready to implement |
| **Movement** | Velocity + wrapping | Same velocity math, same wrapping | Ready to implement |
| **Growth Animation** | Linear interpolation over time | Identical interpolation logic | Ready to implement |
| **Rendering** | `pygame.draw.*` methods | Canvas context methods | Ready to implement |
| **Text** | `font.render()` + `screen.blit()` | `ctx.fillText()` | Ready to implement |
| **Trails** | `pygame.draw.lines()` from history | Canvas `moveTo/lineTo` loop | Ready to implement |
| **Alpha Blending** | `pygame.SRCALPHA` surface | `ctx.globalAlpha` | Ready to implement |

---

## Summary

This port maintains **complete logical parity** with the original Python/Pygame implementation:

✓ All classes and functions have 1-to-1 equivalents  
✓ Data structures map directly (lists→arrays, dicts→objects)  
✓ Simulation loop replaces pygame event loop with `requestAnimationFrame()`  
✓ Graphics API (Canvas CanvasRenderingContext2D) replaces pygame.draw  
✓ Delta time calculation mirrors `clock.tick(60) / 1000`  
✓ Self-contained in one `index.html` file  
✓ JSDoc comments explain Pygame equivalents for educational value  

**No refactoring, bug fixes, or architectural changes** are planned—the JavaScript version will faithfully reproduce the Python behavior in the browser.

---

**Next Steps:**  
When ready to implement, follow the Phase-by-phase checklist starting with Phase 1 (Setup & Primitives). Each phase builds on the previous one, ensuring the simulation is correct before adding rendering complexity.
