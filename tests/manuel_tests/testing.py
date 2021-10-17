from cropping_package import cropping


def test_create_cropped_images():
    input_folder_path = "..//MyImageFolder//"  # set to your desired input folder path here
                                           # In this example the example-images in the folder MyImageFolder is used
    cropping.create_cropped_images(input_folder_path)


test_create_cropped_images()
