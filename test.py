import arcade
import settings

key_translator = {
    48: '0',
    49: '1',
    50: '2',
    51: '3',
    52: '4',
    53: '5',
    54: '6',
    55: '7',
    56: '8',
    57: '9',
    95: '_',
    97: 'A',
    98: 'B',
    99: 'C',
    100: 'D',
    101: 'E',
    102: 'F',
    103: 'G',
    104: 'H',
    105: 'I',
    106: 'J',
    107: 'K',
    108: 'L',
    109: 'M',
    110: 'N',
    111: 'O',
    112: 'P',
    113: 'Q',
    114: 'R',
    115: 'S',
    116: 'T',
    117: 'U',
    118: 'V',
    119: 'W',
    120: 'X',
    121: 'Y',
    122: 'Z'
}

text = ' '
class SriGameView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(text, settings.WIDTH / 2, settings.HEIGHT / 2, arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        global text
        try:
            for num_key, value in key_translator.items():
                if key == 65288 and len(text) > 1:
                    text = text[:10]
                elif num_key == key:
                    if len(text) > 18:
                        break
                    else:
                        letter = value
                        text += letter
                else:
                    continue
        except:
            pass



if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector
    typing = False
    text = 'Username: '
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = SriGameView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
