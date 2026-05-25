import turtle
import math
import random
import colorsys

# 1. Core Engine Configuration
WIDTH, HEIGHT = 800, 600
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("black")  
screen.title("University Engineering Project: Production-Ready Asteroids Engine")
screen.colormode(255)  
screen.tracer(0)      

NEON_PALETTE = [
    (255, 0, 255),    # Neon Magenta
    (0, 255, 255),    # Neon Cyan
    (255, 255, 0),    # Neon Yellow
    (57, 255, 20),    # Neon Lime Green
    (255, 111, 0),    # Neon Deep Orange
    (138, 43, 226)    # BlueViolet
]

# 2. Polymorphic Base Class
class Sprite(turtle.Turtle):
    def __init__(self, shape, color, x, y):
        super().__init__()
        self.penup()
        self.shape(shape)
        if isinstance(color, tuple):
            self.color(color[0], color[1], color[2])
        else:
            self.color(color)
        self.goto(x, y)
        self.dx = 0.0  
        self.dy = 0.0  
        self.radius = 15

    def move(self):
        new_x = self.xcor() + self.dx
        new_y = self.ycor() + self.dy
        
        if new_x > WIDTH // 2: new_x = -WIDTH // 2
        elif new_x < -WIDTH // 2: new_x = WIDTH // 2
        if new_y > HEIGHT // 2: new_y = -HEIGHT // 2
        elif new_y < -HEIGHT // 2: new_y = HEIGHT // 2
            
        self.goto(new_x, new_y)

    def is_colliding_with(self, other):
        return self.distance(other) < (self.radius + other.radius)

# 3. UI Scoreboard Engine (Updated with High Score Memory)
class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.goto(0, (HEIGHT // 2) - 50)
        self.score = 0
        self.high_score = 0  # Persistent metric across restarts
        self.draw_score()

    def draw_score(self):
        self.clear()
        self.goto(0, (HEIGHT // 2) - 50)
        self.color("white")
        # Displays both current session progress and all-time record side-by-side
        self.write(f"SCORE: {self.score}   BEST: {self.high_score}", align="center", font=("Courier", 22, "bold"))

    def add_points(self, points):
        self.score += points
        # Real-time state comparison logic
        if self.score > self.high_score:
            self.high_score = self.score
        self.draw_score()

    def game_over_screen(self):
        self.goto(0, 50)
        self.color("red")
        self.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
        self.goto(0, 0)
        self.color("white")
        self.write(f"FINAL SCORE: {self.score}", align="center", font=("Courier", 18, "normal"))
        self.goto(0, -30)
        self.color((0, 255, 255)) # Cyan highlighting for the milestone record
        self.write(f"ALL-TIME BEST: {self.high_score}", align="center", font=("Courier", 18, "bold"))
        self.goto(0, -80)
        self.color((57, 255, 20)) 
        self.write("PRESS 'R' TO RESTART GAME", align="center", font=("Courier", 14, "bold"))

# 4. Particle Effects Class
class Particle(Sprite):
    def __init__(self, x, y, angle_degrees, initial_color):
        super().__init__("circle", initial_color, x, y)
        self.shapesize(0.2)  
        self.radius = 2
        self.lifespan = 40  

        random_spread = random.uniform(-15, 15)
        angle_rad = math.radians(angle_degrees + 180 + random_spread)  
        launch_speed = random.uniform(3, 6)
        self.dx = math.cos(angle_rad) * launch_speed
        self.dy = math.sin(angle_rad) * launch_speed

    def update_physics_and_color(self):
        self.move()
        self.lifespan -= 1
        self.dx *= 0.96
        self.dy *= 0.96

        hue = max(0.0, min(0.18, (self.lifespan / 40.0) * 0.18))
        value = max(0.0, min(1.0, (self.lifespan / 25.0)))
        rgb = colorsys.hsv_to_rgb(hue, 1.0, value)
        self.color(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

# 5. Ship Subclass
class PlayerShip(Sprite):
    def __init__(self):
        super().__init__("triangle", NEON_PALETTE[1], 0, 0) 
        self.shapesize(stretch_wid=0.6, stretch_len=1.2)
        self.setheading(90)
        self.radius = 12
        self.is_thrusting = False
        self.damage_flash_timer = 0

    def turn_left(self):  self.left(15)
    def turn_right(self): self.right(15)
    def thrust_on(self):  self.is_thrusting = True
    def thrust_off(self): self.is_thrusting = False

    def activate_thrust(self):
        angle_rad = math.radians(self.heading())
        acceleration = 0.5
        self.dx += math.cos(angle_rad) * acceleration
        self.dy += math.sin(angle_rad) * acceleration

    def update_physics_and_state(self):
        self.move()
        self.dx *= 0.97
        self.dy *= 0.97

        if self.damage_flash_timer > 0:
            self.color("red")  
            self.damage_flash_timer -= 1
        elif self.is_thrusting:
            self.color("white") 
        else:
            self.color(NEON_PALETTE[1]) 

# 6. Asteroid Subclass
class Asteroid(Sprite):
    def __init__(self):
        x = random.choice([-WIDTH//2, WIDTH//2])
        y = random.randint(-HEIGHT//2, HEIGHT//2)
        my_color = random.choice(NEON_PALETTE)
        
        super().__init__("circle", my_color, x, y)
        self.shapesize(random.uniform(1.8, 2.8)) 
        self.radius = int(self.shapesize()[0] * 10)
        
        self.dx = random.uniform(-1.8, 1.8)
        self.dy = random.uniform(-1.8, 1.8)

# 7. Projectile Subclass
class Laser(Sprite):
    def __init__(self, ship_x, ship_y, ship_heading):
        super().__init__("square", (255, 0, 0), ship_x, ship_y) 
        self.shapesize(stretch_wid=0.1, stretch_len=0.7)
        self.setheading(ship_heading)
        self.radius = 5
        angle_rad = math.radians(ship_heading)
        speed = 12
        self.dx = math.cos(angle_rad) * speed
        self.dy = math.sin(angle_rad) * speed
        self.lifespan = 30

# 8. Central State Initialization
player = PlayerShip()
scoreboard = Scoreboard()  
asteroids = [Asteroid() for _ in range(7)]
lasers = []
particles = []
game_active = True

def fire_laser():
    if game_active and len(lasers) < 4:
        lasers.append(Laser(player.xcor(), player.ycor(), player.heading()))

def restart_game():
    global game_active, lasers, particles
    if not game_active:
        # Note: scoreboard.high_score is explicitly LEFT ALIVE here
        scoreboard.score = 0
        scoreboard.draw_score()
        
        player.goto(0, 0)
        player.setheading(90)
        player.dx = 0.0
        player.dy = 0.0
        player.color(NEON_PALETTE[1])
        
        for laser in lasers:
            laser.hideturtle()
        for particle in particles:
            particle.hideturtle()
        lasers.clear()
        particles.clear()
        
        for asteroid in asteroids:
            asteroid.goto(random.choice([-WIDTH//2, WIDTH//2]), random.randint(-HEIGHT//2, HEIGHT//2))
            asteroid.color(random.choice(NEON_PALETTE))
            asteroid.dx = random.uniform(-1.8, 1.8)
            asteroid.dy = random.uniform(-1.8, 1.8)
            
        game_active = True
        game_engine_loop()

screen.listen()
screen.onkeypress(player.turn_left, "Left")
screen.onkeypress(player.turn_right, "Right")
screen.onkeypress(player.thrust_on, "Up") 
screen.onkeyrelease(player.thrust_off, "Up") 
screen.onkeypress(fire_laser, "space")
screen.onkeypress(restart_game, "r")  
screen.onkeypress(restart_game, "R")

# 9. Asynchronous Game Loop
def game_engine_loop():
    global game_active
    if not game_active:
        return

    if player.is_thrusting:
        player.activate_thrust()
        rear_x = player.xcor() - math.cos(math.radians(player.heading())) * 15
        rear_y = player.ycor() - math.sin(math.radians(player.heading())) * 15
        particles.append(Particle(rear_x, rear_y, player.heading(), (255, 255, 0))) 

    player.update_physics_and_state()

    # Process Active Projectiles
    for laser in lasers[:]:
        laser.move()
        laser.lifespan -= 1
        if laser.lifespan <= 0:
            laser.hideturtle()
            if laser in lasers: lasers.remove(laser)

    # Process Dynamic Color Particles
    for particle in particles[:]:
        particle.update_physics_and_color()
        if particle.lifespan <= 0:
            particle.hideturtle()
            if particle in particles: particles.remove(particle)

    # Process Asteroids & Collisions
    for asteroid in asteroids:
        asteroid.move()

        if player.is_colliding_with(asteroid):
            game_active = False
            player.color("red")
            scoreboard.game_over_screen()
            screen.update()
            return  

        # Check Projectile Impact Matrix
        for laser in lasers[:]:
            if laser.is_colliding_with(asteroid):
                laser.hideturtle()
                if laser in lasers: lasers.remove(laser)
                
                # Award 10 points per destruction, system validates if high score is breached
                scoreboard.add_points(10)
                
                asteroid.goto(random.choice([-WIDTH//2, WIDTH//2]), random.randint(-HEIGHT//2, HEIGHT//2))
                asteroid.color(random.choice(NEON_PALETTE))
                asteroid.dx = random.uniform(-1.8, 1.8)
                asteroid.dy = random.uniform(-1.8, 1.8)

    screen.update()
    screen.ontimer(game_engine_loop, 20)

# Execute Engine
game_engine_loop()
screen.mainloop()