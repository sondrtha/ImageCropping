**This package is used to crop the images in a folder that is specified by the user.**

<br/>


![Example image of how it looks when the package is used](ReadmeImage/cropProgramExampleImage.png)  
_Example image of how it looks when the package is used. 
The user marks the region of the image that they want to be cropped (the blue region in the image)_   

<br/>
<br/>


[![see illustration video of using the ImageCropping code](https://www.youtube.com/watch?v=FH3f7tnlgq4&ab_channel=zohaBeenCoding/0.jpg)](https://www.youtube.com/watch?v=FH3f7tnlgq4&ab_channel=zohaBeenCoding)
_Illustration video for using the code: (you might want to set youtube speed to 0.5 or use keys to move forward and backward in the video)_

<br/>

### Information about the code:  
The cropped images will be generated after you are done selecting areas to crop
* to mark the region of a image you want to crop: 
	* click with the left mouse button on a corner of the rectangular region you want to crop. 
	* Then drag the mouse to the opposite side of the region to crop and release the mouse button.
	* If desired, change the region selected for the image by repeating the above steps.
* use right key to go to the next image 
* use left key to go back to the previous image 
* press r to rotate the image 90 degrees 
* press enter to generate the cropped images 
	* the images will now appear in a new folder named **out** 
	* the images will be of type bmp
	* the "cropping session" will now end 


#### requirements
This subsection is almost useless so feel free to skip it.....
The project includes a file called some_requirements.txt that contains some (maybe all?) the necessary
python packages to run the code for this project. However the packages named in some_requirements.txt 
are a subset of the packages shown when running pip freeze from a virtualenvironment I have
on WSL (Windows subsystem for Linux), which passes all tests that did not require windows. 
You might prefer to use some other versions of the packages though. 

### running automated tests
This project uses the win32api- so, it will only run on windows "out of the box". However only small
changes are needed for it to run on Linux as well. Use the following commands for testing: 

pip install .\
cd tests\
pytest testUtils.py\
pytest testImageFunctions.py\
pytest testCroppingSession.py