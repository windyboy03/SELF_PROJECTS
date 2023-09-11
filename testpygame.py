import pygame
import sys
import numpy as np

pygame.init()

# Constants
WINDOW_SIZE = (1920, 1080)
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
RECTANGLE_COLOR = (166, 255, 150)
GRID_COLOR = (248, 255, 149)
GRID_SPACING = 50
LINE_WIDTH = 2
MENU_COLOR = (188, 122, 249)
MENU_FONT_SIZE = 36
MENU_ITEM_HEIGHT = 50


# Create window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Draw Rectangles")

# Font
font = pygame.font.Font(None, 36)

# Mouse pos to draw rectangle
start_pos = None
end_pos = None
drawing = False
rect = False
selected_item = 0
selected_text = None
rectangles = []

# User input
t1_input = 0.0
t2_input = 0.0
angle_input = 0.0
W_input = 1.0
H_input = 1.0
destination_points = []

# Menu items
menu_items = [
    "Translation ",
    "Rotation ",
    "Scaling ",
    "Perspective",
    "Apply"
]
# Function translate
def translate(polygon, t1, t2):
    polygon = np.matrix(polygon).T
    T = np.array([[1, 0, t1],
                  [0, 1, t2],
                  [0, 0, 1]])
    new_polygon = T * polygon
    return new_polygon
# Function rotate
def rotate(polygon, angle):
    angle = np.radians(angle)
    R = np.array([[np.cos(angle), -np.sin(angle), 0],
                  [np.sin(angle), np.cos(angle), 0],
                  [0, 0, 1]])
    new_polygon = R * polygon
    return new_polygon
# Function scale
def scale(polygon, w, h):
    S = np.array([[w, 0, 0],
                  [0, h, 0],
                  [0, 0, 1]])
    new_polygon = np.matmul(S, polygon)
    return new_polygon
# Function perspective
def perspective(polygon, destination_points):
    if len(destination_points) != 4:
        raise ValueError("Destination points should have 4 points")
    polygon = np.array(polygon)
    polygon = polygon.T
    A = np.zeros((8, 8))
    b = np.zeros((8, 1))

    for i in range(4):
        x, y, z = polygon[i]
        u, v = destination_points[i]

        A[i] = [x, y, 1, 0, 0, 0, -x * u, -y * u]
        A[i + 4] = [0, 0, 0, x, y, 1, -x * v, -y * v]

        b[i] = u
        b[i + 4] = v

    coefficients = np.linalg.solve(A, b)
    matrix = np.vstack((coefficients, np.array([1])))
    matrix = matrix.reshape((3, 3))
    new_polygon = np.matmul(matrix, polygon.T)
    print(f"Perspective matrix: {matrix}")
    return new_polygon

# Function draw the grid and coordinate
def draw_grid():
    # Draw the grid lines
    for i in range(-WINDOW_SIZE[0] // 2 // GRID_SPACING, WINDOW_SIZE[0] // 2 // GRID_SPACING + 1):
        pygame.draw.line(screen, GRID_COLOR, (i * GRID_SPACING + WINDOW_SIZE[0] // 2, 0),
                         (i * GRID_SPACING + WINDOW_SIZE[0] // 2, WINDOW_SIZE[1]), 1)
    for i in range(-WINDOW_SIZE[1] // 2 // GRID_SPACING, WINDOW_SIZE[1] // 2 // GRID_SPACING + 1):
        pygame.draw.line(screen, GRID_COLOR, (0, i * GRID_SPACING + WINDOW_SIZE[1] // 2),
                         (WINDOW_SIZE[0], i * GRID_SPACING + WINDOW_SIZE[1] // 2), 1)
    # Draw Ox and Oy
    pygame.draw.line(screen, LINE_COLOR, (0, WINDOW_SIZE[1] // 2), (WINDOW_SIZE[0], WINDOW_SIZE[1] // 2), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (WINDOW_SIZE[0] // 2, 0), (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1]), LINE_WIDTH)
# Function draw polygons
def draw_polygon(points, start_pos, end_pos):
    # Draw grid same time with polygon 
    draw_grid()
    
    for point in points:
        translated_points = [(x + WINDOW_SIZE[0] // 2, y + WINDOW_SIZE[1] // 2) for x, y in point]
        pygame.draw.polygon(screen, RECTANGLE_COLOR, translated_points)

    if start_pos is not None and end_pos is not None:
        translated_start = (start_pos[0], start_pos[1])
        translated_end = (end_pos[0] , end_pos[1] )
        pygame.draw.polygon(screen, RECTANGLE_COLOR, [(translated_start[0], translated_start[1]),
                                                      (translated_end[0], translated_start[1]),
                                                      (translated_end[0], translated_end[1]),
                                                      (translated_start[0], translated_end[1])])

# Function convert homogeneous coordinates to cartesian coordinates
def homo_to_cart(polygon):
    polygon = np.array(polygon)
    new_polygon = polygon[..., :-1] / polygon[..., -1, None]
    return new_polygon

# Function convert cartesian coordinates to homogeneous coordinates
def cart_to_homo(polygon):
    polygon = np.array(polygon)
    homo_polygon = np.column_stack((polygon, np.ones(len(polygon))))
    return homo_polygon



# Function display menu
def display_menu(selected_item):
    for i, item in enumerate(menu_items):
        text = font.render(item, True, LINE_COLOR if i != selected_item else (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.topleft = (MENU_ITEM_HEIGHT, (i + 1) * MENU_ITEM_HEIGHT)
        screen.blit(text, text_rect)
# Main loop
while True:
    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:# Quit when clicks the X button
            pygame.quit()
            sys.exit()
        
        # Check if start draw by mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get the start pos
            if not drawing:
                drawing = True
                start_pos = event.pos
        elif event.type == pygame.MOUSEMOTION:
            # get the end pos
            if drawing:
                end_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False
                end_pos = event.pos
                x1, y1 = start_pos 
                x2, y2 = end_pos 
                # get 4 points of rectangle
                point_pos = [(x1 - WINDOW_SIZE[0] // 2, y1 - WINDOW_SIZE[1] // 2),
                             (x2 - WINDOW_SIZE[0] // 2, y1 - WINDOW_SIZE[1] // 2),
                             (x2 - WINDOW_SIZE[0] // 2, y2 - WINDOW_SIZE[1] // 2),
                             (x1 - WINDOW_SIZE[0] // 2, y2 - WINDOW_SIZE[1] // 2)]
                rectangles.append(point_pos)
                if len(rectangles) > 2: # just keep maximun 2 polegons on screen
                    rectangles.pop(0)
                # Reset start and end pos
                start_pos = None
                end_pos = None
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP:
                # Move item up
                selected_item = (selected_item - 1) % len(menu_items)
            elif event.key == pygame.K_DOWN:
                # Move item down
                selected_item = (selected_item + 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
             
                # selected function based on menu
                if selected_item == 0:
                    t1_input = float(input("Enter T1: "))
                    t2_input = float(input("Enter T2: "))
                    menu_items[0] = f"Translation with vector: T1:  {t1_input} , T2: {t2_input} "
                elif selected_item == 1:
                    angle_input = float(input("Enter angle: "))
                    menu_items[1] = f"Rotation with angle: {angle_input} "   
                elif selected_item == 2:
                    W_input = float(input("Enter W:" ))
                    H_input = float(input("Enter H:" ))
                    menu_items[2] = f"Scaling with: W: {W_input} , H: {H_input} "
                elif selected_item == 3:
                    destination_points = []
                    print("Enter 4 points: ")
                    for i in range(4):
                        x, y = map(float, input().split())
                        destination_points.append((x, y))

                    menu_items[3] = f"Perspective transform to: {str(destination_points)}"        
                elif selected_item == 4 and len(rectangles) > 0:
                    rectangles[-1] = cart_to_homo(rectangles[-1])  # Convert cartesian coordinates to homogeneous coordinates
                    rectangles[-1] = translate(rectangles[-1], t1_input, t2_input)
                    rectangles[-1] = rotate(rectangles[-1], angle_input)
                    rectangles[-1] = scale(rectangles[-1], W_input, H_input)
                    if len(destination_points) == 4:
                        rectangles[-1] = perspective(rectangles[-1], destination_points)
                    
                    rectangles[-1] = rectangles[-1].T      
                    rectangles[-1] = homo_to_cart(rectangles[-1])  # Convert homogeneous coordinates back to cartesian coordinates
    screen.fill(WHITE)  # clean window
    draw_polygon(rectangles, start_pos, end_pos)# draw polygon in main loop
    display_menu(selected_item)#draw menu in main loop
    pygame.display.flip()#update window
    