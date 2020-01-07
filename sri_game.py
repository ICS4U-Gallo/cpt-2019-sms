import arcade
import settings


TITLE = "Some disasterous Game"
TEXT_COLOR = arcade.color.ARSENIC
SCREEN_COLOR = arcade.color.BONE

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT

global mode
mode = "menu"


class SriMenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)
    
    def on_draw(self):
        arcade.start_render()

        # Title
        arcade.draw_text(TITLE, WIDTH/2, 0.85 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 30), anchor_x="center", align="right")

        # Labels
        arcade.draw_text("PLAY (P)", WIDTH/2, 0.7 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
        arcade.draw_text("INSTRUCTIONS (I)", WIDTH/2, 0.5 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
        arcade.draw_text("SCOREBOARD (S)", WIDTH/2, 0.3 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
        
    

    def on_key_press(self, key, modifiers):
        global mode
        if key == 112: # P for Play
            mode = "play"
            self.window.show_view(SriGameView())
        elif key == 105: # I for Instructions
            mode = "instructions"
            self.window.show_view(SriInstructionsView(self))
        elif key == 115: # S for Scoreboard
            mode = "scoreboard"
            self.window.show_view(SriScoreBoardView(self))


class SriGameView(arcade.View):  

    def on_show(self):
        if mode == "menu":
            self.window.show_view(SriMenuView(self))
        arcade.set_background_color(SCREEN_COLOR)
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("game ma doode", WIDTH/2, HEIGHT/2,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
    
    def update(self, delta_time: float):
        pass

    def on_key_press(self, key, modifiers):
        self.window.show_view(SriMenuView(self))
        # self.director.next_view()
        # pass


class SriInstructionsView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("instructttiions\nhow do you do fellow kids", WIDTH/2, HEIGHT/2,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
    

    def on_key_press(self, key, modifiers):
        self.window.show_view(SriMenuView(self))


class SriScoreBoardView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Score Board", WIDTH/2, HEIGHT/2,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
    

    def on_key_press(self, key, modifiers):
        self.window.show_view(SriMenuView(self))


class Score:
    pass


class Article:
    pass


class SaveData:
    def __init__(self, game_mode: str, scores):
        self.game_mode = game_mode
        self.scores = scores
    

    def save_to(self, save_file: str):
        # save object to save file








if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = SriGameView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
