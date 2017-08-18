from random import random
from collections import deque

class Maze:

    def __init__(self, width, height, gen=lambda c: random()):
        self._cells = []
        self._w = width
        self._h = height
        self._gen = gen
        self.generate()

    def find_neighbours(self,x,y):
        neighbours = []
        if x > 0:
            neighbours.append((x-1, y))
        if x < self._w - 1:
            neighbours.append((x+1, y))
        if y > 0:
            neighbours.append((x, y-1))
        if y < self._h - 1:
            neighbours.append((x, y+1))
        return [n for n in neighbours if not self._cells[n[0]][n[1]]._visited]

    def generate(self):
        self._cells = [[Cell(x, y) for y in range(self._h)] for x in range(self._w)]
        self._cells[0][0]._visited = True

        unexplored = self._w * self._h - 1

        xy = (0,0)
        stack = [(0,0)]

        while unexplored > 0:
            neighbours = self.find_neighbours(xy[0], xy[1])
            if len(neighbours) > 0:
                cell = sorted(neighbours, key=self._gen)[0]
                stack.append(xy)
                self.remove_walls(cell, stack[-1])
                xy = cell
                self._cells[xy[0]][xy[1]]._visited = True
                unexplored -= 1
            else:
                xy = stack.pop()

    def remove_walls(self,a,b):
        if a[0] > b[0]:     #a to right
            self._cells[a[0]][a[1]]._sides -= 4
            self._cells[b[0]][b[1]]._sides -= 8
        if a[0] < b[0]:     #a on left
            self._cells[a[0]][a[1]]._sides -= 8
            self._cells[b[0]][b[1]]._sides -= 4
        if a[1] > b[1]:     #a below
            self._cells[a[0]][a[1]]._sides -= 1
            self._cells[b[0]][b[1]]._sides -= 2
        if a[1] < b[1]:      #a above
            self._cells[a[0]][a[1]]._sides -= 2
            self._cells[b[0]][b[1]]._sides -= 1

    def draw(self, d, length, border, colour):
        for x in range(self._w):
            for y in range(self._h):
                self._cells[x][y].draw(d, length, border, colour)

    def find_possible_with_direction(self, direction, xy, first):
        if first:
            tocheck = [0,1,2,3]
        else:
            tocheck = [direction, (direction+1)%4, (direction-1)%4]
        x,y = xy
        possible = []
        for n in tocheck:
            if n == 0:
                if self._cells[x][y]._sides & 1 == 0 and y > 0:              #top
                    possible.append(0)
            elif n == 1:
                if self._cells[x][y]._sides & 8 == 0 and x < self._w - 1:    #right
                    possible.append(1)
            elif n == 2:
                if self._cells[x][y]._sides & 2 == 0 and y < self._h - 1:    #bottom
                    possible.append(2)
            else:
                if self._cells[x][y]._sides & 4 == 0 and x > 0:              #left
                    possible.append(3)
        return possible

    def get_next_cell(self, direction, xy):
        x, y = xy
        if direction == 0:
            return (x, y-1)
        elif direction == 1:
            return (x+1, y)
        elif direction == 2:
            return (x, y+1)
        else:
            return (x-1, y)

    def get_coord_path(self, direction_path, xy):
        path = [xy]
        for d in direction_path:
            next_cell = self.get_next_cell(d, xy)
            path.append(next_cell)
            xy = next_cell
        return path

    def solve(self, start, end):
        queue = deque()
        queue.append((start, 1, []))
        first = True
        while queue:
            (xy, direction, path) = queue.popleft()
            if first:
                possible = self.find_possible_with_direction(direction, xy, first)
                first = False
            else:
                possible = self.find_possible_with_direction(direction, xy, first)
            for d in possible:
                next_cell = self.get_next_cell(d, xy)
                if next_cell == end:
                    return self.get_coord_path(path + [d], start)
                else:
                    queue.append((next_cell, d, path+[d]))

    def draw_path(self, path, d, l, b, c):
        for i in range(len(path)-1):
            half_l = l/2
            start_x = path[i][0] * l + b + half_l
            start_y = path[i][1] * l + b + half_l
            end_x = path[i+1][0] * l + b + half_l
            end_y = path[i+1][1] * l + b + half_l
            d.line([(start_x,start_y),(end_x,end_y)], fill=c, width=1)


class Cell:
    
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._sides = 15
        self._visited = False

    def draw(self, d, l, b, colour):
        top_left = (self._x * l + b, self._y * l + b)
        top_right = (self._x * l + b + l, self._y * l + b)
        bot_left = (self._x * l + b, self._y * l + b + l)
        bot_right = (self._x * l + b + l, self._y * l + b + l)
        if self._sides & 1 == 1:    #top
            d.line([top_left, top_right], fill=colour, width=0)
        if self._sides & 2 == 2:    #bottom
            d.line([bot_left, bot_right], fill=colour, width=0)
        if self._sides & 4 == 4:    #left
            d.line([top_left, bot_left], fill=colour, width=0)
        if self._sides & 8 == 8:    #right
            d.line([top_right, bot_right], fill=colour, width=0)

