from maze import Maze
from PIL import Image, ImageDraw
from random import random
from math import sin,cos
from sys import exit

def main():
    config = load_config()
    print(config)
    width = int(config[0])
    height = int(config[1])
    border = int(config[2])
    length = int(config[3])
    difficulty = max(min(int(config[4]),100),0)
    solve = config[5] == 1
    gen_type = int(config[6])
    file = config[7]

    mask = Image.open(file).convert("RGB")
    width,height = mask.size
    image = Image.new("RGB", (width*length + 2*border,height*length + 2*border),
                      color="#0D0221")
    drawer = ImageDraw.Draw(image)

    # 0 - random
    # 1 - sin based
    # 2 - modulus
    # 3 - mask
    gen = [lambda c: random(),
           lambda c: 2 * random() * sin(c[0] / 10) + c[0],
           lambda c: (c[0] * c[1]) % 12 + c[0] + random()*1.5,
           lambda c: c[1] if get_brightness(mask, c) < 0.5 else c[0]*random()]
    
    maze = Maze(width, height, gen[gen_type])
    print("generated")
    maze.draw(drawer, length, border)
    image.save("maze.png", "png")
    print("saved")
    if solve:
        path = maze.solve((0,0), (width-1,height-1))
        print("solved")
        maze.draw_path(path, drawer, length, border)
        image.save("maze_solved.png", "png")
        print("saved")

def load_config(file="default.conf"):
    return [line.split("=")[1].strip() for line in open(file)]


def get_brightness(i, xy):
    r,g,b = i.getpixel(xy)
    luminance = (0.2126*r) + (0.7152*g) + (0.0722*b)
    return luminance/255

if __name__ == '__main__':
    main()
