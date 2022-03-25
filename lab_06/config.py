MAIN_COLOUR = "#d7d7d7"
ADD_COLOUR = "#FDECE4"
CANVAS_COLOUR = "#FFFFFF"
DEFAULT_COLOUR = "#000000" 

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 780
FIELD_WIDTH = FIELD_HEIGHT = 740
center = 370

class Point:
    def __init__(self, x=0, y=0, colour="#FFFFFF"):
        self.x = x
        self.y = y
        self.colour = colour

MODES = ["Без задержки", "С задержкой"]