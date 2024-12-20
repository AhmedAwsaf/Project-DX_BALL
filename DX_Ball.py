from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_width = 800
W_height = 600

paddle_x = 350
paddle_width = 100
paddle_height = 10

ball_x, ball_y = 400, 300
ball_dx, ball_dy = 6, 6  # Increased speed
ball_radius = 10

bricks = []  # List to store bricks
brick_width = 60
brick_height = 20
brick_types = [0, 1, 2]  # 0: Iron, 1: Regular, 2: Wooden

brick_health = {}  # Dictionary to track brick health
paused = False  # Game state for pause/play

# Initialize bricks in an upside-down triangular shape
triangle_base = 10  # Base width of the triangle in bricks
for row in range(triangle_base):
    for col in range(triangle_base - row):
        brick_x = (W_width // 2 - ((triangle_base - row) * (brick_width + 5)) // 2) + col * (brick_width + 5)
        brick_y = W_height - row * (brick_height + 5)
        brick_type = random.choice(brick_types)  # Randomize brick types
        bricks.append((brick_x, brick_y, brick_type))
        if brick_type == 1:  # Regular bricks need 2 hits
            brick_health[(brick_x, brick_y)] = 2
        elif brick_type == 2:  # Wooden bricks need 1 hit
            brick_health[(brick_x, brick_y)] = 1


def draw_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    glBegin(GL_POINTS)
    while True:
        glVertex2f(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    glEnd()

def draw_rectangle(x, y, width, height):
    # Draw rectangle using lines
    for i in range(height):
        draw_line(x, y-i, x + width, y-i)

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def draw_paddle():
    global paddle_x
    glColor3f(0.3, 0.7, 0.9)  # Paddle color - light blue
    draw_rectangle(paddle_x, 50, paddle_width, paddle_height)

def draw_ball():
    glColor3f(1.0, 0.0, 0.0)  # Ball color - red
    glBegin(GL_POINTS)
    for i in range(-ball_radius, ball_radius):
        for j in range(-ball_radius, ball_radius):
            if i**2 + j**2 <= ball_radius**2:
                glVertex2f(ball_x + i, ball_y + j)
    glEnd()

def draw_bricks():
    for brick in bricks:
        brick_x, brick_y, brick_type = brick
        if brick_type == 0:  # Iron brick
            glColor3f(0.5, 0.5, 0.5)  # Gray
        elif brick_type == 1:  # Regular brick
            if brick_health[(brick_x, brick_y)] == 2:
                glColor3f(0.0, 0.0, 1.0)  # Blue
            elif brick_health[(brick_x, brick_y)] == 1:
                glColor3f(0.5, 0.5, 1.0)  # Light Blue
        elif brick_type == 2:  # Wooden brick
            glColor3f(0.6, 0.3, 0.1)  # Brown
        draw_rectangle(brick_x, brick_y, brick_width, brick_height)

def mouse_motion(x, y):
    global paddle_x
    # Update paddle_x based on mouse x position
    paddle_x = x - paddle_width // 2

    # Keep paddle within window bounds
    paddle_x = max(0, min(W_width - paddle_width, paddle_x))
    glutPostRedisplay()

def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy, bricks, brick_health, paused

    if paused:
        return  # Do not update ball if paused

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Wall collisions
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= W_width:
        ball_dx = -ball_dx
    if ball_y + ball_radius >= W_height:
        ball_dy = -ball_dy

    # Paddle collision
    if (paddle_x <= ball_x <= paddle_x + paddle_width and
            50 <= ball_y - ball_radius <= 50 + paddle_height):
        ball_dy = -ball_dy

    # Brick collisions
    for brick in bricks:
        brick_x, brick_y, brick_type = brick
        if (brick_x <= ball_x <= brick_x + brick_width and
                brick_y <= ball_y <= brick_y + brick_height):
            if brick_type == 0:  # Iron bricks are unbreakable
                ball_dx = -ball_dx if (ball_x == brick_x or ball_x == brick_x + brick_width) else ball_dx
                ball_dy = -ball_dy if (ball_y == brick_y or ball_y == brick_y + brick_height) else ball_dy
            else:
                brick_health[(brick_x, brick_y)] -= 1
                if brick_health[(brick_x, brick_y)] == 0:
                    bricks.remove(brick)  # Remove the brick
                    del brick_health[(brick_x, brick_y)]  # Remove from health tracker
                ball_dy = -ball_dy  # Reverse ball direction
            break

    # Bottom collision (game over)
    if ball_y - ball_radius <= 0:
        print("Game Over")
        glutLeaveMainLoop()

def keyboard(key, x, y):
    global paused
    if key == b'p':  # Toggle pause
        paused = not paused

def display():
    glClearColor(0.1, 0.1, 0.1, 1.0)  # Background color - dark gray
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_paddle()
    draw_ball()
    draw_bricks()

    # Draw pause/play text
    glColor3f(1.0, 1.0, 1.0)
    if paused:
        draw_text(W_width // 2 - 50, W_height // 2, "PAUSED")
    else:
        draw_text(10, 10, "Press 'P' to Pause")

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
    update_ball()
    glutPostRedisplay()
    glutTimerFunc(10, timer, 0)  # Faster timer

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W_width, W_height)  # Window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"DX_Ball CSE423-Project")  # Window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)  # Register keyboard function
glutPassiveMotionFunc(mouse_motion)  # Register mouse motion function
glutTimerFunc(10, timer, 0)  # Timer for ball updates

glutMainLoop()
