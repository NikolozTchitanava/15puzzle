import turtle
import random

GRID_SIZE = 4
CELL_SIZE = 50
EMPTY_CELL = -1

matrix = [[(GRID_SIZE * i + j) + 1 for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
matrix[-1][-1] = EMPTY_CELL

def color_cell(row, col, color):
    turtle.hideturtle()
    turtle.penup()
    start_x = -CELL_SIZE * GRID_SIZE / 2 + col * CELL_SIZE
    start_y = CELL_SIZE * GRID_SIZE / 2 - (row) * CELL_SIZE
    turtle.goto(start_x, start_y)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(CELL_SIZE)
        turtle.right(90)
    turtle.end_fill()
    turtle.update()

def draw_grid():
    turtle.clear()
    turtle.speed(0)
    turtle.hideturtle()
    turtle.tracer(0, 0)
    turtle.bgcolor("purple")  
    
    start_x = -CELL_SIZE * GRID_SIZE / 2
    start_y = -CELL_SIZE * GRID_SIZE / 2
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = start_x + col * CELL_SIZE
            y = start_y + row * CELL_SIZE
            color_cell(row, col, "white")
            if matrix[row][col] != EMPTY_CELL:
                draw_number(row, col, matrix[row][col])
            else:
                color_cell(row, col, "purple")  

    turtle.update()

def draw_number(row, col, num):
    turtle.hideturtle()
    turtle.penup()
    x = -CELL_SIZE * GRID_SIZE / 2 + col * CELL_SIZE + (CELL_SIZE / 2)
    y = CELL_SIZE * GRID_SIZE / 2 - (row) * CELL_SIZE - (CELL_SIZE / 2)
    turtle.goto(x, y - 13)
    turtle.write(num, align="center", font=("Bagel Fat One", 80, "normal"))
    turtle.update()

def get_empty_cell():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if matrix[row][col] == EMPTY_CELL:
                return row, col

def is_adjacent(row1, col1, row2, col2):
    return (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1)

def click_handler(x, y):
    col = int((x + CELL_SIZE * GRID_SIZE / 2) // CELL_SIZE)
    row = int((-y + CELL_SIZE * GRID_SIZE / 2) // CELL_SIZE)
    empty_row, empty_col = get_empty_cell()

    if is_adjacent(row, col, empty_row, empty_col):
        matrix[row][col], matrix[empty_row][empty_col] = matrix[empty_row][empty_col], matrix[row][col]
        draw_grid()

def cells_around(direction):
    cells = []
    row, col = get_empty_cell()
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                cells.append((new_row, new_col))

    if direction == "up":
        for el in cells:
            if el[0] - 1 == row:
                matrix[el[0]][el[1]], matrix[el[0] - 1][el[1]] = matrix[el[0] - 1][el[1]], matrix[el[0]][el[1]]
        draw_grid()
    elif direction == "down":
        for el in cells:
            if el[0] + 1 == row:
                matrix[el[0]][el[1]], matrix[el[0] + 1][el[1]] = matrix[el[0] + 1][el[1]], matrix[el[0]][el[1]]
        draw_grid()
    elif direction == "left":
        for el in cells:
            if el[1] - 1 == col:
                matrix[el[0]][el[1]], matrix[el[0]][el[1] - 1] = matrix[el[0]][el[1] - 1], matrix[el[0]][el[1]]
        draw_grid()
    elif direction == "right":
        for el in cells:
            if el[1] + 1 == col:
                matrix[el[0]][el[1]], matrix[el[0]][el[1] + 1] = matrix[el[0]][el[1] + 1], matrix[el[0]][el[1]]
        draw_grid()

    return cells

def shuffle_board():
    for _ in range(1000):
        empty_row, empty_col = get_empty_cell()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                matrix[empty_row][empty_col], matrix[new_row][new_col] = matrix[new_row][new_col], matrix[empty_row][empty_col]
                break

screen = turtle.Screen()
screen.tracer(0)
screen.setworldcoordinates(-CELL_SIZE*GRID_SIZE/2, -CELL_SIZE*GRID_SIZE/2, CELL_SIZE*GRID_SIZE/2, CELL_SIZE*GRID_SIZE/2)

draw_grid()
shuffle_board()

turtle.onscreenclick(click_handler)

turtle.onkey(lambda: cells_around("up"), "Up")
turtle.onkey(lambda: cells_around("down"), "Down")
turtle.onkey(lambda: cells_around("left"), "Left")
turtle.onkey(lambda: cells_around("right"), "Right")

turtle.listen()

turtle.mainloop()
