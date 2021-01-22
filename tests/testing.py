from cropping_package import cropping


def testCreateCroppedImages():
    input_folder_path = "MyImageFolder//"  # set to your desired input folder path here
                                           # In this example the example-images in the folder MyImageFolder is used
    cropping.createCroppedImages(input_folder_path)

testCreateCroppedImages()