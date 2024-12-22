from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

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

class Brick:
    def __init__(self,x,y,li,w,h):
        self.x = x
        self.y = y
        self.ty = li
        self.li = li
        self.w = w
        self.h = h

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

def mouse_motion(x, y):
    global paddleobj
    paddleobj.x = x - paddle_width // 2
    paddleobj.x = max(0, min(W_width - paddle_width, paddleobj.x ))

def animate():
    pass

def display():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_bricks()

    draw_paddle()

def intializeLevel():
    global level0,brick_height,brick_width,bricks,W_height,W_width,paddleobj,paddle_height,paddle_width,paddle_x,paddle_y
    leftp = (W_width-len(level0[0])*(brick_width+5))//2
    for y in range(len(level0)):
        for x in range(len(level0[0])):
            if level0[y][x] == 0:
                continue
            xp = leftp + x*(brick_width+5)
            yp = W_height - 20 - y*(brick_height+5)
            bricks.append(Brick(xp,yp,level0[y][x],brick_width,brick_height))
    
    paddleobj = Brick(paddle_x,paddle_y,4,paddle_width,paddle_height)


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
    animate()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0) 

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W_width, W_height)  # Window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"DX_Ball CSE423-Project")  # Window name

intializeLevel()

glutDisplayFunc(showScreen)
# glutKeyboardFunc(keyboard)
glutPassiveMotionFunc(mouse_motion)
glutTimerFunc(8, timer, 0) 

glutMainLoop()
