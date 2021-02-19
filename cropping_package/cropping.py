from cropping_package.CroppingImplementation.croppingSession import CroppingSession


def create_cropped_images(input_folder_path):
    """
    This is the only function intended to be used by the user of this package

    input_folder_path is the path to the input folder where the images to be cropped are located.
    The resulting cropped images will be put within this Project's folder named out.
    The resulting images will be of type bmp

    How to use the program:
    Click with the left mouse button on a corner position of the area you want to crop in the image,
    and while holding down the left button move the mouse to the opposite corner of the image so the desired area is cropped,
    and let go of the left mouse button. Now the desired area to be cropped should be marked in a blue-ish color.
    If you are unhappy with the crop area selection for the currently displayed image, repeat the process for that image.
    Press the right arrow to go to the next image in the list of images
    Press the left arrow to go back to the previous image
    When you have marked all the images you want to crop, press enter and
    then the cropped images will be generated and saved to the output-location given by out//
    """

    cropping_session = CroppingSession(input_folder_path)
    cropping_session.loop()
