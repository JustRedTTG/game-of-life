from infinitygrid import *

grid = Grid(5, 3, 0) # width, height, initiator
grid.set(1, 1, 'value') # width, height, value

print(grid.get(1, 1)) # 'value'
print(grid.get(2, 1)) # 0
print(grid.get(6, 10)) # None

grid.graph()

# value
# 0
# None
# □  □  □  □  □
# □  ■  □  □  □
# □  □  □  □  □