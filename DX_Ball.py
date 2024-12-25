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

def draw_circle(x, y, radius):
    points = midpoint_circle(x, y, radius)
    glBegin(GL_POINTS)
    for point in points:
        glVertex2f(point[0], point[1])
    glEnd()

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

def draw_gradient_rectangle(x, y, width, height, color_start, color_end):
    r1, g1, b1 = color_start
    r2, g2, b2 = color_end
    for i in range(height):
        t = i / height
        r = r1 * (1 - t) + r2 * t
        g = g1 * (1 - t) + g2 * t
        b = b1 * (1 - t) + b2 * t
        glColor3f(r, g, b)
        draw_line(x, y - i, x + width, y - i)

def draw_bricks():
    for idx, brick in enumerate(bricks):
        brick_x, brick_y, brick_type = brick
        if brick_type == 0:  # Iron brick
            draw_gradient_rectangle(brick_x, brick_y, brick_width, brick_height, (0.5, 0.5, 0.5), (0.3, 0.3, 0.3))
        elif brick_type == 1:  # Regular brick
            if brick_health[(brick_x, brick_y)] == 2:
                draw_gradient_rectangle(brick_x, brick_y, brick_width, brick_height, (0.0, 0.0, 1.0), (0.0, 0.0, 0.7))
            elif brick_health[(brick_x, brick_y)] == 1:
                draw_gradient_rectangle(brick_x, brick_y, brick_width, brick_height, (0.5, 0.5, 1.0), (0.3, 0.3, 0.7))
        elif brick_type == 2:  # Wooden brick
            draw_gradient_rectangle(brick_x, brick_y, brick_width, brick_height, (0.6, 0.3, 0.1), (0.4, 0.2, 0.1))

def draw_paddle():
    global paddle_x
    glColor3f(0.3, 0.7, 0.9)  # Paddle color - light blue
    draw_rectangle(paddle_x, 50, paddle_width, paddle_height)

def draw_ball():
    glColor3f(1.0, 0.0, 1.0)  # Ball color - red
    radius = ball_radius
    x_center = ball_x
    y_center = ball_y

    x = radius
    y = 0
    p = 1 - radius

    # Loop to draw horizontal lines for filling
    while x >= y:
        # Draw horizontal lines between symmetric points
        draw_line(x_center - x, y_center + y, x_center + x, y_center + y)  # Upper part
        draw_line(x_center - y, y_center + x, x_center + y, y_center + x)  # Upper part
        draw_line(x_center - x, y_center - y, x_center + x, y_center - y)  # Lower part
        draw_line(x_center - y, y_center - x, x_center + y, y_center - x)  # Lower part

        y += 1
        if p < 0:
            p += 2 * y + 1
        else:
            x -= 1
            p += 2 * (y - x) + 1

def draw_rectangle(x, y, width, height):
    # Draw rectangle using lines
    for i in range(height):
        draw_line(x, y - i, x + width, y - i)

def draw_pause_button():
    """Draw a pause button in the bottom left corner using midpoint line drawing."""
    glColor3f(0.5, 0.5, 0.5)  # Gray color
    x_start = 10
    y_start = 10
    button_width = 30
    button_height = 30

    # Draw rectangle outline for pause button
    draw_line(x_start, y_start, x_start + button_width, y_start)
    draw_line(x_start, y_start, x_start, y_start + button_height)
    draw_line(x_start + button_width, y_start, x_start + button_width, y_start + button_height)
    draw_line(x_start, y_start + button_height, x_start + button_width, y_start + button_height)

    # Draw pause symbol (two vertical lines)
    line_spacing = 10
    draw_line(x_start + line_spacing, y_start + 5, x_start + line_spacing, y_start + button_height - 5)
    draw_line(x_start + button_width - line_spacing, y_start + 5, x_start + button_width - line_spacing, y_start + button_height - 5)

def draw_pause_menu():
    """Draw pause menu with Restart, Resume, and Exit buttons."""
    glColor3f(1.0, 1.0, 1.0)  # White color

    # Restart button
    restart_x, restart_y = 350, 400
    button_width, button_height = 100, 40
    draw_line(restart_x, restart_y, restart_x + button_width, restart_y)
    draw_line(restart_x, restart_y, restart_x, restart_y - button_height)
    draw_line(restart_x + button_width, restart_y, restart_x + button_width, restart_y - button_height)
    draw_line(restart_x, restart_y - button_height, restart_x + button_width, restart_y - button_height)

    # Resume button
    resume_x, resume_y = 350, 340
    draw_line(resume_x, resume_y, resume_x + button_width, resume_y)
    draw_line(resume_x, resume_y, resume_x, resume_y - button_height)
    draw_line(resume_x + button_width, resume_y, resume_x + button_width, resume_y - button_height)
    draw_line(resume_x, resume_y - button_height, resume_x + button_width, resume_y - button_height)

    # Exit button
    exit_x, exit_y = 350, 280
    draw_line(exit_x, exit_y, exit_x + button_width, exit_y)
    draw_line(exit_x, exit_y, exit_x, exit_y - button_height)
    draw_line(exit_x + button_width, exit_y, exit_x + button_width, exit_y - button_height)
    draw_line(exit_x, exit_y - button_height, exit_x + button_width, exit_y - button_height)

def mouse_motion(x, y):
    global paddle_x
    # Update paddle_x based on mouse x position
    paddle_x = x - paddle_width // 2

    # Keep paddle within window bounds
    paddle_x = max(0, min(W_width - paddle_width, paddle_x))

def mouse_click(button, state, x, y):
    global paused
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if paused:
            # Check if Restart button clicked
            if 350 <= x <= 450 and 200 <= (W_height - y) <= 240:
                print("Restart")
                glutLeaveMainLoop()
                return

            # Check if Resume button clicked
            if 350 <= x <= 450 and 260 <= (W_height - y) <= 300:
                paused = False
                return

            # Check if Exit button clicked
            if 350 <= x <= 450 and 320 <= (W_height - y) <= 360:
                print("Exit")
                glutLeaveMainLoop()
                return

        # Check if the click is inside the pause button
        if 10 <= x <= 40 and W_height - y <= 40:
            paused = not paused

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

def display():
    glClearColor(0.1, 0.1, 0.1, 1.0)  # Background color - dark gray
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_paddle()
    draw_ball()
    draw_bricks()
    draw_pause_button()
    if paused:
        draw_pause_menu()

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
    glutTimerFunc(16, timer, 0) 

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W_width, W_height)  # Window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"DX_Ball CSE423-Project")  # Window name
glutDisplayFunc(showScreen)
glutMouseFunc(mouse_click)  # Register mouse click function
glutPassiveMotionFunc(mouse_motion)  # Register mouse motion function
glutTimerFunc(16, timer, 0)  # Timer for ball updates

glutMainLoop()
