# Pygame Squares Animation - Architecture Documentation

## Overview
A pygame-based animation system featuring multiple moving squares with AI-driven behavior (fleeing and chasing), lifespan management, physics simulation, and wall collisions. The program runs at 60 FPS with real-time rendering.

---

## 1. Module Dependency Graph

```mermaid
graph TB
    PY["Python Standard Library"]
    PYGAME["pygame (External)"]
    MATH["math (Standard)"]
    RANDOM["random (Standard)"]
    TIME["time (Standard)"]
    
    MAIN["main.py<br/>(Primary Game Loop)"]
    
    FLEEING["fleeingfeature.py<br/>(Archive)"]
    LIFESPAN["lifespan.py<br/>(Archive)"]
    
    PY --> MAIN
    PYGAME --> MAIN
    MATH --> MAIN
    RANDOM --> MAIN
    TIME --> MAIN
    
    style MAIN fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff
    style FLEEING fill:#FFA726,stroke:#333,stroke-width:1px,color:#fff
    style LIFESPAN fill:#FFA726,stroke:#333,stroke-width:1px,color:#fff
    style PYGAME fill:#42A5F5,stroke:#333,stroke-width:2px,color:#fff
```

---

## 2. High-Level System Architecture

```mermaid
graph LR
    INPUT["Input Handler<br/>(Events)"]
    SPAWN["Spawn/Respawn<br/>System"]
    INTERACT["Interaction<br/>System<br/>(AI)"]
    PHYSICS["Physics Engine<br/>(Movement &<br/>Collisions)"]
    RENDER["Rendering<br/>System"]
    STATE["Game State<br/>(Squares List)"]
    
    INPUT --> STATE
    SPAWN --> STATE
    INTERACT --> STATE
    PHYSICS --> STATE
    STATE --> RENDER
    
    style INPUT fill:#FF6B6B,stroke:#333,stroke-width:2px,color:#fff
    style SPAWN fill:#4ECDC4,stroke:#333,stroke-width:2px,color:#fff
    style INTERACT fill:#95E1D3,stroke:#333,stroke-width:2px,color:#fff
    style PHYSICS fill:#F38181,stroke:#333,stroke-width:2px,color:#fff
    style RENDER fill:#AA96DA,stroke:#333,stroke-width:2px,color:#fff
    style STATE fill:#FCBAD3,stroke:#333,stroke-width:2px,color:#000
```

---

## 3. Square Data Structure

Each square in the `squares` list is a dictionary containing:

```mermaid
graph TD
    SQUARE["Square Entity"]
    POS["pos: list[x, y]<br/>(top-left corner)"]
    VEL["vel: list[dx, dy]<br/>(velocity vector)"]
    SIZE["size: int<br/>(pixels)"]
    COLOR["color: tuple<br/>(RGB)"]
    BIRTH["birth: float<br/>(spawn timestamp)"]
    LIFE["life: float<br/>(lifespan seconds)"]
    MAXSPEED["max_speed: float<br/>(normalized speed)"]
    
    SQUARE --> POS
    SQUARE --> VEL
    SQUARE --> SIZE
    SQUARE --> COLOR
    SQUARE --> BIRTH
    SQUARE --> LIFE
    SQUARE --> MAXSPEED
    
    style SQUARE fill:#FF6B6B,stroke:#333,stroke-width:2px,color:#fff
```

---

## 4. Main Game Loop Execution Flow

```mermaid
graph TD
    START["🎮 Start Game<br/>Initialize pygame<br/>Create squares"]
    CLOCK["Set Frame Rate<br/>60 FPS"]
    LOOP_START["Frame Loop"]
    DT["Calculate Delta Time<br/>dt = elapsed ms / 1000"]
    CLEAR["Clear Screen<br/>Fill bg color"]
    EVENTS["Process Events<br/>Check for QUIT"]
    RESPAWN["Respawn System<br/>Replace expired squares"]
    INTERACT["Interaction System<br/>Compute steering forces<br/>Update velocities"]
    MOVEMENT["Movement System<br/>Apply velocity to position<br/>Add random wander"]
    COLLISION["Collision Detection<br/>Bounce off walls<br/>Apply damping"]
    ALPHA["Calculate Alpha<br/>Fade out effect"]
    DRAW["Draw Squares<br/>with transparency"]
    UI["Render UI<br/>FPS counter"]
    DISPLAY["Update Display<br/>pygame.display.flip"]
    END_LOOP{">60 FPS<br/>elapsed?"}
    QUIT{"User quit?"}
    END["🛑 Exit<br/>pygame.quit()"]
    
    START --> CLOCK
    CLOCK --> LOOP_START
    LOOP_START --> DT
    DT --> CLEAR
    CLEAR --> EVENTS
    EVENTS --> RESPAWN
    RESPAWN --> INTERACT
    INTERACT --> MOVEMENT
    MOVEMENT --> COLLISION
    COLLISION --> ALPHA
    ALPHA --> DRAW
    DRAW --> UI
    UI --> DISPLAY
    DISPLAY --> END_LOOP
    END_LOOP -->|Wait for frame| LOOP_START
    EVENTS --> QUIT
    QUIT -->|Yes| END
    QUIT -->|No| RESPAWN
    
    style START fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff
    style END fill:#F44336,stroke:#333,stroke-width:2px,color:#fff
    style INTERACT fill:#95E1D3,stroke:#333,stroke-width:2px,color:#000
    style COLLISION fill:#F38181,stroke:#333,stroke-width:2px,color:#fff
```

---

## 5. Interaction System (AI Steering)

The AI behavior determines how squares move relative to each other based on size comparison.

```mermaid
graph TD
    ITER_START["For each square s1"]
    GET_CENTER["Get center position<br/>of s1"]
    STEER_INIT["Initialize<br/>steer_x = 0<br/>steer_y = 0"]
    
    ITER_OTHER["For each other square s2"]
    SKIP{">Same square?"}
    GET_CENTER2["Get center position<br/>of s2"]
    CALC_DIST["Calculate distance<br/>between s1 and s2"]
    CHECK_DIST{">Distance <br/>FLEE_DISTANCE<br/>(150px)?"}
    
    NORM_DIR["Normalize direction vector<br/>from s1 to s2"]
    SIZE_CHECK{">s1.size ><br/>s2.size?"}
    CHASE["Chase:<br/>steer += direction<br/>(move toward)"]
    FLEE["Flee:<br/>steer -= direction<br/>(move away)"]
    
    APPLY_STEER["Normalize steering vector<br/>mag = hypot(steer_x, steer_y)"]
    BLEND["Blend steering into velocity<br/>vel += (steer_norm * max_speed - vel) *<br/>STEER_FORCE (0.05)"]
    
    ITER_START --> GET_CENTER
    GET_CENTER --> STEER_INIT
    STEER_INIT --> ITER_OTHER
    ITER_OTHER --> SKIP
    SKIP -->|Yes| ITER_OTHER
    SKIP -->|No| GET_CENTER2
    GET_CENTER2 --> CALC_DIST
    CALC_DIST --> CHECK_DIST
    CHECK_DIST -->|No| ITER_OTHER
    CHECK_DIST -->|Yes| NORM_DIR
    NORM_DIR --> SIZE_CHECK
    SIZE_CHECK -->|Yes| CHASE
    SIZE_CHECK -->|No| FLEE
    CHASE --> ITER_OTHER
    FLEE --> ITER_OTHER
    ITER_OTHER -->|No more| APPLY_STEER
    APPLY_STEER --> BLEND
    
    style CHASE fill:#FF6B6B,stroke:#333,stroke-width:2px,color:#fff
    style FLEE fill:#4ECDC4,stroke:#333,stroke-width:2px,color:#fff
    style INTERACT fill:#95E1D3,stroke:#333,stroke-width:2px,color:#000
```

---

## 6. Physics System (Collision & Movement)

```mermaid
graph TD
    FOR_EACH["For each square"]
    
    WANDER["Random Wandering<br/>2% chance<br/>vel += random(-10, 10)"]
    
    UPDATE_POS["Update Position<br/>pos += vel * dt"]
    
    BOUND_LEFT{">pos.x <= 0?"}
    BOUNCE_LEFT["Bounce Left Wall:<br/>pos.x = 0<br/>vel.x = abs(vel.x) *<br/>BOUNCE_DAMPING (0.9)"]
    
    BOUND_RIGHT{">pos.x + size<br/>>= WIDTH?"}
    BOUNCE_RIGHT["Bounce Right Wall:<br/>pos.x = WIDTH - size<br/>vel.x = -abs(vel.x) *<br/>BOUNCE_DAMPING"]
    
    BOUND_TOP{">pos.y <= 0?"}
    BOUNCE_TOP["Bounce Top Wall:<br/>pos.y = 0<br/>vel.y = abs(vel.y) *<br/>BOUNCE_DAMPING"]
    
    BOUND_BOTTOM{">pos.y + size<br/>>= HEIGHT?"}
    BOUNCE_BOTTOM["Bounce Bottom Wall:<br/>pos.y = HEIGHT - size<br/>vel.y = -abs(vel.y) *<br/>BOUNCE_DAMPING"]
    
    FOR_EACH --> WANDER
    WANDER --> UPDATE_POS
    UPDATE_POS --> BOUND_LEFT
    BOUND_LEFT -->|Yes| BOUNCE_LEFT
    BOUND_LEFT -->|No| BOUND_RIGHT
    BOUNCE_LEFT --> BOUND_RIGHT
    BOUND_RIGHT -->|Yes| BOUNCE_RIGHT
    BOUND_RIGHT -->|No| BOUND_TOP
    BOUNCE_RIGHT --> BOUND_TOP
    BOUND_TOP -->|Yes| BOUNCE_TOP
    BOUND_TOP -->|No| BOUND_BOTTOM
    BOUNCE_TOP --> BOUND_BOTTOM
    BOUND_BOTTOM -->|Yes| BOUNCE_BOTTOM
    
    style WANDER fill:#FFE082,stroke:#333,stroke-width:2px,color:#000
    style BOUNCE_LEFT fill:#F38181,stroke:#333,stroke-width:2px,color:#fff
    style BOUNCE_RIGHT fill:#F38181,stroke:#333,stroke-width:2px,color:#fff
    style BOUNCE_TOP fill:#F38181,stroke:#333,stroke-width:2px,color:#fff
    style BOUNCE_BOTTOM fill:#F38181,stroke:#333,stroke-width:2px,color:#fff
```

---

## 7. Lifespan & Respawn System

```mermaid
graph TD
    NOW["Get current time<br/>now = time.time()"]
    FOR_SQUARE["For each square"]
    
    CALC_AGE["Calculate age<br/>age = now - birth_time"]
    CHECK_LIFE{">age >=<br/>lifespan?"}
    
    REMOVE["Remove old square<br/>from list"]
    
    CREATE_NEW["Create new square:<br/>• Random size: 15-80 px<br/>• Random color<br/>• Random position<br/>• Random angle<br/>• Calculate speed"]
    
    APPEND["Append new square<br/>to list"]
    
    NOW --> FOR_SQUARE
    FOR_SQUARE --> CALC_AGE
    CALC_AGE --> CHECK_LIFE
    CHECK_LIFE -->|Yes| REMOVE
    CHECK_LIFE -->|No| FOR_SQUARE
    REMOVE --> CREATE_NEW
    CREATE_NEW --> APPEND
    APPEND --> FOR_SQUARE
    
    style REMOVE fill:#F44336,stroke:#333,stroke-width:2px,color:#fff
    style CREATE_NEW fill:#4ECDC4,stroke:#333,stroke-width:2px,color:#fff
```

---

## 8. Rendering Pipeline

```mermaid
graph TD
    FOR_SQUARE["For each square"]
    
    CALC_AGE["Calculate age<br/>age = now - birth_time"]
    
    CHECK_FADE{">age > lifespan - 2?"}
    ALPHA_FULL["alpha = 255<br/>(fully opaque)"]
    ALPHA_FADE["Calculate fade:<br/>alpha = 255 * (life - age) / 2<br/>Clamp to [0, 255]"]
    
    CREATE_SURF["Create surface<br/>pygame.Surface<br/>(size x size)<br/>with alpha channel"]
    
    FILL_COLOR["Fill surface<br/>with (r, g, b, alpha)"]
    
    BLIT["Blit to screen<br/>at (x, y)"]
    
    FOR_SQUARE --> CALC_AGE
    CALC_AGE --> CHECK_FADE
    CHECK_FADE -->|No| ALPHA_FULL
    CHECK_FADE -->|Yes| ALPHA_FADE
    ALPHA_FULL --> CREATE_SURF
    ALPHA_FADE --> CREATE_SURF
    CREATE_SURF --> FILL_COLOR
    FILL_COLOR --> BLIT
    
    style ALPHA_FADE fill:#FFE082,stroke:#333,stroke-width:2px,color:#000
    style BLIT fill:#AA96DA,stroke:#333,stroke-width:2px,color:#fff
```

---

## 9. Key Configuration Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| `NUM_SQUARES` | 15 | Initial number of squares |
| `FLEE_DISTANCE` | 150 px | Distance at which squares react |
| `STEER_FORCE` | 0.05 | Steering intensity (0-1 blend factor) |
| `BOUNCE_DAMPING` | 0.9 | Energy retained after wall collision |
| `COLORS` | RGB tuples | 4 available colors for squares |
| `WIDTH, HEIGHT` | 800, 600 | Screen dimensions |
| `Target FPS` | 60 | Frame rate (clock.tick) |
| `Size range` | 15-80 px | Square size randomization |
| `Lifespan range` | 12-18 s | Square lifetime before respawn |

---

## 10. Entry Point & Initialization

**File:** `main.py`

**Initialization Sequence:**
1. Import libraries: `pygame`, `random`, `math`, `time`
2. Initialize pygame: `pygame.init()`
3. Create display window (800x600)
4. Set window caption
5. Populate `squares` list with 15 randomly configured squares
6. Create game clock (60 FPS target)
7. Create font for UI
8. Enter main game loop

---

## 11. Data Flow Diagram

```mermaid
graph LR
    INPUT["👤 User Input<br/>(QUIT)"]
    CLOCK["⏱️ Clock<br/>(Frame Timing)"]
    
    RESPAWN["Respawn<br/>System"]
    AI["AI Steering<br/>System"]
    PHYSICS["Physics<br/>System"]
    RENDER["Render<br/>System"]
    
    STATE["🔄 Game State<br/>(Squares List)"]
    
    INPUT --> STATE
    CLOCK --> STATE
    STATE --> RESPAWN
    STATE --> AI
    STATE --> PHYSICS
    STATE --> RENDER
    RESPAWN --> STATE
    AI --> STATE
    PHYSICS --> STATE
    
    style STATE fill:#FCBAD3,stroke:#333,stroke-width:2px,color:#000
    style INPUT fill:#FF6B6B,stroke:#333,stroke-width:2px,color:#fff
    style CLOCK fill:#FFE082,stroke:#333,stroke-width:2px,color:#000
    style RESPAWN fill:#4ECDC4,stroke:#333,stroke-width:2px,color:#000
    style AI fill:#95E1D3,stroke:#333,stroke-width:2px,color:#000
    style PHYSICS fill:#F38181,stroke:#333,stroke-width:2px,color:#fff
    style RENDER fill:#AA96DA,stroke:#333,stroke-width:2px,color:#fff
```

---

## 12. Code Sections Breakdown

| Section | Location | Responsibility |
|---------|----------|-----------------|
| **Initialization** | Lines 1-55 | Pygame setup, square creation, constants |
| **Main Loop Setup** | Lines 56-62 | Game state & timing initialization |
| **Event Handling** | Lines 65-68 | Input and quit event processing |
| **Respawn System** | Lines 70-86 | Lifespan tracking and square replacement |
| **Interaction System** | Lines 88-131 | AI steering (chase/flee behavior) |
| **Movement & Physics** | Lines 133-173 | Velocity application, wall bouncing, damping |
| **Rendering** | Lines 175-193 | Square drawing with fade effect, UI text |
| **Display Update** | Line 195 | Frame buffer swap |
| **Cleanup** | Line 197 | Pygame shutdown |

---

## Summary

This pygame animation system demonstrates:
- **Object-oriented simulation** using dictionary-based entity storage
- **AI behavior** through steering forces and size-based interaction rules
- **Physics simulation** including velocity, collision detection, and damping
- **Lifespan management** with time-based entity respawning
- **Real-time rendering** with transparency and fade effects
- **Modular game loop** separating input, update, and render phases

The architecture is suitable for educational purposes and demonstrates fundamental game engine concepts in ~200 lines of Python.
