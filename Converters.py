#--- Returns a tuple containing the given coordinates originating from the centre, but converted to originate from the top left corner ---

import pygame

def CentreOrigin(image, screen_resolution = (1280,720), desired_coordinates = (0,0)):
    image_size = (image.get_width(),image.get_height())
    return ((((screen_resolution[0]/2)-(image_size[0]/2))+desired_coordinates[0]),(screen_resolution[1] - (((screen_resolution[1]/2)-(image_size[1]/2))+desired_coordinates[1])))