from cropping_package.CroppingImplementation import utils, image

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
        self.scaled_image = image.get_shrunken_image(original_image, self.scale)  #version of the image scaled to fit inside the screen

    def get_scaled_image(self):
        return self.scaled_image

    @staticmethod
    def calculate_scaling(img):
        #calculate a scale so that the image fits within the screen
        scale = image.calculate_scaling(img, UserImage.screen_resolution)
        return scale

    def rotate_image(self):
        #rotate the originally sized image, then recalculate the scaling and rescale the shrunken image
        self.original_image = image.rotate90(self.original_image)
        self.scale = self.calculate_scaling(self.original_image)
        self.scaled_image = image.get_shrunken_image(self.original_image, self.scale)
