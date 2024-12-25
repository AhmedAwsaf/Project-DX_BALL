from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_width = 800
W_height = 600

ball_x, ball_y = 400, 300
ball_dx, ball_dy = 6, 6 
ball_radius = 7

paddleobj = 0
paddle_x = 350
paddle_y = 30
paddle_width = 100
paddle_height = 10

ball_x, ball_y = 400, 300
ball_speed = 6
ball_dx, ball_dy = -6, -6 
ball_radius = 10

falling_box = None
falling_box_width = 20
falling_box_height = 20
falling_box_speed = 4 

bricks = [] 
rembricks = [] 
brick_width = 60
brick_height = 20
brick_types = [1, 2, 3] 
brick_colors = {
    1: (0.9, 0.3, 0.1),    # Brick Type 1: Red-Orange
    2: (0.1, 1.0, 1.0),    # Brick Type 2: Cyan (Damage Brick)
    3: (0.5, 0.5, 0.5),    # Brick Type 3: Gray (Iron Brick)
    4: (1.0, 0.7, 0.9),    # Paddle: Pinkish
    5: (0.3, 0.3, 0.7)     # Brick Type 5: Dark Blue (Damage Brick 2)
}

paused = False 
scene = 0
# 0: Menu, 1: Game, 2: Game Over


level0 = [
    [0,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,1,0,1,0,0,0,0],
    [0,0,0,1,0,1,0,1,0,0,0],
    [0,0,1,0,1,0,1,0,1,3,0],
    [0,1,0,1,0,1,0,1,0,1,0],
    [1,0,2,0,1,0,1,0,1,0,1]
]
levelblocks = 0
levelblocksbroken = 0

newDig = [W_width-20, W_height-20]
newTimDig = [W_width-20, W_height-50]
changeDigx = -20
score = 11
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
    10:[
         1,
        1,0,
         0,
        1,1,
         1
    ], #G
    11:[
         1,
        1,1,
         1,
        1,1,
         0
    ], #A
    12:[
         0,
        1,1,
         0,
        1,1,
         0
    ],#M
    13:[
         1,
        1,0,
         1,
        1,0,
         1
    ],#E
    14:[
         1,
        1,0,
         1,
        1,1,
         0
    ],#R
    15:[
         1,
        1,0,
         0,
        1,0,
         1
    ],#c
    16:[
         1,
        1,1,
         1,
        0,1,
         1
    ],
    17:[
         1,
        1,1,
         1,
        0,1,
         1
    ],
}

def draw_points(x, y, w=2):
    glPointSize(w)
    glBegin(GL_POINTS)
    glVertex2f(x,y) 
    glEnd()

def draw_line(x1, y1, x2, y2, w=4):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        draw_points(x1, y1, w)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_rectangle(x, y, width, height, color_start):
    r1, g1, b1 = color_start

    glColor3f(r1, g1, b1)
    draw_line(x, y, x + width, y)
    draw_line(x, y - height, x + width, y - height)
    draw_line(x, y, x, y - height)
    draw_line(x + width, y, x + width, y - height)
    draw_line(x+height//2, y-height//2, x+width-height//2, y-height//2, height)

def draw_circle(x,y,r,c,w=2):
    r1,g1,b1 = c
    glColor3f(r1,g1, b1) 
    radius = r
    x_center = x
    y_center = y

    x = radius
    y = 0
    p = 1 - radius

    while x >= y:
        draw_line(x_center - x, y_center + y, x_center + x, y_center + y, w) 
        draw_line(x_center - y, y_center + x, x_center + y, y_center + x, w) 
        draw_line(x_center - x, y_center - y, x_center + x, y_center - y, w) 
        draw_line(x_center - y, y_center - x, x_center + y, y_center - x, w) 

        y += 1
        if p < 0:
            p += 2 * y + 1
        else:
            x -= 1
            p += 2 * (y - x) + 1

def draw_ball():
    global ball_y,ball_x,ball_radius
    glColor3f(1.0, 1,1.0) 
    radius = ball_radius
    x_center = ball_x
    y_center = ball_y

    x = radius
    y = 0
    p = 1 - radius

    while x >= y:
        draw_line(x_center - x, y_center + y, x_center + x, y_center + y) 
        draw_line(x_center - y, y_center + x, x_center + y, y_center + x) 
        draw_line(x_center - x, y_center - y, x_center + x, y_center - y) 
        draw_line(x_center - y, y_center - x, x_center + y, y_center - x) 

        y += 2
        if p < 0:
            p += 2 * y + 1
        else:
            x -= 2
            p += 2 * (y - x) + 1

class Brick:
    def __init__(self,x,y,li,w,h):
        self.x = x
        self.y = y
        self.ty = li
        self.li = li
        self.w = w
        self.h = h
        self.e = True

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
        if not brick.e:
            continue
        s = brick_colors[brick.ty]
        if brick.ty == 2 and brick.li == 1:
            s = brick_colors[5]
        draw_rectangle(brick.x,brick.y,brick.w,brick.h,s)

def draw_paddle():
    global paddleobj,brick_colors
    s = brick_colors[paddleobj.ty]
    draw_rectangle(paddleobj.x,paddleobj.y,paddleobj.w,paddleobj.h,s)

def draw_score():
    global numbers
    glColor3f(0.2,1,0.4)
    for number in numbers:
        number.draw()



class Coin:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def move(self):
        self.y -= falling_box_speed 

    def draw(self):
        glColor3f(1, 0.84, 0) 
        draw_circle(self.x,self.y,self.radius,(1,0.84,0))
        
def create_coin(x,y):
    global falling_box
    if falling_box == None:
        falling_box = Coin(x,y,7)

############### BACKGROUND PART ############################
def draw_hill():
    glColor3f(0.2, 0.6, 0.2) 
    hill_peak_x = W_width // 2
    hill_peak_y = W_height // 2
    hill_base_y = 0
    hill_left_x = 0
    hill_right_x = W_width

    for y in range(hill_base_y, hill_peak_y + 1,6):
        x_start = int(hill_left_x + (hill_peak_x - hill_left_x) * (y / hill_peak_y))
        x_end = int(hill_right_x - (hill_right_x - hill_peak_x) * (y / hill_peak_y))
        for x in range(x_start, x_end + 1,6):
            draw_points(x, y, 6)  
def draw_tree(x, y, trunk_width, trunk_height, foliage_radius):

    glColor3f(0.2, 0.1, 0.0)  
    for i in range(0,trunk_height,2):
        for j in range(-trunk_width // 2, trunk_width // 2 + 1,2):
            draw_points(x + j, y + i)

   
    glColor3f(0.0, 0.4, 0.0)  
    draw_circle(x, y + trunk_height, foliage_radius, (0.0, 0.4, 0.0))


def draw_treehouse(x, y, house_width, house_height):
   
    glColor3f(0.5, 0.35, 0.2)  
    for i in range(house_height):
        for j in range(-house_width // 2, house_width // 2 + 1):
            draw_points(x + j, y + i)

    glColor3f(0.3, 0.2, 0.1) 
    roof_height = house_height // 2
    for i in range(roof_height):
        x_start = x - house_width // 2 + i
        x_end = x + house_width // 2 - i
        for j in range(x_start, x_end + 1):
            draw_points(j, y + house_height + i)

def draw_bird(x, y, size):
    
    for i in range(-size, size + 1):
        # glColor3f(0.0, 0.0, 0.0) 
        # draw_points(x + i, y + abs(i) // 2)
        # draw_points(x - i, y + abs(i) // 2)
        
        glColor3f(1.0, 1.0, 1.0) 
        draw_points(x + i, y + abs(i) // 2)
        draw_points(x - i, y + abs(i) // 2)

def draw_background():
    draw_tree(100, 50, 10, 50, 20)  
    draw_tree(W_width - 100, 50, 10, 50, 20)  

    draw_treehouse(W_width - 200, 150, 40, 30)

    draw_bird(200, 500, 10)
    draw_bird(250, 520, 8)
    draw_bird(450, 540, 12)
    draw_bird(500, 560, 9)
    draw_bird(300, 550, 6)

############################################################

window_width = W_width
window_height = W_height

def draw_point(x, y):
    """Helper function to draw a point at (x, y)"""
    glVertex2f(x, y)

def draw_building(x, y, width, height, lit_ratio=0.1):
    """
    Draws a single building using GL_POINTS. Lit windows are randomized.
    The window layout is symmetrical in the building area.
    """
    glColor3f(0.3, 0.3, 0.3)  # Dark gray for the building outline
    # Draw each point as part of the building
    for i in range(width):
        for j in range(height):
            draw_point(x + i, y + j)  # Use helper function

    # Draw lit windows as points (windows in a grid)
    window_size = 3  # Smaller window size
    glColor3f(1.0, 1.0, 1.0)  # White for lit windows
    window_columns = width // window_size  # Number of columns
    window_rows = height // window_size  # Number of rows

    for row in range(window_rows):
        for col in range(window_columns):
            if random.random() < lit_ratio:  # Lit window
                wx = x + col * window_size
                wy = y + row * window_size
                for i in range(window_size):
                    for j in range(window_size):
                        draw_point(wx + i, wy + j)  # Representing the window with points

def draw_clouds():
    """
    Draws large clouds using GL_POINTS (white and black ash clouds).
    """
    cloud_count = 100  # Reduced count since clouds will be larger
    for _ in range(cloud_count):
        # Randomly generate cloud position
        x = random.randint(-window_width, window_width)
        y = random.randint(int(window_height / 2), window_height)

        # Random size for clouds
        cloud_size = random.randint(5, 20)

        # Draw the cloud as a cluster of points
        color_choice = random.choice([(1.0, 1.0, 1.0), (0.2, 0.2, 0.2)])  # White or black ash cloud
        glColor3f(*color_choice)

        # Generate the cloud by drawing points in a small area around (x, y)
        for i in range(cloud_size):
            for j in range(cloud_size):
                # Randomly scatter points around the cloud center
                draw_point(x + random.randint(-5, 5), y + random.randint(-5, 5))  # Cloud point

def draw_airplane():
    """
    Draws a simple airplane using GL_POINTS.
    """
    airplane_x = random.randint(-window_width, window_width)
    airplane_y = random.randint(window_height // 2, window_height)

    glColor3f(1.0, 1.0, 1.0)  # White for airplane

    # Airplane body (represented by points)
    draw_point(airplane_x, airplane_y)  # Front of airplane (tail)
    draw_point(airplane_x + 10, airplane_y - 5)  # Back of airplane (body)

    # Wings of the airplane (V shape using points)
    draw_point(airplane_x + 5, airplane_y)  # Left wing
    draw_point(airplane_x + 5, airplane_y - 10)  # Right wing
    draw_point(airplane_x + 15, airplane_y - 5)  # Wing connection

def draw_buildings():
    """
    Draws the city buildings using multiple buildings with increased height and symmetrical windows.
    """
    building_width_range = (40, 80)
    building_height_range = (300, 600)  # Increased building height range
    x = -window_width

    while x < window_width:
        width = random.randint(*building_width_range)
        height = random.randint(*building_height_range)
        y = -window_height
        draw_building(x, y, width, height, lit_ratio=0.03)  # Buildings are drawn as points
        x += width + random.randint(40, 60)  # Increased gap between buildings to reduce their number

def draw_city_background():
    """
    Entry point to render the city background.
    Calls other functions to draw the city skyline, clouds, and airplane.
    """
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)

    # Draw buildings using GL_POINTS
    draw_buildings()

    # Draw clouds using GL_POINTS
    draw_clouds()

    # Draw airplane using GL_POINTS
    draw_airplane()

    glEnd()
    glFlush()


#########################################################

def check_score():
    global score, numbers, newDig, changeDigx, levelblocksbroken, levelblocks
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
    
    if levelblocksbroken>=levelblocks:
        print("END")
    

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

def check_collision(ball_x, ball_y, ball_r, block):
    # Ball boundaries
    ball_left = ball_x - ball_r
    ball_right = ball_x + ball_r
    ball_top = ball_y - ball_r 
    ball_bottom = ball_y + ball_r 

    # Block boundaries
    block_left = block.x
    block_right = block.x + block.w
    block_top = block.y - block.h
    block_bottom = block.y

    # Check for collision
    if ball_right > block_left and ball_left < block_right and ball_bottom > block_top and ball_top < block_bottom:

        overlap_x = min(ball_right - block_left, block_right - ball_left)
        overlap_y = min(ball_bottom - block_top, block_bottom - ball_top)

        # Determine collision side
        if overlap_x < overlap_y:  
            if ball_x < block.x:
                return "Left"
            else:
                return "Right"
        else:
            if ball_y < block.y:
                return "Top"
            else:
                return "Bottom"
    return None



def update_ball():
    global ball_x,ball_y,ball_dx,ball_dy,ball_radius, W_width, W_height, paddleobj, ball_speed, bricks, rembricks, level0, brick_height , levelblocksbroken, falling_box, score
    ball_x += ball_dx
    ball_y += ball_dy
    
    # paddle
    if ball_y - ball_radius < paddleobj.y + paddleobj.h:
        if paddleobj.x <= ball_x <= paddleobj.x + paddleobj.w:
            relative_intersection = (ball_x - (paddleobj.x + paddleobj.w // 2)) / (paddleobj.w // 2)

            ball_dy *= -1

            ball_dx = relative_intersection * ball_speed 

    
    # bound
    if ball_x - ball_radius < 0 or ball_x + ball_radius > W_width:
        ball_dx = -ball_dx
    if ball_y + ball_radius > W_height:
        ball_dy = -ball_dy
        
    #bricks
    b_start = 100+(len(level0)*(brick_height+5))
    
    if W_height - b_start < ball_y + ball_radius:
        for bricki in range(len(bricks)):
            if not bricks[bricki].e:
                continue
            side = check_collision(ball_x,ball_y, ball_radius,bricks[bricki])
            if side == None:
                continue
            if side == "Left" or side == "Right":
                ball_dx = -ball_dx
                rembricks.append(bricki)
            if side =="Top" or side =="Bottom":
                ball_dy = -ball_dy
                rembricks.append(bricki)
                
    while rembricks != []:
        i = rembricks[len(rembricks)-1]
        brick = bricks[i]
        if brick.ty == 2 and brick.li > 1:
            print("damage")
            brick.li -=1
            score += 5
        elif brick.ty != 3:
            create_coin(bricks[i].x,bricks[i].y)
            # bricks.pop(i)
            brick.e = False
            levelblocksbroken += 1
            score += 10
            
        rembricks.pop() 
    
    if falling_box != None and paddleobj.y>=falling_box.y>= paddleobj.y - paddleobj.h:
        if paddleobj.x < falling_box.x < paddleobj.x + paddleobj.w:
            falling_box = None
            score += 18
    

def mouse_motion(x, y):
    global paddleobj, paused, scene 
    if not paused and scene == 1:
        paddleobj.x = x - paddle_width // 2
        paddleobj.x = max(0, min(W_width - paddle_width, paddleobj.x ))

def keyboard(key, x, y):
    global paused,scene
    if scene == 1:
        if key == b'p':  # Toggle pause
            paused = not paused

def Click(button, state, x, y):
    global W_height,W_width,score,scene
    xp,yp = x,W_height-y
    x_c,y_c = W_width//2, W_height//2
    if scene == 2:
        if (x_c-110< xp <x_c+110) and (y_c-5<yp<y_c+40):
            if state==GLUT_DOWN:
                scene=0
    

def animate():
    global timecounter,time,falling_box
    timecounter += 1
    if timecounter >= 10:
        time += 1
        timecounter = 0
        
    if falling_box != None:
        falling_box.move()
        if falling_box.y<0:
            falling_box = None

    check_time()
    check_score()
    update_ball()

def display():
    global falling_box
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Hill
    draw_hill()
    draw_background()
    # draw_city_background()
    
    draw_bricks()
    draw_paddle()
    draw_score()
    draw_time()
    draw_ball()
    if falling_box != None:
        falling_box.draw()

def displayKO():
    global newDig
    x_center = W_height//2 + 70
    y_center = W_width//2 - 30
    
    glColor3f(1,1,1)
    #G
    x = Number(x_center-50,y_center, 10)
    x.draw()
    #A
    x = Number(x_center-30,y_center, 11)
    x.draw()
    #M
    x = Number(x_center-10,y_center, 12)
    x.draw()
    draw_line(x_center-15,y_center+8,x_center-5,y_center+8)
    #E
    x = Number(x_center+10,y_center, 13)
    x.draw()
    #O
    x = Number(x_center+40,y_center, 0)
    x.draw()
    #V
    draw_line(x_center+60,y_center-10,x_center+55,y_center+10)
    draw_line(x_center+60,y_center-10,x_center+65,y_center+10)
    #E
    x = Number(x_center+80,y_center, 13)
    x.draw()
    #R
    x = Number(x_center+100,y_center, 14)
    x.draw()
    draw_line(x_center+100,y_center,x_center+108,y_center+10)
    
    y_center -= 50
    x_center += 65
    #R
    x = Number(x_center-100,y_center, 14)
    x.draw()
    draw_line(x_center-100,y_center,x_center-92,y_center+10)
    #E
    x = Number(x_center-80,y_center, 13)
    x.draw()
    #S
    x = Number(x_center-60,y_center, 5)
    x.draw()
    #T
    draw_line(x_center-45,y_center+10,x_center-35,y_center+10)
    draw_line(x_center-40,y_center+10,x_center-40,y_center-10)
    #A
    x = Number(x_center-20,y_center, 11)
    x.draw()
    #R
    x = Number(x_center,y_center, 14)
    x.draw()
    draw_line(x_center,y_center,x_center+8,y_center+10)
    #T
    draw_line(x_center+15,y_center+10,x_center+25,y_center+10)
    draw_line(x_center+20,y_center+10,x_center+20,y_center-10)
    
    y_center -= 60
    x_center += 10
    
    #S
    x = Number(x_center-100,y_center, 5)
    x.draw()
    #C
    x = Number(x_center-80,y_center, 15)
    x.draw()
    #O
    x = Number(x_center-60,y_center, 0)
    x.draw()
    #R
    x = Number(x_center-40,y_center, 14)
    x.draw()
    draw_line(x_center-40,y_center,x_center-32,y_center+10)
    #E
    x = Number(x_center-20,y_center, 13)
    x.draw()
    
    newDig = [x_center,y_center-50]
    check_score()
    draw_score()
    
    
    
    

def displaymenu():
    x_center = W_height//2+50
    y_center = W_width//2
    
    glColor3f(1,1,1)
    draw_circle(x_center-100, y_center,50,(1,1,1))
    draw_line(x_center+30,y_center+35,x_center-20,y_center-35,20)
    draw_line(x_center+30,y_center-35,x_center-20,y_center+35,20)
    
    glColor3f(0,0,0)
    draw_line(x_center-140,y_center+50,x_center-140,y_center-50,50)
    
    glColor3f(1,1,1)
    one = Number(W_width-200,200,1,10)
    one.draw()
    two = Number(W_width-200,150,2,10)
    two.draw()
    three = Number(W_width-200,100,3,10)
    three.draw()

def intializeLevel():
    global level0,levelblocks,brick_height,brick_width,bricks,W_height,W_width,paddleobj,paddle_height,paddle_width,paddle_x,paddle_y
    leftp = (W_width-len(level0[0])*(brick_width+5))//2
    for y in range(len(level0)):
        for x in range(len(level0[0])):
            if level0[y][x] == 0:
                continue
            elif level0[y][x] != 3:
                levelblocks += 1
            xp = leftp + x*(brick_width+5)
            yp = W_height - 100 - y*(brick_height+5)
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
    if scene == 1:
        display()
    elif scene == 0:
        displaymenu()
    elif scene == 2:
        displayKO()
    glutSwapBuffers()

def timer(value):
    if not paused and scene==1:
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
glutKeyboardFunc(keyboard)
glutPassiveMotionFunc(mouse_motion)
glutMouseFunc(Click)
glutTimerFunc(16, timer, 0) 

glutMainLoop()
