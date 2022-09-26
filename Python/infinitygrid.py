import math

class Grid:
    width = 2
    height = 2
    length = 4
    array = []
    initiator = None

    def __init__(self, width: int, height: int, initiator: any = None):
        self.width = width
        self.height = height
        self.length = width * height
        self.array = [initiator] * self.length
        self.initiator = initiator

    def get(self, x: int, y: int):
        if x < 0 or y < 0 or x > self.width - 1 or y > self.height - 1:
            return None
        return self.array[x + (y * self.width)]

    def set(self, x: int, y: int, value: any):
        if x < 0 or y < 0 or x > self.width - 1 or y > self.height - 1:
            return
        self.array[x + (y * self.width)] = value
        if type(value) == GridObject:
            value.x = x
            value.y = y
    def graph(self, key: any = None):
        x, y = 0, 0
        while y < self.height:
            while x < self.width:
                if (key and key(x, y)) or (not key and self.get(x, y)):
                    print('■  ', end='')
                else:
                    print('□  ', end='')
                x += 1
            print('')
            y += 1
            x = 0

class GridObject:
    value = None
    grid = None
    x = 0
    y = 0

    def __init__(self, value: any, grid: Grid, x: int = 1, y: int = 1):
        self.value = value
        self.grid = grid
        self.x = x
        self.y = y

    def left(self):
        return self.grid.get(self.x-1, self.y)

    def right(self):
        return self.grid.get(self.x+1, self.y)

    def up(self):
        return self.grid.get(self.x, self.y-1)

    def down(self):
        return self.grid.get(self.x-1, self.y+1)

class Inf_grid:
    def __init__(self, default: any = None):
        self.data = {}
        self.default = default

    def get(self, x, y):
        if (x, y) in self.data:
            return self.data[(x, y)]
        return self.default

    def set(self, x, y, data: any = None):
        self.data[(x, y)] = data

    def reset(self, x, y):
        if (x, y) in self.data:
            del self.data[(x, y)]

    def snippet(self, start_x: int, start_y: int, width: int, height: int):
        snip = Grid(width, height, self.default)
        x, y = start_x, start_y
        while x < start_x + width:
            while y < start_y + height:
                snip.set(x-start_x, y-start_y, self.get(x, y))
                y += 1
            y = start_y
            x += 1
        return snip

    def copy(self, destination: 'Inf_grid' = None):
        if not destination:
            destination = Inf_grid()
        destination.default = self.default
        destination.data = self.data.copy()
        return destination

    def get_area(self):
        keys = list(self.data.keys())
        list_of_x = [x[0] for x in keys]
        list_of_y = [x[1] for x in keys]
        start = (min(list_of_x), min(list_of_y))
        end = (max(list_of_x), max(list_of_y))
        return *start, end[0]-start[0]+1, end[1]-start[1]+1
