from cropping_package.CroppingImplementation.utils import *

def test_get_screen_resolution():
    screen_width, screen_height = get_screen_resolution()
    assert(screen_width > 100)      #basically check that the screen resolution is a number