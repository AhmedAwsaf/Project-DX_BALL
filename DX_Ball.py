from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_width = 800
W_height = 600

paddle_x = 350
paddle_width = 100
paddle_height = 10

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
    draw_line(x, y, x + width, y)
    draw_line(x + width, y, x + width, y + height)
    draw_line(x + width, y + height, x, y + height)
    draw_line(x, y + height, x, y)

def draw_paddle():
    global paddle_x
    draw_rectangle(paddle_x, 50, paddle_width, paddle_height)

def keyboard(key, x, y):
    global paddle_x

    if key == b'a':  # Move paddle left
        paddle_x -= 15
    elif key == b'd':  # Move paddle right
        paddle_x += 15

    # Keep paddle within window bounds
    paddle_x = max(0, min(W_width - paddle_width, paddle_x))

    glutPostRedisplay()

def display():
    draw_paddle()

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
    glColor3f(0.5, 0.0, 0.5)   # Paddle color

    # Call the draw methods here
    display()

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W_width, W_height)  # Window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"DX_Ball CSE423-Project")  # Window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)  # Register keyboard function

glutMainLoop()
