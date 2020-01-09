import arcade
import settings

from time import time
import random
from typing import List

TITLE = "Some disasterous Game"
TEXT_COLOR = arcade.color.ARSENIC
SCREEN_COLOR = arcade.color.BONE

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT
PRESS_ANY_KEY_TEXT = "Press any key to return to the Menu"

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
        
        sri = Score(15, "Sridhar", 1231231.33, "adf")
        Score(20, "haha", 1.1, "adf")
    
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
        instruction_text = """

        CONTROLS:

        Move the mouse and
        click on the
        words and buttons

        """
        arcade.draw_text(instruction_text, 0.6 * WIDTH,  0 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")
    
        arcade.draw_text(PRESS_ANY_KEY_TEXT, 0.175 * WIDTH, 0.003 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")
        



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
        arcade.draw_text("Score Board", WIDTH/2, 0.9 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50), anchor_x="center", align="right")

        arcade.draw_text(PRESS_ANY_KEY_TEXT, 0.175 * WIDTH, 0.003 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")

        top_5_names = []
        top_5_scores = []

        top_scores = Score.get_top_5_scores()

        for score in top_scores:
            top_5_names.append(score.get_player())
            top_5_scores.append(score.get_points())
        
        print(top_scores)
        print(top_5_names)
        print(top_5_scores)


        for i in range(len(top_scores)):
            arcade.draw_text(f"{i + 1}. {top_5_names[i]} ---- {top_5_scores[i]}",
                             WIDTH * 0.3, 0.8 * HEIGHT - HEIGHT * 0.07 * i * 2, arcade.color.BLUE, 18, align="left")
    

    def on_key_press(self, key, modifiers):
        self.window.show_view(SriMenuView(self))


class Score:
    all_scores = []
    
    def __init__(self, points: int, player: int, time: float, article: "Article"):
        self._points = points
        self._player = player
        self._time = time
        self.article = article

        Score.all_scores.append(self)
    
    def change_points(self, points: int):
        if points is int:
            self._points = points
        else:
            raise Exception("Points should be an integer")

    def get_points(self):
        return self._points

    def set_player(self, player: str):
        if player is str:
            self._player = player
        else:
            self._player = str(player)

    def get_player(self):
        return self._player

    def set_time(self, time: float):
        if time is float and time > 0:
            self._time = time
        else:
            raise Exception("Time should be a positive float")

    def get_time(self):
        return time

    @classmethod
    def get_top_5_scores(cls):
        return cls.all_scores

        mabye just a regular merge sort sending only the player names and scores.

        """ FIX THE SORTING AND DISPLAYING OF SCORES!!! """

        return sort_scores(cls.all_scores)[0:5]

        


class Article:
    def __init__(self):
        used_words = []
        unused_words = get_words()
        random.shuffle(unused_words)
        unused_words = unused_words[0:100]
        all_words = unused_words

        author = Article.make_name("Berock") + Article.make_name("Obamer")
        date = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1600, 2300)}"

    
    @staticmethod
    def make_name(backup: str):
        words = get_words()

        random.shuffle(words)
        for word in words:
            if word[0].isupper() and len(word) > 3:
                    name = word
                    break
            else:
                name = backup
    
        return name
        



    


class SaveData:
    def __init__(self, game_mode: str, scores):
        self.game_mode = game_mode
        self.scores = scores
    

    def save_to(self, save_file: str):
        # save object to save file
        pass



def get_words():
    lines = []
    with open("Sri_Words.txt", "r") as f:
        for line in f:
            lines.append(line.strip())
    
    return lines


def sort_scores(scores: List["Score"]):
    # Merge Sort
    # Greatest to least

    if len(scores) == 1 or len(scores) == 0:
        return scores

    midpoint = len(scores) // 2
    
    left_side = sort_scores(scores[:midpoint])
    right_side = sort_scores(scores[midpoint:])

    sorted_list = []

    left_marker = 0
    right_marker = 0

    while left_marker < len(left_side) and right_marker < len(right_side):
        if left_side[left_marker].get_points() < right_side[right_marker].get_points():
            sorted_list.append(right_side[right_marker])
            right_marker += 1
        else:
            sorted_list.append(left_side[left_marker])
            left_marker += 1

    
    while right_marker < len(right_side):
        sorted_list.append(right_side[right_marker])
        right_marker += 1
    
    while left_marker < len(left_side):
        sorted_list.append(left_side[left_marker])
        left_marker += 1
    
    return sorted_list





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
