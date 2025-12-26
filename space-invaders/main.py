import turtle
import random
import time

# ─── CONFIG ────────────────────────────────────────────────────────
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 700
PLAYER_SPEED  = 20
BULLET_SPEED  = 20
ENEMY_SPEED   = 2
ENEMY_DROP    = 40
NUM_ENEMIES   = 5
BARRIER_COUNT = 3
# ────────────────────────────────────────────────────────────────────


# ─── SETUP SCREEN ──────────────────────────────────────────────────
wn = turtle.Screen()
wn.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
wn.title("Space Invaders")
wn.bgcolor("black")
wn.tracer(0)

# ─── PLAYER ────────────────────────────────────────────────────────
player = turtle.Turtle("triangle")
player.color("white")
player.penup()
player.setheading(90)
player.goto(0, -SCREEN_HEIGHT//2 + 50)

# ─── BULLET ───────────────────────────────────────────────────────
bullet = turtle.Turtle("square")
bullet.color("yellow")
bullet.shapesize(stretch_wid=0.2, stretch_len=0.6)
bullet.penup()
bullet.hideturtle()
bullet_state = "ready"  # "ready" or "fire"

# ─── ENEMIES ─────────────────────────────────────────────────────
enemies = []
start_x = -200
start_y = 250
for i in range(NUM_ENEMIES):
    enemy = turtle.Turtle("square")
    enemy.color("green")
    enemy.penup()
    enemy.goto(start_x + i*80, start_y)
    enemies.append(enemy)

enemy_dx = ENEMY_SPEED

# ─── BARRIERS ────────────────────────────────────────────────────
barrier_segments = []
for b in range(BARRIER_COUNT):
    bx = -200 + b*200
    by = -100
    for i in range(-40, 60, 20):
        seg = turtle.Turtle("square")
        seg.color("blue")
        seg.shapesize(0.5, 1)
        seg.penup()
        seg.goto(bx + i, by)
        barrier_segments.append(seg)

# ─── MOVEMENT FUNCTIONS ───────────────────────────────────────────
def move_left():
    x = player.xcor() - PLAYER_SPEED
    if x < -SCREEN_WIDTH//2 + 20:
        x = -SCREEN_WIDTH//2 + 20
    player.setx(x)

def move_right():
    x = player.xcor() + PLAYER_SPEED
    if x > SCREEN_WIDTH//2 - 20:
        x = SCREEN_WIDTH//2 - 20
    player.setx(x)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.setheading(90)
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

# ─── KEY BINDINGS ─────────────────────────────────────────────────
wn.listen()
wn.onkey(move_left, "Left")
wn.onkey(move_right, "Right")
wn.onkey(fire_bullet, "space")

# ─── COLLISION DETECTION ──────────────────────────────────────────
def is_collision(t1, t2, tol=20):
    return t1.distance(t2) < tol

# ─── MAIN GAME LOOP ───────────────────────────────────────────────
def game_loop():
    global enemy_dx, bullet_state

    # Move enemiesndu open we have
    reverse = False
    for e in enemies:
        e.setx(e.xcor() + enemy_dx)
        # if any enemy hits side wall, flag to reverse
        if e.xcor() > SCREEN_WIDTH//2 - 20 or e.xcor() < -SCREEN_WIDTH//2 + 20:
            reverse = True

    # If we need to reverse, move all enemies down
    if reverse:
        enemy_dx *= -1
        for e in enemies:
            e.sety(e.ycor() - ENEMY_DROP)

    # Move bullet
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + BULLET_SPEED)
        # Bullet goes off screen
        if bullet.ycor() > SCREEN_HEIGHT//2:
            bullet.hideturtle()
            bullet_state = "ready"

    # Check for bullet-enemy collisions
    for e in enemies:
        if bullet_state == "fire" and is_collision(bullet, e):
            # Reset bullet
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.goto(0, -SCREEN_HEIGHT)
            # Respawn or hide enemy
            e.goto(1000, 1000)  # off-screen
            enemies.remove(e)
            break

    # Check for enemy-barrier collisions
    for seg in barrier_segments:
        for e in enemies:
            if is_collision(e, seg, tol=15):
                # barrier is destroyed
                seg.hideturtle()
                barrier_segments.remove(seg)
                break

    # Check for enemy-player collisions or enemies reaching bottom
    for e in enemies:
        if is_collision(e, player, tol=20) or e.ycor() < player.ycor():
            player.hideturtle()
            e.hideturtle()
            wn.update()
            print("GAME OVER")
            return  # stop the loop

    wn.update()
    wn.ontimer(game_loop, 50)  # run again after 50ms

# start the loop
game_loop()
wn.mainloop()
