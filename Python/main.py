import pygameextra as pe
import pygameextra.settings
import time
from infinitygrid import Inf_grid

pe.init()
grid = Inf_grid(0)
pe.display.make((600, 600), "Life")

# Init data
scale = 15
color_active = (0, 0, 0)
color_inactive = (255, 255, 255)
color_grid = (180, 180, 180)
running = False
offset = (0, 0)
time_to_run = 0.03
time_waiting = 0
trans = 75

# Init images
play_button = pe.Image('icons1.png', (35, 35))
play_button_active = pe.Image('icons2.png', (35, 35))
pause_button = pe.Image('icons3.png', (35, 35))
pause_button_active = pe.Image('icons4.png', (35, 35))
iterate_button = pe.Image('icons5.png', (35, 35))
iterate_button_active = pe.Image('icons6.png', (35, 35))
edit_button = pe.Image('icons7.png', (35, 35))
edit_button_active = pe.Image('icons8.png', (35, 35))


def check_cells(x, y):
    cells = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]
    total = 0
    for cell in cells:
        total += grid.get(*cell)
    return total


def iterate():
    global grid
    # fewer than 2 - dies
    # 2 or 3 - lives
    # more than 3 - dies
    # 3 - becomes
    new = grid.copy()
    to_check = set()
    for coordinate in grid.data:
        to_check.add(coordinate)
        to_check.add((coordinate[0]-1, coordinate[1]-1))
        to_check.add((coordinate[0], coordinate[1]-1))
        to_check.add((coordinate[0]+1, coordinate[1]-1))
        to_check.add((coordinate[0]-1, coordinate[1]))
        to_check.add((coordinate[0]+1, coordinate[1]))
        to_check.add((coordinate[0]-1, coordinate[1]+1))
        to_check.add((coordinate[0], coordinate[1]+1))
        to_check.add((coordinate[0]+1, coordinate[1]+1))
    for check in to_check:
        if not grid.get(*check):
            if check_cells(*check) == 3:
                new.set(*check, 1)
            continue
        if check_cells(*check) < 2: new.reset(*check)
        elif check_cells(*check) > 3: new.reset(*check)
    grid = new


def center():
    global offset
    offset = pe.math.center(grid.get_area())


grid.set(1, 0, 1)
grid.set(2, 1, 1)
grid.set(0, 2, 1)
grid.set(1, 2, 1)
grid.set(2, 2, 1)


def switch(state: bool):
    global running
    running = state


while True:
    for pe.event.c in pe.event.get():
        pe.event.quitcheckauto()
    before_time = time.time()
    pe.fill.transparency(color_inactive, trans)
    center_of_screen = pe.math.center((0, 0, *pe.display.get_size()))
    real_offset = (center_of_screen[0] - offset[0]*scale, center_of_screen[1] - offset[1]*scale)
    for tile in grid.data:
        pe.draw.rect(color_active, (real_offset[0] + tile[0]*scale, real_offset[1] + tile[1]*scale, scale, scale))
    if not running and pe.mouse.pos()[1]> 50:
        mouse = pe.mouse.pos()
        mouse_tile = int((mouse[0] - real_offset[0]) / scale) -1, int((mouse[1] - real_offset[1]) / scale) -1

        pe.draw.rect(color_grid, (real_offset[0] + mouse_tile[0] * scale, real_offset[1] + mouse_tile[1] * scale, scale, scale), int(scale*.25))
        if pe.mouse.clicked()[0] and not pe.settings.button_lock:
            if grid.get(*mouse_tile):
                grid.reset(*mouse_tile)
            else:
                grid.set(*mouse_tile, 1)
            pe.button.lock()



    # Menu
    if running:
        pe.button.image((10, 10, 35, 35), pause_button, pause_button_active, action=switch, data=False)
        #pe.button.image((55, 10, 35, 35), edit_button, edit_button_active)
    else:
        pe.button.image((10, 10, 35, 35), play_button, play_button_active, action=switch, data=True)
        pe.button.image((55, 10, 35, 35), iterate_button, iterate_button_active, action=iterate)
        #pe.button.image((100, 10, 35, 35), edit_button, edit_button_active)
        time_waiting = 0
    time_waiting += time.time()-before_time
    if time_waiting >= time_to_run:
        time_waiting = 0
        iterate()
    pe.display.update(60)