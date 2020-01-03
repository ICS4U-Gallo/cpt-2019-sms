import arcade

class Button:
    def __init__(self, x, y, radius, texture, color, transparency):
        self.button = arcade.Sprite(center_x=x, center_y=y)
        self.button.texture = texture
    