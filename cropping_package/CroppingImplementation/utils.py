from win32api import GetSystemMetrics       # is used to get your screen resolution

def get_screen_resolution():
    screen_resolution_width = GetSystemMetrics(0)
    screen_resolution_height = GetSystemMetrics(1)
    return (screen_resolution_width, screen_resolution_height)
