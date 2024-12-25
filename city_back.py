import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window dimensions
window_width = 800
window_height = 600

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

def setup():
    """
    OpenGL setup function.
    """
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    gluOrtho2D(-window_width, window_width, -window_height, window_height)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"City Background with Modular Design (Only GL_POINTS)")
    setup()
    glutDisplayFunc(draw_city_background)  # Only display once on window creation
    glutMainLoop()  # Starts the rendering loop (no mouse interaction here)


