import arcade
import settings

from time import time
import random
from typing import List, Dict
import pickle
from datetime import date

TITLE = "Some disasterous Game"
TEXT_COLOR = arcade.color.ARSENIC
SCREEN_COLOR = arcade.color.BONE

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT
PRESS_ANY_KEY_TEXT = "Press any key to return to the Menu"

PICKLE_FILE = "sri_data.p"

LETTERS = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()

global mode, save_file, cur_game
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
        arcade.draw_text("Press (N) to go to the next game", 0.175 * WIDTH, 0.003 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")

    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        global mode
        if key == 112: # P for Play
            mode = "ask player name"
            self.window.show_view(SriGameView())
        elif key == 105: # I for Instructions
            mode = "instructions"
            self.window.show_view(SriInstructionsView(self))
        elif key == 115: # S for Scoreboard
            mode = "scoreboard"
            self.window.show_view(SriScoreBoardView(self))
        elif key == 110: # N for Next Game
            self.window.next_view()


class SriAskPlayerNameView(arcade.View):
    name = ""

    def __init__(self):
        super().__init__()
        SriAskPlayerNameView.name = ""
    
    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)
    
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text("Please type your name | Your name must be 5 characters or shorter", 0.5 * WIDTH, HEIGHT - (0.03 * HEIGHT),
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")
        arcade.draw_text("Press (ENTER) when complete | Press (ESC) to go to the Menu", 0.5 * WIDTH, HEIGHT - (0.07 * HEIGHT),
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")

        arcade.draw_text(f'Name: "{SriAskPlayerNameView.name}"', 0.5 * WIDTH, 0.5 * HEIGHT,
                         TEXT_COLOR, font_size=(0.02 * (HEIGHT + WIDTH)), anchor_x="center", align="center")
    
    def update(self, delta_time: float):
        pass

    def on_key_press(self, key, modifiers):
        global mode
        if key == 65307: # ESCAPE
            mode = "menu"
            self.window.show_view(SriMenuView(self))
        elif key == 65288: # BACKSPACE
            SriAskPlayerNameView.name = SriAskPlayerNameView.name[:-1]
        elif key == 65293: # ENTER
            mode = "play"
            self.window.show_view(SriGameView())
        elif len(SriAskPlayerNameView.name) >= 5:
            pass
        elif key in range(97, 122 + 1):
            SriAskPlayerNameView.name += key_code_to_letter(key)


class SriGameView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        global mode
        global cur_game

        if mode == "menu":
            self.window.show_view(SriMenuView(self))
        elif mode == "instructions":
            self.window.show_view(SriInstructionsView(self))
        elif mode == "scoreboard":
            self.window.show_view(SriScoreBoardView(self))
        elif mode == "play":
            cur_player = SriAskPlayerNameView.name
            cur_game = Game(
                Score(0, cur_player),
                Article()
                )
        elif mode == "ask player name":
            self.window.show_view(SriAskPlayerNameView())
    

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(SCREEN_COLOR)

        global cur_game

        cur_game.update_points()

        # Titles and Related
        arcade.draw_text("Press (ESC) to go to the Menu | Use the mouse to click on the words", 0.5 * WIDTH, 0.97 *  HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="right")        

        disp_clock = cur_game.game_display_time(1)
        cur_points = cur_game.game_score.get_points()

        disp_date = convert_date_to_words(cur_game.article.date)

        arcade.draw_text(f"Actions Performed: {cur_game.actions_performed} | Points: {cur_points} | Time: {disp_clock}s / {cur_game.max_time}s", 0.5 * WIDTH, 0.035 * HEIGHT,
                         TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)), anchor_x="center", align="center")
        
        arcade.draw_text(f"{cur_game.article.title}    By: {cur_game.article.author}", 0.5 * WIDTH, 0.9 * HEIGHT,
                         TEXT_COLOR, font_size=(0.016 * (HEIGHT + WIDTH)), anchor_x="center", align="center", bold=True, italic=True)
        arcade.draw_text(f"Date: {disp_date}", 0.5 * WIDTH, 0.85 * HEIGHT,
                         TEXT_COLOR, font_size=(0.012 * (HEIGHT + WIDTH)), anchor_x="center", align="center", bold=True, italic=True)


        # IM CHANGING THE WAY THE GAME WORDS!!!

        # 10 words, labelled 0 - 9
        # computer plays the game (finds a path of words that work)
        # shuffles the words and displays them 0 - 9
        # each word = 10 points
        # more points based on the time left

        arcade.draw_text(f"Current Word: {cur_game.article.used_words[-1]}", 0.5 * WIDTH, 0.095 * HEIGHT,
                         TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)), anchor_x="center", align="center")

        for i, word in enumerate(cur_game.article.all_words[:5]):
            if word in cur_game.article.used_words:
                continue
            arcade.draw_text(f"{i}. {word}", 0.1 * WIDTH, 0.7 * HEIGHT - (i * 0.1 * HEIGHT),
                             TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)), anchor_x="left", align="left")

        for i, word in enumerate(cur_game.article.all_words[5:]):
            if word in cur_game.article.used_words:
                continue
            arcade.draw_text(f"{i + 5}. {word}", 0.5 * WIDTH, 0.7 * HEIGHT - (i * 0.1 * HEIGHT),
                             TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)), anchor_x="left", align="left")



        # End Game

        end_game_condition_1 = float(disp_clock[:-1]) >= cur_game.max_time
        end_game_condition_2 = len(cur_game.article.used_words) == len(cur_game.article.all_words)

        if end_game_condition_1 or end_game_condition_2:
            global mode
            mode = "endgame"

            # Clearing the board bonus
            if end_game_condition_2:
                cur_game.game_score.add_points(100)

            self.window.show_view(SriEndGameView())

            # Time Bonus Multiplier
            time_multiplier = cur_game.max_time - float(disp_clock[:-1])
            if time_multiplier > 1:
                cur_game.game_score.add_points(
                    int(cur_game.game_score.get_points() * time_multiplier)
                )

    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        if key == 65307: # ESCAPE for menu
            global mode
            mode = "menu"
            self.window.show_view(SriMenuView(self))
        
        number = key_code_to_number(key)
        if number in range(0, 9 + 1):
            cur_game.actions_performed += 1
            if (cur_game.article.used_words[-1])[-1].upper() == (cur_game.article.all_words[number])[0].upper():
                temp = cur_game.article.all_words[number]
                cur_game.article.used_words.append(temp)
                cur_game.game_score.add_1_words_joined()
        
        if key == 117: # U for undo
            cur_game.actions_performed += 1
            cur_game.article.used_words.pop(-1)


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
        
    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        global mode
        mode = "menu"
        self.window.show_view(SriMenuView(self))


class SriScoreBoardView(arcade.View):
    nuke_counter = 0

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

        top_scores = Score.get_top_scores()

        num_scores_to_show = len(top_scores)

        if num_scores_to_show > 5:
            num_scores_to_show = 5

        for i in range(num_scores_to_show):
            top_5_scores.append(top_scores[i].get_points())
            top_5_names.append(top_scores[i].get_player())

        # show the number of words joined
        # 22d
        # make this more neat (no top5names junk)

        for i in range(num_scores_to_show):
            arcade.draw_text(f"{i + 1}. '{top_5_names[i]}' ---- {top_5_scores[i]} ---- {22}",
                             WIDTH * 0.3, 0.8 * HEIGHT - HEIGHT * 0.07 * i * 2, arcade.color.BLUE, 18, align="left")
    
    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        if key == 110: # N for nuke
            SriScoreBoardView.nuke_counter += 1
            if SriScoreBoardView.nuke_counter >= 10:
                global save_file
                SriScoreBoardView.nuke_counter = 0
                save_file.nuke()
                save_file.load_from_file()
        else:
            self.window.show_view(SriMenuView(self))
            global mode
            mode = "menu"


class SriEndGameView(arcade.View):
    def __init__(self):
        super().__init__()
    
    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)
    
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text("Press any key (other than the numbers) to return to the menu", 0.5 * WIDTH, HEIGHT - (0.03 * HEIGHT),
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)), anchor_x="center", align="center")
        
        global cur_game

        arcade.draw_text(f"Player: {cur_game.game_score.get_player()}\n\nWords Joined: {cur_game.game_score.get_words_joined()}\n\nPoints: {cur_game.game_score.get_points()}\n\nRank: {cur_game.game_score.find_rank()}", 0.5 * WIDTH, 0.2 * HEIGHT,
                         TEXT_COLOR, font_size=(0.03 * (HEIGHT + WIDTH)), anchor_x="center", align="center")
    
    def update(self, delta_time: float):
        pass

    def on_key_press(self, key, modifiers):
        if key_code_to_number(key) in range(0, 9 + 1):
            pass
        else:
            global mode
            mode = "menu"
            self.window.show_view(SriMenuView(self))


class Game:
    all_games = []

    def __init__(self, game_score: "Score", article: "Article"):
        self.game_score = game_score
        self.article = article
        self.start_time = time()
        self.max_time = 1
        self.actions_performed = 0
        Game.all_games.append(self)

    def game_display_time(self, decimal_places: int = 3) -> str:
        if decimal_places < 0:
            decimal_places = 0

        disp_clock = delta_time(self.start_time, time())

        disp_clock = round(disp_clock, decimal_places)
        
        return f"{disp_clock}"

    def calculate_points(self):
        base_score = 10 * self.game_score.get_words_joined()
        base_score -= self.actions_performed

        return base_score
    
    def update_points(self):
        self.game_score.change_points(self.calculate_points())



class Score:
    all_scores = []
    
    def __init__(self, points: int, player: int):
        self._points = points
        self._player = player
        self._time = float(time())
        self._words_joined = 0

        Score.all_scores.append(self)
    
    def change_points(self, points: int):
        if isinstance(points, int):
            self._points = points
        else:
            raise Exception("Points should be an integer")

    def add_points(self, points: int):
        if isinstance(points, int):
            self._points += points
        else:
            raise Exception("Points should be an integer")

    def get_points(self):
        return self._points

    def set_player(self, player: str):
        if isinstance(player, str):
            self._player = player
        else:
            self._player = str(player)

    def get_player(self):
        return self._player

    def set_time(self, time: float):
        if isinstance(time, float) and time > 0:
            self._time = time
        else:
            raise Exception("Time should be a positive float")

    def get_time(self):
        return time

    def get_words_joined(self):
        return self._words_joined
    
    def add_1_words_joined(self):
        self._words_joined += 1

    @classmethod
    def get_top_scores(cls): 
        return merge_sort_scores(cls.all_scores)
    
    def find_rank(self) -> int:
        scores = Score.get_top_scores()

        for i in range(len(scores)):
            if scores[i] == self:
                rank = i
                break

        return rank + 1


class Article:
    def __init__(self):
        self.title = Article.make_title(3)
        self.author = f'{Article.make_name("Berock")} {Article.make_name("Obamer")}'
        self.date = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1600, 2300)}"

        self.all_words = self.make_game_words()
        self.starting_word = self.all_words[0]
        self.all_words = self.all_words[1:]
        self.used_words = [self.starting_word]
        random.shuffle(self.all_words)

    def make_game_words(self) -> List[str]:
        all_words = get_words_by_letter()
        starting_letter = random_letter()
        starting_word = random_word_from_list(all_words[starting_letter][:])
        final_words = [starting_word]

        for i in range(10):
            letter = final_words[i][-1].upper()
            word = random_word_from_list(((all_words[letter])[:]))
            final_words.append(word)
        
        return final_words


    @staticmethod
    def make_title(num_words: int) -> str:
        words = get_words()
        random.shuffle(words)
        
        title = ""

        for i in range(3):
            rand_word = random.choice(words)
            rand_word = rand_word[0].upper() + rand_word[1:].lower()
            title += (rand_word + " ")
        
        return title[:-1]

    @staticmethod
    def make_name(backup: str) -> str:
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
    def __init__(self):
        global mode
        self.game_mode = "menu"
        self.scores = Score.all_scores

    def load_from_file(self, save_file: str = PICKLE_FILE):
        try:
            save_files = pickle.load(open(save_file, "rb"))
        except EOFError:
            self.game_mode = "menu"

        try:
            self.game_mode = save_files["game_mode"]
            self.scores = save_files["scores"]
        except KeyError:
            self.game_mode = "menu"
            self.scores = []
        except UnboundLocalError:
            self.game_mode = "menu"
            self.scores = []

        global mode
        Score.all_scores = self.scores
        mode = self.game_mode

    def save(self, save_file: str = PICKLE_FILE):
        self.scores = Score.all_scores

        save_files = {
            "game_mode": self.game_mode,
            "scores": self.scores
        }

        pickle.dump(save_files, open(save_file, "wb"))
    
    def nuke(self, save_file: str = PICKLE_FILE):
        pickle.dump({}, open(save_file, "wb"))


global save_file
save_file = SaveData()
save_file.load_from_file()


def random_word_from_list(words: List[str]) -> str:
    random.shuffle(words)
    return words[0]


def random_letter() -> str:
    rand_letter = random.randint(0, 25)
    rand_letter = LETTERS[rand_letter]
    return rand_letter


def get_words() -> List[str]:
    lines = []
    with open("Sri_Words.txt", "r") as f:
        for line in f:
            lines.append(line.strip())
    
    return lines


def merge_sort_scores(nums: List["Score"]) -> List["Score"]:
    
    if len(nums) <= 1:
        return nums
    
    midpoint = len(nums) // 2

    left_side = merge_sort_scores(nums[:midpoint])
    right_side = merge_sort_scores(nums[midpoint:])

    sorted_list = []

    left_marker = 0
    right_marker = 0

    while left_marker < len(left_side) and right_marker < len(right_side):
        
        if left_side[left_marker].get_points() > right_side[right_marker].get_points():
            sorted_list.append(left_side[left_marker])
            left_marker += 1
        else:
            sorted_list.append(right_side[right_marker])
            right_marker += 1
        
    
    while left_marker < len(left_side):
        sorted_list.append(left_side[left_marker])
        left_marker += 1
    
    while right_marker < len(right_side):
        sorted_list.append(right_side[right_marker])
        right_marker += 1
    
    return sorted_list


def key_code_to_letter(key_code: int) -> str:
    letters = LETTERS

    # A -> 97
    # Z -> 122

    key_code -= 97

    return letters[key_code]


def key_code_to_number(key_code: int) -> int:
    # Keypad numbers
    # 0 -> 65456
    # 9 -> 65465
    
    if key_code in range(65456, 65465 + 1):
        return key_code - 65456
    
    # Keyboard numbers
    # 0 -> 48
    # 9 -> 57

    elif key_code in range(48, 57 + 1):
        return key_code - 48
    else:
        return -1


def delta_time(time_1: float, time_2: float) -> float:
    return time_2 - time_1


def convert_date_to_words(slash_date: str) -> str:
    slash_date = slash_date.split("/")

    for i in range(len(slash_date)):
        slash_date[i] = int(slash_date[i])

    words = date(day=slash_date[0],
                 month=slash_date[1],
                 year=slash_date[2]).strftime('%A %d %B %Y')

    return words


def get_words_by_letter() -> Dict:
    all_words = get_words()

    letters = LETTERS
    by_letter = {"ETC": []}
    for letter in letters:
        by_letter[letter] = []
    
    for word in all_words:
        first_letter = word[0].upper()
        try:
            by_letter[first_letter].append(word)
        except KeyError:
            by_letter["ETC"].append(word)

    return by_letter


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
