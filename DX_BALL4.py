from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_width = 800
W_height = 600
###########BALL PART################
ball_x, ball_y = 400, 300
ball_dx, ball_dy = 10, 10  # Adjust speed as needed
ball_radius = 10
paused = False  # Pause state
#########BALLL PART END#############
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


def draw_bricks():
    global bricks,brick_colors
    
    for brick in bricks:
        r,g,b = brick_colors[brick.ty]
        glColor3f(r,g,b)
        draw_rectangle(brick.x,brick.y,brick.w,brick.h)
def timer(value):
    update_ball()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)
###### ADDING NEW BALL PART ################
def draw_ball():
    glColor3f(1.0, 0.0, 0.0)  # Ball color - red
    radius = ball_radius
    x_center = ball_x
    y_center = ball_y

    x = radius
    y = 0
    p = 1 - radius

    while x >= y:
        draw_line(x_center - x, y_center + y, x_center + x, y_center + y)  # Upper
        draw_line(x_center - y, y_center + x, x_center + y, y_center + x)  # Upper
        draw_line(x_center - x, y_center - y, x_center + x, y_center - y)  # Lower
        draw_line(x_center - y, y_center - x, x_center + y, y_center - x)  # Lower

        y += 1
        if p < 0:
            p += 2 * y + 1
        else:
            x -= 1
            p += 2 * (y - x) + 1
def check_brick_collision():
    global ball_dx, ball_dy, bricks

    for brick in bricks[:]:  # Iterate over a copy to modify the original list
        # Check if the ball is within the bounds of the brick
        if (brick.x <= ball_x + ball_radius <= brick.x + brick.w or
            brick.x <= ball_x - ball_radius <= brick.x + brick.w) and \
           (brick.y <= ball_y + ball_radius <= brick.y + brick.h or
            brick.y <= ball_y - ball_radius <= brick.y + brick.h):
            
            if ball_y + ball_radius >= brick.y and ball_y - ball_radius <= brick.y + brick.h:
                ball_dy = -ball_dy  
            else:
                ball_dx = -ball_dx  

            if brick.ty > 1:
                brick.ty -= 1  
            else:
                bricks.remove(brick)  
            break  

def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy, paused

    if paused:
        return  

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Wall collisions
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= W_width:
        ball_dx = -ball_dx 
    if ball_y + ball_radius >= W_height:
        ball_dy = -ball_dy 

    # Paddle collision
    if paddle_y <= ball_y - ball_radius <= paddle_y + paddle_height:
        if paddle_x <= ball_x <= paddle_x + paddle_width:
            ball_dy = -ball_dy  

    
    check_brick_collision()
########### ADDID NEW END####################
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
############### BACKGROUND PART ############################
def draw_hill():
    glColor3f(0.2, 0.6, 0.2)  # Set hill color (greenish)
    hill_peak_x = W_width // 2
    hill_peak_y = W_height // 2
    hill_base_y = 0
    hill_left_x = 0
    hill_right_x = W_width

    for y in range(hill_base_y, hill_peak_y + 1):
        x_start = int(hill_left_x + (hill_peak_x - hill_left_x) * (y / hill_peak_y))
        x_end = int(hill_right_x - (hill_right_x - hill_peak_x) * (y / hill_peak_y))
        for x in range(x_start, x_end + 1):
            draw_points(x, y)  
def draw_tree(x, y, trunk_width, trunk_height, foliage_radius):
    # Draw trunk
    glColor3f(0.2, 0.1, 0.0)  
    for i in range(trunk_height):
        for j in range(-trunk_width // 2, trunk_width // 2 + 1):
            draw_points(x + j, y + i)

   
    glColor3f(0.0, 0.4, 0.0)  # Foliage color (green)
    for i in range(-foliage_radius, foliage_radius + 1):
        for j in range(-foliage_radius, foliage_radius + 1):
            if i**2 + j**2 <= foliage_radius**2:
                draw_points(x + j, y + trunk_height + i)
def draw_treehouse(x, y, house_width, house_height):
    glColor3f(0.5, 0.35, 0.2)  # House color (wooden brown)
    for i in range(house_height):
        for j in range(-house_width // 2, house_width // 2 + 1):
            draw_points(x + j, y + i)

  
    glColor3f(0.3, 0.2, 0.1)  # Roof color (dark brown)
    roof_height = house_height // 2
    for i in range(roof_height):
        x_start = x - house_width // 2 + i
        x_end = x + house_width // 2 - i
        for j in range(x_start, x_end + 1):
            draw_points(j, y + house_height + i)

def draw_treehouse(x, y, house_width, house_height):
   
    glColor3f(0.5, 0.35, 0.2)  # House color (wooden brown)
    for i in range(house_height):
        for j in range(-house_width // 2, house_width // 2 + 1):
            draw_points(x + j, y + i)

    # Draw the roof
    glColor3f(0.3, 0.2, 0.1)  # Roof color (dark brown)
    roof_height = house_height // 2
    for i in range(roof_height):
        x_start = x - house_width // 2 + i
        x_end = x + house_width // 2 - i
        for j in range(x_start, x_end + 1):
            draw_points(j, y + house_height + i)

def draw_bird(x, y, size):
    glColor3f(0.0, 0.0, 0.0)  # Bird color (black)
    for i in range(-size, size + 1):
        draw_points(x + i, y + abs(i) // 2)
        draw_points(x - i, y + abs(i) // 2)

def draw_scene_elements():
    # Draw trees at the edges
    draw_tree(100, 50, 10, 50, 20)  # Left edge
    draw_tree(W_width - 100, 50, 10, 50, 20)  # Right edge

    # Draw treehouse on the right
    draw_treehouse(W_width - 200, 150, 40, 30)

    # Draw birds
    draw_bird(200, 500, 10)
    draw_bird(250, 520, 8)
    draw_bird(450, 540, 12)
    draw_bird(500, 560, 9)
    draw_bird(300, 550, 6)

  
    text = "LEVEL-1"
    text_width = len(text) * (50 + 10)  # Adjust based on text size and spacing
    draw_text(W_width // 2 - text_width // 2, W_height // 2 - 25, text, size=50)
def draw_text(x, y, text, size=50):

    spacing = size + 10  # Increase spacing to match larger size
    glColor3f(1, 1, 1)  # White color for text

    for i, char in enumerate(text.upper()):
        draw_character(x + i * spacing, y, char, size)
def draw_character(x, y, char, size=50):
    character_map = {
        "L": [(0, 0), (0, size), (0, 0), (size // 2, 0)],
        "E": [(0, 0), (0, size), (0, 0), (size // 2, 0), (0, size // 2), (size // 2, size // 2)],
        "V": [(0, size), (size // 2, 0), (size, size)],
        "1": [(size // 2, 0), (size // 2, size)],
        "-": [(0, size // 2), (size, size // 2)],
    }

    if char not in character_map:
        return

    for x_offset, y_offset in character_map[char]:
        draw_points(x + x_offset, y + y_offset)
def draw_character(x, y, char, size=8):
    character_map = {
        "L": [(0, 0), (0, size), (0, 0), (size // 2, 0)],
        "E": [(0, 0), (0, size), (0, 0), (size // 2, 0), (0, size // 2), (size // 2, size // 2)],
        "V": [(0, size), (size // 2, 0), (size, size)],
        "1": [(size // 2, 0), (size // 2, size)],
        "-": [(0, size // 2), (size // 2, size // 2)],
    }

    if char not in character_map:
        return

    for x_offset, y_offset in character_map[char]:
        draw_points(x + x_offset, y + y_offset)

############### BACKGROUND PART END ############################
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
    global timecounter,time
    timecounter += 1
    if timecounter >= 10:
        time += 1
        timecounter = 0

    check_time()
    check_score()

def display():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_bricks()

    draw_hill()  # Draw the background hill
    draw_scene_elements()  # Draw trees, treehouse, birds, and text
    draw_ball()
    draw_bricks()
    draw_paddle()
    draw_score()
    draw_time()

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
    update_ball()
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
glutTimerFunc(16, timer, 0) 

glutMainLoop()
