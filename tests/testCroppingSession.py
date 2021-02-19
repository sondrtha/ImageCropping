import os
import cv2
from collections import namedtuple
from cropping_package.CroppingImplementation.croppingSession import CroppingSession, UserImage
from utils import remove_out_files

# The tests in testImageFunctions and testUtils should preferably run before the tests in this file are run


def test_UserImage():
    img = cv2.imread('MyImageFolder/schoolwork.jpg')
    userImage = UserImage(img)

    screen_width, screen_height = userImage.screen_resolution
    assert(10000 > screen_width > 100)      # this test is to ensure that the screen resolution variable is set
    h, w = userImage.scaled_image.shape[:2]
    assert(0 < w <= screen_width)           # the scaled image should have a width less than the screen with
    assert(0 < h <= screen_height)


def test_create_list_of_user_images():
    path = 'MyImageFolder//'
    croppingSession = CroppingSession(path)
    # The method create_list_of_userimages is called in the __init__ -function for the croppingSession object
    imgs = croppingSession.images_to_be_cropped
    assert(len(imgs) == 4)
    for img in imgs:
        assert(type(img) == UserImage)


def test_CroppingSession_with_events():
    # start with removing all files already in the out folder
    remove_out_files()
    input_images_folder = 'MyImageFolder//'

    MouseEvent = namedtuple('MouseEvent',['event', 'x', 'y'])
    EVENT_LBUTTONDOWN = 1
    EVENT_LBUTTONUP = 4

    KeyEvent = namedtuple('KeyEvent', 'k')
    RIGHT_KEY = 2555904
    LEFT_KEY = 2424832
    ENTER_KEY = 13
    R_KEY = ord('r')

    croppingSession = CroppingSession(input_images_folder)

    def handle_event(event):
        if (type(event) == KeyEvent):
            croppingSession.key_handler(event.k)
        if (type(event) == MouseEvent):
            croppingSession.mouse_event_handling(event.event, event.x, event.y, None, None)

    handle_event(MouseEvent(event=EVENT_LBUTTONDOWN, x=10, y=10))       # start marking a region to crop in the image
    handle_event(MouseEvent(event=EVENT_LBUTTONUP, x=400, y=400))       # end marking the region to crop in the image
    handle_event(KeyEvent(k=RIGHT_KEY))                                 # go to the next userImage in the list of images

    assert(len(croppingSession.marked_rectangles_dict) == 1)        # at this point there should be one marked rectanlge

    handle_event(MouseEvent(event=EVENT_LBUTTONDOWN, x=10, y=10))
    handle_event(MouseEvent(event=EVENT_LBUTTONUP, x=510, y=510))

    assert (len(croppingSession.marked_rectangles_dict) == 2)       # at this point there should be 2 marked rectanlges

    #handle_event(KeyEvent(k=RIGHT_KEY))
    handle_event(KeyEvent(k=ENTER_KEY))     # end the croppingSession and save images to the out folder

    out_folder = "out//"
    out_files = list(os.listdir(out_folder))
    assert(len(out_files) == 2)             # there should now be 2 images in the out folder

    file_name_1 = out_folder+out_files[0]
    out_image1 = cv2.imread(file_name_1)
    h1, w1 = out_image1.shape[:2]
    assert(h1 == 390 and w1 == 390)         # check that the output images has the correct size

    file_name_2 = out_folder + out_files[1]
    out_image2 = cv2.imread(file_name_2)
    h2, w2 = out_image2.shape[:2]
    assert(h2 == 500*2 and w2 == 500*2)     # check that the output images has the correct size


