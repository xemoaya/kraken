from global_cfg import *

class Grid :
    def __init__(self, x = 0, y = 0) :
        self.x = x
        self.y = y
        self.occupied = False
        self.type = "normal"

def judge_same_grid(x1, x2, y1, y2) :
        global grid_width
        return abs(x1 - x2) < grid_width / 2 and abs(y1 - y2) < grid_width / 2

def judge_next_grid(x1, x2, y1, y2) :
        global grid_width
        #print (x1, x2, y1, y2) 
        if abs(x1 - x2) < 1 and abs (abs(y1 - y2) - grid_width) < 1: #same x
            return True
        if abs(y1 - y2) < 1 and abs (abs(x1 - x2) - grid_width) < 1: #same y
            return True
        return False

class BoardGrid :
    def __init__(self) :
        self.grids = []
        global basic_x, basic_y, grid_width
        for i in range(7) :
            for j in range(7) :
                nx, ny = basic_x + grid_width * i, basic_y + grid_width * j
                self.grids.append(Grid(nx, ny) )


    def occupy(self, x, y) :
        for grid in self.grids :
            if judge_same_grid(grid.x, x, grid.y, y):
                grid.occupied = True

    def unoccupy(self, x, y) :
        for grid in self.grids :
            if judge_same_grid(grid.x, x, grid.y, y):
                grid.occupied = False

    def check_occupy(self, x, y) : 
        for grid in self.grids :
            if judge_same_grid(grid.x, x, grid.y, y) :
                return grid.occupied
    
    def get_grid(self, x, y):
        global grid_width
        for grid in self.grids :
            if judge_same_grid(grid.x, x, grid.y, y):
                return grid.x, grid.y
        return -2 * grid_width, -2 * grid_width

    def set_grid_type(self, x, y, tp):
        for grid in self.grids :
            if judge_same_grid(grid.x, x, grid.y, y):
                grid.type = tp

    def get_grid_type(self, x, y):
        for grid in self.grids :
            if judge_same_grid(grid.x, x, grid.y, y):
                return grid.type



