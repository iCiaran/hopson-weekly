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

    def find_possible(self, xy):
        x,y = xy
        possible = []
        if self._cells[x][y]._sides & 1 == 0 and y > 0:    #top
            possible.append((x,y-1))
        if self._cells[x][y]._sides & 2 == 0 and y < self._h - 1:    #bottom
            possible.append((x,y+1))
        if self._cells[x][y]._sides & 4 == 0 and x > 0:    #left
            possible.append((x-1,y))
        if self._cells[x][y]._sides & 8 == 0 and x < self._w - 1:    #right
            possible.append((x+1,y))
        return possible

    def solve(self, start, end):
        queue = deque()
        queue.append((start,[start]))
        while queue:
            (vertex, path) = queue.popleft()
            possible = [n for n in self.find_possible(vertex) if n not in path]
            for x in possible:
                if x == end:
                    return path+[x]
                else:
                    queue.append((x,path + [x]))

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

