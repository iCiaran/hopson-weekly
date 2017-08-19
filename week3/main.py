from maze import Maze
from PIL import Image, ImageDraw
from random import random
from math import sin,cos
from sys import exit

def main():
    # Super basic config loading
    config = load_config()
    width = int(config[0])
    height = int(config[1])
    border = int(config[2])
    length = int(config[3])
    difficulty = max(min(int(config[4]),100),1)
    solve = int(config[5]) == 1
    gen_type = int(config[6])
    file = config[7]
    background_colour = config[8]
    wall_colour = config[9]
    path_colour = config[10]

    # Load in image mask and resize to width and height
    mask = Image.open(file).convert("RGB").resize((width, height))

    # Create the image to draw to
    image = Image.new("RGB", (width*length + 2*border,height*length + 2*border),
                      color=background_colour)
    drawer = ImageDraw.Draw(image)

    # Generation Functions
    # 0 - random
    # 1 - mask
    # 2 - modulus
    gen = [lambda c: c[0] + random()* (1+difficulty/20),
           lambda c: c[1] if get_brightness(mask, c) < 0.5 else (c[0]+random()*(1+difficulty/20)),
           lambda c: (c[0] * c[1]) % 10 + c[0] + random()*1.5]
    
    # Generate and draw maze to image
    maze = Maze(width, height, gen[gen_type])
    print("Generated Maze")
    maze.draw(drawer, length, border, wall_colour)
    
    # Save maze image without solution
    image.save("maze.png", "png")
    print("Saved Maze")


    if solve:
        # Solve maze and draw path
        path = maze.solve((0,0), (width-1,height-1))
        print("Solved Maze")
        maze.draw_path(path, drawer, length, border, path_colour)

        # Save maze image with solution
        image.save("maze_solved.png", "png")
        print("Saved Maze With Solution")

def load_config(file="default.conf"):
    '''Return a list of config values'''
    return [line.split("=")[1].strip() for line in open(file)]


def get_brightness(i, xy):
    '''Get human perceived brightness of a pixel'''
    r,g,b = i.getpixel(xy)
    luminance = (0.2126*r) + (0.7152*g) + (0.0722*b)
    return luminance/255

if __name__ == '__main__':
    main()
