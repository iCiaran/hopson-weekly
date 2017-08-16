from maze import Maze
from PIL import Image, ImageDraw
from random import random

def main():
    width = 30
    height = 25
    border = 10
    length = 8
    difficulty = 100

    image = Image.new("RGB", (width*length + 2*border,height*length + 2*border),
                      color="#0D0221")
    drawer = ImageDraw.Draw(image)

    # maze = Maze(width, height, gen=lambda c: (c[0] * c[1]) % 12 + c[0] + random()*1.5)
    maze = Maze(width, height)
    print("generated")
    maze.draw(drawer, length, border)
    image.save("maze.png", "png")
    print("saved")
    
    path = maze.solve((0,0), (width-1,height-1))
    print("solved")
    maze.draw_path(path, drawer, length, border)
    image.save("maze_solved.png", "png")
    print("saved")

if __name__ == '__main__':
    main()
