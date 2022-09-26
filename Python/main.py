from infinitygrid import Inf_grid

grid = Inf_grid(0)

def check_cells(x, y):
    cells = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]
    total = 0
    for cell in cells:
        total += grid.get(*cell)
    return total


def to_check_key(x, y):
    return grid.get(x, y) or check_cells(x, y) > 0


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

grid.set(1, 0, 1)
grid.set(2, 1, 1)
grid.set(0, 2, 1)
grid.set(1, 2, 1)
grid.set(2, 2, 1)

def def_key(x, y):
    return grid.get(x, y) == 'meow'

while True:
    before = len(grid.data)
    grid.snippet(*grid.get_area()).graph()
    iterate()
    input(f'----{before}----')