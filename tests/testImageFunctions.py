from cropping_package.CroppingImplementation.image import *
import random
import cv2


def test_get_shrunken_image():
    img = cv2.imread('MyImageFolder/schoolwork.jpg')

    assert(not img is None)
    scale = 3
    shrunken_img = get_shrunken_image(img, scale)

    h0, w0 = img.shape[:2]
    h1, w1 = shrunken_img.shape[:2]
    assert(scale*(h1-1) <= h0 <= scale * (h1 +1))               # the height of the shrunken image should be 1/scale of the initial image
    assert (scale * (w1 - 1) <= w0 <= scale * (w1 + 1))
    assert(np.allclose(shrunken_img[0,0,:], img[0,0,:]))        # the rgb-values of the first pixel for both images should be identical


def test_draw_marked_rectangle():
    img = np.zeros((300,300,3), np.uint8)
    background_color = (205,200,200)
    img[:,:] = background_color
    draw_marked_rectangle(img, 40,50, 250, 260)              # draws a rectangle that is 50 % original color and 50 % blue
    assert(np.allclose(img[50,39], background_color))        # outside of the marked region the color should still have its original value
    assert (np.allclose(img[50,41], (230, 100,100)))         #  inside the marked rectangle the color should be the average of blue and the original color
    assert (np.allclose(img[259, 249], (230, 100, 100)))     # the color should be ((205+255)/2, (200+0)/2, (200+0)/2) = (230,100,100)
    assert (np.allclose(img[261, 251], background_color))    # (x=251, y = 261) is outside of the rectangle and should have its original color (backround_color)


def test_get_rectangle():


    p1 = (10, 10)
    p2 = (20, 30)
    min_x, min_y, width, height = get_rectangle(p1, p2)
    assert(min_x == 10 and min_y == 10 and width == 11 and height == 21)


    for _ in range(20):
        x1 = random.randint(0,500)
        y1 = random.randint(0,500)

        x2 = random.randint(0,500)
        y2 = random.randint(0, 500)

        rect1 = get_rectangle((x1,y1), (x2, y2))
        rect2 = get_rectangle((x2,y2), (x1, y1))

        min_x_1, min_y_1, width_1, height_1 = rect1
        min_x_2, min_y_2, width_2, height_2 = rect2

        assert(min_x_1 == min_x_2 and min_y_1 == min_y_2 and width_1 == width_2 and height_1 == height_2)
        assert(width_1 >= 1 and height_1 >= 1)


def test_get_distance():
    x1, y1 = 10,10
    x2, y2 = 13, 14
    dist = get_distance((x1,y1), (x2,y2))
    assert(4.99999 < dist <5.0001)


def test_get_corner_points_from_rectangle():
    def test():
        x_min = random.randint(0, 100)
        y_min = random.randint(0, 100)

        width = random.randint(1, 100)
        height = random.randint(1, 100)

        rectanlge = (x_min, y_min, width, height)
        p1, p2 = get_corner_points_from_rectangle(rectanlge)
        x1, y1 = p1
        x2, y2 = p2

        assert(x1 == x_min and y1 == y_min and x2 == (x_min + width -1) and y2 == (y_min + height -1))

    for i in range(10):
        test()


def test_rotate90():
    # the rotation is counter-clockwise
    # checks that the corresponding position in the rotated matrix has the same value at a given position as the point in the original image
    h0, w0 = 7, 15

    # position in original image
    old_x = 5
    old_y = 6

    img = np.zeros((h0, w0, 3), np.uint8)
    img[:,:] = (0,0,0)

    img[old_y,old_x] = [150,50,100]
    new_img = rotate90(img)

    # corresponding position in new image
    new_y = w0 - 1 - old_x
    new_x = old_y
    assert(np.array_equal(new_img[new_y,new_x], img[old_y, old_x]))



def test_calculate_scaling():
    img = cv2.imread('MyImageFolder/schoolwork.jpg')
    screen_resolution = (1280, 720)
    scale = calculate_scaling(img, screen_resolution)
    assert(scale == 2)

    new_screen_resolution = (1920, 1080)
    scale = calculate_scaling(img, new_screen_resolution)
    assert (scale == 1)






