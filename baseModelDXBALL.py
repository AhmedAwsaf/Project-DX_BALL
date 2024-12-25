from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from math import cos, sin, radians


W_width = 800
W_height = 600

paddleobj = 0
paddle_x = 350
paddle_y = 30
paddle_width = 100
paddle_height = 10

ball_x, ball_y = 400, 300
ball_dx, ball_dy = 6, 6  # Increased speed
ball_radius = 10

bricks = []  # List to store bricks
brick_width = 60
brick_height = 20
brick_types = [1, 2, 3]  # 0: Iron, 1: Regular, 2: Wooden
brick_colors = {
    1: [1,0,0],
    2: [1,0,1],
    3: [0.5,0.5,0.5],
    4: [1,1,1]
}

paused = False  # Game state for pause/play

level0 = [
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,1,0,0,0],
    [0,3,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,1],
]

newDig = [W_width-20, W_height-20]
newTimDig = [W_width-20, W_height-50]
changeDigx = -20
score = 1234567890
time = 0
timecounter = 0
numbers = []
timenumbers = []

scoreboard={
    0:[
         1,
        1,1,
         0,
        1,1,
         1
    ],
    1:[
         0,
        0,1,
         0,
        0,1,
         0
    ],
    2:[
         1,
        0,1,
         1,
        1,0,
         1
    ],
    3:[
         1,
        0,1,
         1,
        0,1,
         1
    ],
    4:[
         0,
        1,1,
         1,
        0,1,
         0
    ],
    5:[
         1,
        1,0,
         1,
        0,1,
         1
    ],
    6:[
         1,
        1,0,
         1,
        1,1,
         1
    ],
    7:[
         1,
        0,1,
         0,
        0,1,
         0
    ],
    8:[
         1,
        1,1,
         1,
        1,1,
         1
    ],
    9:[
         1,
        1,1,
         1,
        0,1,
         1
    ],
}

def draw_points(x, y, w=4):
    glPointSize(w)
    glBegin(GL_POINTS)
    glVertex2f(x,y) 
    glEnd()

def draw_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        draw_points(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_rectangle(x, y, width, height):
    for i in range(height):
        draw_line(x, y-i, x + width, y-i)

falling_box = None
falling_box_width = 20
falling_box_height = 20
falling_box_speed = 4  # Speed at which the box falls

class Coin:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def move(self):
        self.y -= falling_box_speed  # Coin falls downwards

    def reset_position(self):
        self.x = random.randint(self.radius, W_width - self.radius)  # Random x position
        self.y = W_height  # Start at the top of the screen

    def draw(self):
        glColor3f(1, 0.84, 0)  # Gold color for the coin
        glBegin(GL_POINTS)
        for angle in range(0, 360, 10):  # Adjust the angle step for point density
            x = self.x + self.radius * cos(radians(angle))
            y = self.y + self.radius * sin(radians(angle))
            glVertex2f(x, y)
        glEnd()

# Modify the ball_move function to include logic for falling boxes
def falling_coin_move():
    global falling_box, score

    # Move the coin down
    falling_box.move()

    # Check if the coin collides with the paddle
    if (falling_box.y - falling_box.radius <= paddleobj.y + paddle_height and
        falling_box.x + falling_box.radius >= paddleobj.x and
        falling_box.x - falling_box.radius <= paddleobj.x + paddle_width):
        # Coin hit the paddle
        score += 10  # Increase the score
        falling_box.reset_position()  # Reset the coin to the top

    # If the coin falls off the screen, reset it
    if falling_box.y + falling_box.radius <= 0:
        falling_box.reset_position()

def initialize_falling_coin():
    global falling_box
    coin_radius = 10
    falling_box = Coin(random.randint(coin_radius, W_width - coin_radius), W_height, coin_radius)

class Brick:
    def __init__(self,x,y,li,w,h):
        self.x = x
        self.y = y
        self.ty = li
        self.li = li
        self.w = w
        self.h = h

class Number:
    def __init__(self,x,y,num, w=10):
        self.x = x
        self.y = y
        self.num = num
        self.w = w
    def draw(self):
        global scoreboard
        x,y,w = self.x,self.y,self.w
        scoreboardarr = scoreboard[self.num]

        Scoreline = {
            0: [x+w//2,y+w,x-w//2,y+w],
            1: [x-w//2,y+w,x-w//2,y],
            2: [x+w//2,y+w,x+w//2,y],
            3: [x+w//2,y,x-w//2,y],
            4: [x-w//2,y,x-w//2,y-w],
            5: [x+w//2,y,x+w//2,y-w],
            6: [x-w//2,y-w,x+w//2,y-w]
        }

        
        for i in range(len(scoreboardarr)):
            if scoreboardarr[i] == 1:
                x1,y1,x2,y2 = Scoreline[i]
                draw_line(x1,y1,x2,y2)

# Ball properties and movement
ball_radius = 10
ball_x, ball_y = 400, 300
ball_dx, ball_dy = 6, 6  # Increased speed
ball_paddle_collision = False  # Flag to check if the ball hit the paddle

def draw_ball():
    glColor3f(1, 1, 0)  # Ball color (Yellow)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(ball_x, ball_y)
    for angle in range(0, 360, 10):
        x = ball_x + ball_radius * cos(radians(angle))
        y = ball_y + ball_radius * sin(radians(angle))
        glVertex2f(x, y)
    glEnd()

def ball_move():
    global ball_x, ball_y, ball_dx, ball_dy, paddleobj, bricks, score, time

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Check for ball collision with walls
    if ball_x <= 0 or ball_x >= W_width:
        ball_dx = -ball_dx  # Reverse direction on X-axis
    if ball_y >= W_height:
        ball_dy = -ball_dy  # Reverse direction on Y-axis (bottom wall)

    # Ball hits top wall, game over
    if ball_y <= 0:
        game_over()

    # Ball hits paddle
    if (ball_y - ball_radius <= paddleobj.y + paddle_height and
        ball_x >= paddleobj.x and
        ball_x <= paddleobj.x + paddle_width):
        ball_dy = -ball_dy  # Reverse direction on Y-axis when hitting paddle

    # Ball hits bricks
    for brick in bricks[:]:
        if (brick.x <= ball_x <= brick.x + brick.w and
            brick.y <= ball_y <= brick.y + brick.h):
            ball_dy = -ball_dy  # Reverse direction on Y-axis when hitting brick
            bricks.remove(brick)
            score += 10  # Increase score when a brick is hit

def game_over():
    global score
    print("Game Over! Final Score:", score)
    # Reset or quit the game here as necessary
    exit()  # To terminate the game immediately


def draw_bricks():
    global bricks,brick_colors
    
    for brick in bricks:
        r,g,b = brick_colors[brick.ty]
        glColor3f(r,g,b)
        draw_rectangle(brick.x,brick.y,brick.w,brick.h)

def draw_paddle():
    global paddleobj,brick_colors
    r,g,b =brick_colors[paddleobj.ty]
    glColor3f(r,g,b)
    draw_rectangle(paddleobj.x,paddleobj.y,paddleobj.w,paddleobj.h)

def draw_score():
    global numbers
    glColor3f(0.2,1,0.4)
    for number in numbers:
        number.draw()

def check_score():
    global score, numbers, newDig, changeDigx
    temp_score = score
    n = 0

    while temp_score > 0:
        rem = temp_score % 10
        temp_score = temp_score // 10
        n += 1

        if len(numbers) < n:
            numbers.append(Number(newDig[0], newDig[1], 0))
            newDig[0] += changeDigx

        numbers[n-1].num = rem

    for i in range(n, len(numbers)):
        numbers[i].num = 0

def draw_time():
    global timenumbers
    glColor3f(1,0.5,0.6)
    for number in timenumbers:
        number.draw()

def check_time():
    global time, timenumbers, newTimDig, changeDigx
    temp_score = time
    n = 0

    while temp_score > 0:
        rem = temp_score % 10
        temp_score = temp_score // 10
        n += 1

        if len(timenumbers) < n:
            timenumbers.append(Number(newTimDig[0], newTimDig[1], 0))
            newTimDig[0] += changeDigx

        timenumbers[n-1].num = rem

    for i in range(n, len(timenumbers)):
        timenumbers[i].num = 0




def mouse_motion(x, y):
    global paddleobj
    paddleobj.x = x - paddle_width // 2
    paddleobj.x = max(0, min(W_width - paddle_width, paddleobj.x ))

def animate():
    global timecounter, time
    timecounter += 1
    if timecounter >= 10:
        time += 1
        timecounter = 0

    ball_move()  # Move the ball and check collisions
    falling_coin_move()  # Move the coin and check for collisions
    check_time()
    check_score()  

def display():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_bricks()
    draw_paddle()
    draw_ball()  # Draw the ball
    draw_score()
    draw_time()
    falling_box.draw()  # Draw the falling box
def intializeLevel():
    global level0, brick_height, brick_width, bricks, W_height, W_width, paddleobj, paddle_height, paddle_width, paddle_x, paddle_y
    leftp = (W_width - len(level0[0]) * (brick_width + 5)) // 2
    for y in range(len(level0)):
        for x in range(len(level0[0])):
            if level0[y][x] == 0:
                continue
            xp = leftp + x * (brick_width + 5)
            yp = W_height - 20 - y * (brick_height + 5)
            bricks.append(Brick(xp, yp, level0[y][x], brick_width, brick_height))

    paddleobj = Brick(paddle_x, paddle_y, 4, paddle_width, paddle_height)
    initialize_falling_coin()  # Initialize the coin

def iterate():
    global W_height, W_width
    glViewport(0, 0, W_width, W_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_width, 0.0, W_height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    display()
    glutSwapBuffers()

def timer(value):
    animate()  # Move the ball and the falling box
    glutPostRedisplay()  # Redisplay the screen
    glutTimerFunc(16, timer, 0)  # Call this function every 16 ms (60 FPS)

# Initialize and start the game
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W_width, W_height)  # Window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"DX_Ball CSE423-Project")  # Window name

intializeLevel()  # Initialize the game level and falling box

glutDisplayFunc(showScreen)
glutPassiveMotionFunc(mouse_motion)
glutTimerFunc(8, timer, 0)

glutMainLoop()






