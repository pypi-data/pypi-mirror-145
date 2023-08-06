import numpy as np
from js import document
import colorsys
import math

class Canvas:
    def __init__(self, width, height):
        self.canvas = document.getElementById('canvas')
        self.context = self.canvas.getContext("2d")
        self.canvas.style.width = str(width) + "px";
        self.canvas.style.height = str(height) + "px";
        self.context.clearRect(0, 0, width, height);

    def draw_circle(self, radius, center_x, center_y, color):
        self.context.beginPath()
        # context.strokeStyle = color
        self.context.fillStyle=color
        self.context.arc(center_x, center_y, radius, 0, 2 * math.pi)
        self.context.fill()

def create_canvas(width, height):
    return Canvas(width, height)

def random_color():
    """
    Generates a random color in HSV space, then
    translates it into RGB space. Feel free to edit
    """
    h = np.random.uniform(200,300) / 360
    s = np.random.uniform(0.5, 0.9) 
    v = np.random.uniform(.7, .9) 
    (r,g,b) = colorsys.hsv_to_rgb(h, s, v)
    return f'rgb({r*256},{g*256},{b*256})'