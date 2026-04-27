# Light Refactoring Plan: Pygame Squares Animation
**For First-Year Computer Science Students**

---

## 1. Overview

### Code Summary
The program is a pygame-based animation with ~200 lines of Python that:
- Creates 15 moving squares with AI steering (chase/flee)
- Handles physics (velocity, wall bouncing, damping)
- Manages entity lifecycle (respawning after 12-18 seconds)
- Renders with transparency fade effects at 60 FPS

### Current State Assessment
**Strengths:**
- Well-commented with clear section headers
- Good use of dictionaries for entity data
- Proper time-based delta updates

**Areas for Improvement:**
1. **Code Duplication:** Square creation appears twice (lines 33-57 and 86-97) with nearly identical logic
2. **Magic Numbers:** Constants like `15, 80, 30, 150, 0.05, 0.9, 2, 0.02` scattered throughout code, making parameters hard to tune
3. **Repeated Calculations:** Distance/magnitude calculations and vector normalization repeated in multiple places
4. **Mixed Responsibilities:** Main loop handles initialization, updates, and rendering all at once (unclear flow)
5. **Wall Bounce Duplication:** Similar collision logic for left/right/top/bottom walls (repetitive)

---

## 2. Refactoring Goals

1. **Eliminate Duplication** → Extract square creation into reusable function
2. **Extract Constants** → Move magic numbers to top-level configuration
3. **Improve Clarity** → Extract complex logic into well-named helper functions
4. **Maintain Behavior** → All refactoring preserves existing game mechanics
5. **Beginner-Friendly** → Use only functions, no classes or advanced patterns

---

## 3. Step-by-Step Refactoring Plan

### **STEP 1: Extract Magic Numbers to Configuration Constants**

**What to do:**
- Create a new `CONFIG` dictionary at the top (after imports, before pygame.init())
- Move all numeric constants into this dictionary with clear names
- Replace scattered magic numbers with `CONFIG['key']` references

**Why this helps:**
- Makes game parameters easy to find and tune
- Teaches the DRY principle (Don't Repeat Yourself)
- Reduces errors from inconsistent values
- Single source of truth for game settings

**Before-After Example:**
```python
# BEFORE: Magic numbers scattered
speed = (30 / size) * 150
if random.random() < 0.02:
    s['vel'][0] += random.uniform(-10, 10)
    
# AFTER: Clear references
speed = (CONFIG['SIZE_FACTOR'] / size) * CONFIG['BASE_SPEED']
if random.random() < CONFIG['WANDER_CHANCE']:
    s['vel'][0] += random.uniform(-CONFIG['WANDER_FORCE'], CONFIG['WANDER_FORCE'])
```

**Constants to extract:**
- `15` (NUM_SQUARES) → already a constant, but could move to CONFIG
- `80` (max size) → CONFIG['MAX_SIZE']
- `15` (min size) → CONFIG['MIN_SIZE']
- `30, 150` (speed formula) → CONFIG['SIZE_FACTOR'], CONFIG['BASE_SPEED']
- `150` (FLEE_DISTANCE) → already named
- `0.05` (STEER_FORCE) → already named
- `0.9` (BOUNCE_DAMPING) → already named
- `2` (fade time window) → CONFIG['FADE_TIME_WINDOW']
- `0.02` (wander chance) → CONFIG['WANDER_CHANCE']
- `10` (wander force) → CONFIG['WANDER_FORCE']
- `12, 18` (lifespan range) → CONFIG['MIN_LIFESPAN'], CONFIG['MAX_LIFESPAN']
- `(200, 200, 200)` (UI text color) → CONFIG['UI_COLOR']

**Inline comment to add:**
"# Centralized game constants for easy tuning. Gathering all magic numbers here makes parameter adjustments quick and prevents inconsistencies across the code."

---

### **STEP 2: Create `create_square()` Function**

**What to do:**
- Extract the square creation logic (lines 35-57) into a function called `create_square(x=None, y=None)`
- If x/y are None, generate random positions (for initialization)
- If x/y provided, use them (for respawning at specific location)
- Return the square dictionary

**Why this helps:**
- Eliminates code duplication (creation code appears twice)
- Makes adding new squares easier
- Teaches function extraction and parameterization
- Bug fix area: ensures consistency between initial and respawned squares

**Before-After:**
```python
# BEFORE: Repeated in two places
for _ in range(NUM_SQUARES):
    size = random.randint(15, 80)
    color = random.choice(COLORS)
    x = random.uniform(0, WIDTH - size)
    y = random.uniform(0, HEIGHT - size)
    # ... 12 more lines ...
    squares.append({...})

# And again in respawn:
new_size = random.randint(15, 80)
new_speed = (30 / new_size) * 150
# ... similar logic ...
squares.append({...})

# AFTER: Single source
def create_square(x=None, y=None):
    size = random.randint(CONFIG['MIN_SIZE'], CONFIG['MAX_SIZE'])
    color = random.choice(COLORS)
    
    if x is None or y is None:
        x = random.uniform(0, WIDTH - size)
        y = random.uniform(0, HEIGHT - size)
    
    speed = (CONFIG['SIZE_FACTOR'] / size) * CONFIG['BASE_SPEED']
    angle = random.uniform(0, 2 * math.pi)
    
    return {
        'pos': [x, y],
        'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
        'size': size,
        'color': color,
        'birth': time.time(),
        'life': random.uniform(CONFIG['MIN_LIFESPAN'], CONFIG['MAX_LIFESPAN']),
        'max_speed': speed
    }

# Usage:
squares = [create_square() for _ in range(NUM_SQUARES)]
# And in respawn:
squares.append(create_square())
```

**Inline comments to add:**
- "# Unified square creation reduces duplication and ensures consistent properties"
- "# Parameterized coordinates allow both random initialization and specific respawning"

---

### **STEP 3: Create `calculate_distance_between_centers()` Function**

**What to do:**
- Extract the center calculation and distance computation into helper function
- Takes two squares as parameters
- Returns distance (float)
- Creates reusable logic for any distance-based interaction

**Why this helps:**
- Reduces repeated math operations
- Makes distance checks more readable
- Easier to debug or add distance-based features later
- Teaches helper functions for clarity

**Before-After:**
```python
# BEFORE: Inline calculation
c1 = [s1['pos'][0] + s1['size']/2, s1['pos'][1] + s1['size']/2]
c2 = [s2['pos'][0] + s2['size']/2, s2['pos'][1] + s2['size']/2]
dx, dy = c2[0] - c1[0], c2[1] - c1[1]
dist = math.hypot(dx, dy)

# AFTER: Clear function
def calculate_distance_between_centers(square1, square2):
    # Get center of each square (top-left + half-size)
    center1 = [square1['pos'][0] + square1['size']/2, 
               square1['pos'][1] + square1['size']/2]
    center2 = [square2['pos'][0] + square2['size']/2, 
               square2['pos'][1] + square2['size']/2]
    
    # Pythagorean distance
    dx = center2[0] - center1[0]
    dy = center2[1] - center1[1]
    return math.hypot(dx, dy)

# Usage:
dist = calculate_distance_between_centers(s1, s2)
```

**Inline comments to add:**
- "# Encapsulates center calculation for reusability and clarity"
- "# Using hypot handles vector magnitude calculation accurately"

---

### **STEP 4: Create `apply_wall_collisions()` Function**

**What to do:**
- Extract wall bounce logic (lines 168-183) into a function
- Takes a square and returns the modified square (updated in-place)
- Combines all four wall checks into one organized function

**Why this helps:**
- Reduces code repetition (left/right/top/bottom are similar)
- Makes physics easier to understand at a glance
- Easier to add new collision features (particles, sounds, etc.)
- Teaches function extraction for repeated patterns

**Before-After:**
```python
# BEFORE: Repeated for each wall
if s['pos'][0] <= 0:
    s['pos'][0] = 0
    s['vel'][0] = abs(s['vel'][0]) * BOUNCE_DAMPING
elif s['pos'][0] + s['size'] >= WIDTH:
    s['pos'][0] = WIDTH - s['size']
    s['vel'][0] = -abs(s['vel'][0]) * BOUNCE_DAMPING

if s['pos'][1] <= 0:
    s['pos'][1] = 0
    s['vel'][1] = abs(s['vel'][1]) * BOUNCE_DAMPING
elif s['pos'][1] + s['size'] >= HEIGHT:
    s['pos'][1] = HEIGHT - s['size']
    s['vel'][1] = -abs(s['vel'][1]) * BOUNCE_DAMPING

# AFTER: Unified function
def apply_wall_collisions(square):
    # Horizontal (left/right) wall collisions
    if square['pos'][0] <= 0:
        square['pos'][0] = 0
        square['vel'][0] = abs(square['vel'][0]) * CONFIG['BOUNCE_DAMPING']
    elif square['pos'][0] + square['size'] >= WIDTH:
        square['pos'][0] = WIDTH - square['size']
        square['vel'][0] = -abs(square['vel'][0]) * CONFIG['BOUNCE_DAMPING']
    
    # Vertical (top/bottom) wall collisions
    if square['pos'][1] <= 0:
        square['pos'][1] = 0
        square['vel'][1] = abs(square['vel'][1]) * CONFIG['BOUNCE_DAMPING']
    elif square['pos'][1] + square['size'] >= HEIGHT:
        square['pos'][1] = HEIGHT - square['size']
        square['vel'][1] = -abs(square['vel'][1]) * CONFIG['BOUNCE_DAMPING']

# Usage:
apply_wall_collisions(s)
```

**Inline comments to add:**
- "# Consolidates collision logic for all walls; easier to debug and modify"
- "# Damping reduces velocity to simulate energy loss on impact"

---

### **STEP 5: Create `normalize_vector()` Function**

**What to do:**
- Extract vector normalization logic into reusable function
- Takes (x, y) components, returns normalized (x, y)
- Safely handles zero-magnitude vectors to prevent division by zero

**Why this helps:**
- Used twice in interaction system (steering + direction)
- Prevents bugs from forgetting magnitude check
- Teaches vector math encapsulation
- Prevents potential divide-by-zero errors

**Before-After:**
```python
# BEFORE: Repeated twice with magic numbers
nx, ny = dx / dist, dy / dist  # Line 115
# ...later...
mag = math.hypot(steer_x, steer_y)
steer_x, steer_y = steer_x / mag, steer_y / mag  # Line 124

# AFTER: Safe, reusable function
def normalize_vector(x, y):
    # Avoid division by zero when vector is zero
    mag = math.hypot(x, y)
    if mag == 0:
        return 0, 0  # Zero vector stays zero
    return x / mag, y / mag

# Usage:
nx, ny = normalize_vector(dx, dy)
# Later:
steer_x, steer_y = normalize_vector(steer_x, steer_y)
```

**Inline comments to add:**
- "# Ensures vectors always have magnitude 1 (except zero vector)"
- "# Prevents crashes from dividing by zero when magnitude is 0"

---

### **STEP 6: Create `calculate_alpha()` Function**

**What to do:**
- Extract fade calculation (lines 186-189) into function
- Takes (age, lifespan) and returns alpha value (0-255)
- Encapsulates the fade logic in one place

**Why this helps:**
- Clarifies the fade math in one readable place
- Easier to adjust fade duration
- Teaches how to extract math logic
- Reduces visual rendering complexity

**Before-After:**
```python
# BEFORE: Inline calculation
alpha = 255
if age > s['life'] - 2:
    alpha = int(255 * (s['life'] - age) / 2)
    alpha = max(0, alpha)

# AFTER: Clear function
def calculate_alpha(age, lifespan):
    # Fade only during last FADE_TIME_WINDOW seconds
    fade_window = CONFIG['FADE_TIME_WINDOW']
    if age > lifespan - fade_window:
        # Linear interpolation from 255 to 0
        alpha = int(255 * (lifespan - age) / fade_window)
        return max(0, alpha)  # Clamp to prevent negative
    return 255  # Fully opaque

# Usage:
alpha = calculate_alpha(age, s['life'])
```

**Inline comments to add:**
- "# Calculates transparency for fade-out effect near end of life"
- "# Clamping ensures alpha stays in valid range [0, 255]"

---

### **STEP 7: Extract Steering Force Logic (Optional Advanced)**

**What to do:**
- Extract the chase/flee decision and steering accumulation into `apply_steering_force()`
- Takes s1, s2 and modifies s1's steering accumulators
- Clarifies the AI logic (this is the most complex part)

**Why this helps:**
- Encapsulates the "hardest to understand" part of the code
- Makes chase vs flee decision explicit
- Easier to debug AI behavior or add variations
- Teaches extracting complex logic

**Note:** This can be optional for a first pass, but recommended for clarity.

---

## 4. Final Output Requirements (Mandatory)

When this refactoring plan is executed, the final refactored code **MUST**:

### ✓ Structure
- Place all imports at top
- Add CONFIG dictionary with all magic numbers extracted
- Define all helper functions (Steps 1-7) before the main loop
- Keep main game loop mostly unchanged, but calling helper functions

### ✓ Comments Requirements
Every refactoring change **MUST include inline comments explaining:**

1. **What changed:** 
   - e.g., "# Extracted from duplicated initialization code"
   
2. **Why it improves the code:**
   - e.g., "# Function eliminates 60 lines of duplication; changes in one place now affect both creation and respawn"
   
3. **Relevant programming concepts:**
   - e.g., "# DRY Principle: Don't Repeat Yourself. Reduces bugs from inconsistent updates."
   - e.g., "# Function Extraction: Moving related code into named functions improves readability"
   - e.g., "# Vector normalization: Ensures consistent direction magnitude (length = 1)"

### ✓ Code Quality
- All functions have docstrings explaining parameters and return values
- Variable names are clear (avoid single letters except for x, y, dx, dy, i, j)
- Logic is grouped by responsibility (math → physics → rendering)
- Game behavior is identical to original (no logic changes, only reorganization)

### ✓ Output Format
- Save as a new Python file named `main_refactored.py`
- Include at least 15 inline comments explaining improvements
- Code should be ~250-280 lines (slightly longer due to comments, but more readable)
- Keep original `main.py` unchanged for comparison

---

## 5. Key Concepts for Students

### **DRY Principle (Don't Repeat Yourself)**
When code appears in multiple places, small bug fixes become time-consuming. By extracting duplicated logic into functions, you only need to update one place.

**Example:** Square creation appears twice. If you want to change how squares spawn, without a function you must edit two places (and likely forget one!).

### **Function Extraction**
Breaking large problems into smaller named functions makes code:
- **Easier to read:** Function names describe what code does
- **Easier to test:** Each function can be tested independently
- **Easier to reuse:** Need to create a square? Just call `create_square()`

### **Magic Numbers vs Named Constants**
```python
# ❌ Magic numbers (confusing)
if age > life - 2:
    alpha = int(255 * (life - age) / 2)

# ✓ Named constants (clear)
FADE_WINDOW = 2  # seconds
alpha = int(255 * (life - age) / FADE_WINDOW)
```

### **Vector Operations**
- **Normalization:** Scaling a vector to length 1 while preserving direction
- **Magnitude:** The "length" of a vector; calculated with Pythagorean theorem
- **Important:** Always check for zero-magnitude vectors before dividing

### **Separation of Concerns**
Each function should have one clear responsibility:
- `create_square()` → Creates squares
- `apply_wall_collisions()` → Handles bouncing
- `normalize_vector()` → Normalizes vectors

This makes code modular and easier to extend.

---

## 6. Safety Notes

⚠️ **Testing is Critical**

1. **Run the refactored code and verify:**
   - Squares still spawn and respawn correctly
   - Chase/flee behavior unchanged
   - Wall bouncing works (energy loss visible)
   - Fade effect still appears
   - FPS counter still displays

2. **Parameter tuning:** After refactoring, the CONFIG dictionary makes experimentation easier:
   - Try `NUM_SQUARES = 30` (watch for performance drop)
   - Try `STEER_FORCE = 0.2` (faster steering)
   - Try `BOUNCE_DAMPING = 0.5` (bouncier squares)

3. **Edge cases to check:**
   - Do squares still respawn after 12-18 seconds?
   - Do fade effects work (squares should vanish smoothly)?
   - Do squares still interact within 150 pixels of each other?

4. **Preserve behavior:**
   - This refactoring reorganizes code, not logic
   - If the refactored code behaves differently, you've introduced a bug (revert that change)
   - Use the original `main.py` as a reference

5. **Common mistakes to avoid:**
   - Don't change the order of operations in the main loop
   - Don't modify how entity dictionaries store data (keys must match)
   - Don't alter the pygame initialization or display logic
   - Test after each step, not just at the end

---

## Summary

This refactoring is **beginner-appropriate** because it:
- ✅ Uses only functions (no classes)
- ✅ Improves readability dramatically
- ✅ Eliminates ~60 lines of duplication
- ✅ Extracts magic numbers for easy tuning
- ✅ Teaches DRY, separation of concerns, and function design
- ✅ Preserves all original game behavior

**Expected outcome:** ~250 lines of cleaner, more maintainable code that's easier to debug, extend, and understand.
