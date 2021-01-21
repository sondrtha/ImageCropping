import numpy as np
import copy
import math

def get_shrunken_image(img, scale):
    assert(type(scale) == int and scale > 0)
    h,w = img.shape[:2]
    shrunk_img = img[:h:scale, :w:scale]
    shrunk_img = shrunk_img.copy()
    return shrunk_img

def copy_img(img):
    new_img = copy.copy(img)
    return new_img


def draw_marked_rectangle(img,  min_x, min_y, max_x, max_y, color = (255,0,0)):
    img[min_y:max_y,min_x:max_x] = (color + img[min_y:max_y,min_x:max_x])/2


def get_rectangle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)
    width  = max_x - min_x + 1
    height = max_y - min_y + 1
    return (min_x, min_y, width, height)

def get_corner_points_from_rectangle(rectangle):
    min_x, min_y, width, height = rectangle
    p1 = (min_x, min_y)
    p2 = (min_x + width -1, min_y + height -1)
    return ((p1, p2))

def get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    dist = math.sqrt((dx * dx + dy * dy))
    return dist

def rotate90(matrix):
    return np.rot90(matrix)
