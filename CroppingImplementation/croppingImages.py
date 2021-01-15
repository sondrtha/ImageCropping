import cv2      # opencv
import os
import math
from CroppingImplementation import utils    # used to get screen resolution (assumes user is on windows pc)
from CroppingImplementation import image


class UserImage():
    """
    Objects of this class contains both a version of the image provided by the user in its original size
    and also a scaled down version used to display each image so the entire image fits inside the screen.
    """

    #screen_resolution = (1920, 1080)                   # use this if you are not on windows
    screen_resolution = utils.get_screen_resolution()   # use windows api to find screen resolution

    def __init__(self, original_image):
        self.original_image = original_image
        self.scale = self.calculate_scaling(original_image)
        self.scaled_image = image.get_shrunken_image(original_image, self.scale)

    def get_scaled_image(self):
        return self.scaled_image

    @staticmethod
    def calculate_scaling(img):
        #calculate a scale so that the image fits within the screen
        screen_resolution_width, screen_resolution_height = UserImage.screen_resolution
        h, w = img.shape[:2]
        temp1 = math.ceil(h / screen_resolution_height)
        temp2 = math.ceil(w / screen_resolution_width)
        scale = max(temp1, temp2)
        return scale

    def rotate_image(self):
        #rotate the originally sized image, then recalculate the scaling and rescale the shrunken image
        self.original_image = image.rotate90(self.original_image)
        self.scale = self.calculate_scaling(self.original_image)
        self.scaled_image = image.get_shrunken_image(self.original_image, self.scale)


class CropUserImages():
    def __init__(self, input_folder_path):
        self.input_folder_path = input_folder_path
        self.images_to_be_cropped = self.create_list_of_user_images()    # list of objects of type userImage, see userImage class
        self.mouse_pos = None               # current position (x,y) of mouse, used when marking area to crop
        self.marked_pos = None              # the first of the two positions to be marked
        self.marked_position_pair = None    # consists of two corner positions that are used to make the crop.
                                            # (the positions are given for the scaled version of the image)

        self.current_image_index = 0        # indicates index of the image the user is currently looking at
        self.marked_rectangles_dict = {}    # a dictionary with the image-index as key and a corresponding marked rectangle as value

        self.resulting_crop_images = []     # the resulting cropped images (in bmp format) created by cropping each of the original images


    def create_list_of_user_images(self):
        folder_path = self.input_folder_path
        userImagesToBeCropped = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            img = cv2.imread(file_path)

            #if opencv can't open the image file (or other type of file), the file will be ignored
            if(img is None):
                continue

            userImage = UserImage(img)
            userImagesToBeCropped.append(userImage)
        return userImagesToBeCropped

    def rescale_current_image(self):
        self.images_to_be_cropped[self.current_image_index].rotate_image()

    def has_marked_a_rectangle(self):
        return (not self.marked_position_pair is None)

    def get_rectangle(self, marked_position_pair):
        p1, p2 = marked_position_pair
        rectangle = image.get_rectangle(p1, p2)
        return rectangle

    def mouse_event_handling(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.marked_pos = (x,y)
            self.marked_position_pair = None

        if event == cv2.EVENT_LBUTTONUP:
            self.marked_position_pair = (self.marked_pos, (x,y))
            self.marked_pos = None

        if event == cv2.EVENT_MOUSEMOVE:
            self.mouse_pos = (x,y)


    def draw_marked_rect(self, img, rectangle):
        min_x, min_y, width, height = rectangle
        image.draw_marked_rectangle(img, min_x, min_y, min_x + width, min_y + height)


    def draw_image(self):
        image_index = self.current_image_index
        userImage = self.images_to_be_cropped[image_index]
        img = image.copy_img(userImage.get_scaled_image())

        #draw crop-rectangle on the image
        if(self.has_marked_a_rectangle()):
            rectangle = self.get_rectangle(self.marked_position_pair)
            self.draw_marked_rect(img, rectangle)
        elif(not self.marked_pos is None):
            pos1 = self.marked_pos
            pos2 = self.mouse_pos
            rectangle = image.get_rectangle(pos1, pos2)
            self.draw_marked_rect(img, rectangle)
        return img


    def get_marked_position_pair_for_image(self, image_index):
        if(image_index in self.marked_rectangles_dict):
            crop_rect = self.marked_rectangles_dict[image_index]
            marked_position_pair = image.get_corner_points_from_rectangle(crop_rect)
            return marked_position_pair


    def save_crop_image_state(self):
        #This function is called in order to save crop-information about the current image before moving to another image
        if (self.has_marked_a_rectangle()):
            marked_rectangle = self.get_rectangle(self.marked_position_pair)
            self.marked_rectangles_dict[self.current_image_index] = marked_rectangle
        self.marked_position_pair = None
        self.marked_pos = None

    def right_arrow(self):
        if(self.current_image_index < len(self.images_to_be_cropped)-1):
            self.save_crop_image_state()
            self.current_image_index += 1
            self.marked_position_pair = self.get_marked_position_pair_for_image(self.current_image_index)

    def left_arrow(self):
        if (self.current_image_index > 0):
            self.save_crop_image_state()
            self.current_image_index -= 1
            self.marked_position_pair = self.get_marked_position_pair_for_image(self.current_image_index)

    def create_cropped_images_list(self):
        cropped_image_list = []
        for image_index in self.marked_rectangles_dict:
            crop_rect = self.marked_rectangles_dict[image_index]
            p1, p2 = image.get_corner_points_from_rectangle(crop_rect)

            scale = self.images_to_be_cropped[image_index].scale

            # coordinates within the shrunken image that is displayed
            x1,y1 = p1
            x2,y2 = p2

            # coordinates within the origianlly sized image
            X1, Y1 = x1 * scale, y1 * scale
            X2, Y2 = x2 * scale, y2 * scale


            # Ignore cases with very small crop region.
            # They typically appear when the user left clicks (and does not drag the mouse) and don't intend to create a region for cropping.
            if(image.get_distance(p1, p2) < 5):
                continue

            original_image = self.images_to_be_cropped[image_index].original_image
            cropped_image = original_image[Y1:Y2, X1:X2]
            cropped_image_list.append(cropped_image)
        self.resulting_crop_images = cropped_image_list


    def save_resulting_cropped_images(self):
        #save images to out folder
        outpath = "out"
        if(not os.path.exists(outpath)):
            os.mkdir(outpath)
        for index, cropped_img in enumerate(self.resulting_crop_images):
            file_path = outpath + "//" + "img"+str(index)+".bmp"
            cv2.imwrite(file_path, cropped_img)

    def create_and_save_cropped_images(self):
        self.create_cropped_images_list()
        self.save_resulting_cropped_images()



    def loop(self):
        cv2.namedWindow("Frame")
        cv2.setMouseCallback("Frame", self.mouse_event_handling)

        while (True):
            img = self.draw_image()
            cv2.imshow("Frame", img)
            k = cv2.waitKeyEx(5)

            if k == 27:         #ESC -key
                # press the Esc-key to stop the program.
                # the cropping information about the images will be lost
                break

            if k == 2555904:    #RIGHT - key
                #press the right arrow to go to the next image on the list
                self.right_arrow()

            if k == 2424832:    #left - key
                # go to the previous image on the list
                self.left_arrow()

            if k == 13 :        #Enter - key
                # press enter to create and save the cropped images and then the program will exit
                self.create_and_save_cropped_images()


            if k == ord('r'):   #press r to rotate the image
                self.rescale_current_image()
