import OpenGL.GL as gl
import OpenGL.GLUT as glut
import sys
import math

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0)
GRAY = (0.5, 0.5, 0.5)
HIGHLIGHT = (0.6, 0.6, 0.6)

def midpoint_circle(cx, cy, radius):
    """Midpoint circle drawing algorithm."""
    x = 0
    y = radius
    d = 1 - radius

    points = []

    while x <= y:
        points.extend([
            (cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x), (cx + y, cy - x), (cx - y, cy - x)
        ])
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

    return points

def midpoint_line(x0, y0, x1, y1):
    """Midpoint line drawing algorithm."""
    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return points

def draw_text_with_points(x, y, text, size):
    """Draw pixelated text using points."""
    offset_x = x
    for char in text:
        char_pattern = get_char_pattern(char)
        for px, py in char_pattern:
            draw_pixel(offset_x + px * size, y - py * size, size)
        offset_x += (4 * size)  # Adjust spacing for better alignment

def get_char_pattern(char):
    """Return a pixel pattern for a given character."""
    patterns = {
        'R': [(0, 0), (0, 1), (0, 2), (1, 2), (2, 1), (1, 1), (2, 0)],
        'E': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 2)],
        'S': [(0, 0), (0, 1), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
        'U': [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1), (2, 2)],
        'M': [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)],
        'T': [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)],
        'A': [(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2)],
        ' ': []
    }
    return patterns.get(char.upper(), [])

def draw_pixel(x, y, size):
    """Draw a pixel as a square at the given position, mapped to OpenGL coordinates."""
    x = (x / SCREEN_WIDTH) * 2 - 1
    y = (y / SCREEN_HEIGHT) * 2 - 1
    size_x = (size / SCREEN_WIDTH) * 2
    size_y = (size / SCREEN_HEIGHT) * 2

    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(x, y)
    gl.glVertex2f(x + size_x, y)
    gl.glVertex2f(x + size_x, y - size_y)
    gl.glVertex2f(x, y - size_y)
    gl.glEnd()

def render():
    """Render the scene."""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    # Draw decorations
    gl.glColor3f(*WHITE)
    circle_points = midpoint_circle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, 100)
    gl.glBegin(gl.GL_POINTS)
    for x, y in circle_points:
        gl.glVertex2f(x / SCREEN_WIDTH * 2 - 1, y / SCREEN_HEIGHT * 2 - 1)
    gl.glEnd()

    line_points = midpoint_line(100, 500, 700, 500)
    gl.glBegin(gl.GL_POINTS)
    for x, y in line_points:
        gl.glVertex2f(x / SCREEN_WIDTH * 2 - 1, y / SCREEN_HEIGHT * 2 - 1)
    gl.glEnd()

    # Draw menu options
    gl.glColor3f(*HIGHLIGHT)
    draw_text_with_points(100, 400, "RESUME", 10)
    draw_text_with_points(100, 350, "RESTART", 10)
    draw_text_with_points(100, 300, "EXIT", 10)

    glut.glutSwapBuffers()


def check_button_click(x, y):
    global is_paused
    if 10 <= x <= 50 and height - 40 <= y <= height - 10:
        restart_game()
    elif 60 <= x <= 100 and height - 40 <= y <= height - 10:
        is_paused = not is_paused
        print("Game Paused" if is_paused else "Game Resumed")
    elif 110 <= x <= 150 and height - 40 <= y <= height - 10:
        print(f"Goodbye! Final Score: {score}")
        glutLeaveMainLoop()

def main():
    """Main function."""
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB)
    glut.glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glut.glutCreateWindow(b"Pause Menu Example")
    gl.glClearColor(*GRAY, 1.0)
    glut.glutDisplayFunc(render)
    glut.glutIdleFunc(render)
    glut.glutMainLoop()

if __name__ == "__main__":
    main()
