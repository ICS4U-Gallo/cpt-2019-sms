import arcade
import settings

from time import time
import random
from typing import List, Dict
import pickle
from datetime import date

TITLE = "Word Linker"
TEXT_COLOR = arcade.color.ARSENIC
SCREEN_COLOR = arcade.color.BONE

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT

PRESS_ANY_KEY_TEXT = "Press any key to return to the Menu"

PICKLE_FILE = "sri_data.p"
WORD_FILE = "Sri_Words.txt"

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
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 30),
                         anchor_x="center", align="center")

        # Labels
        arcade.draw_text("PLAY (P)", WIDTH/2, 0.7 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50),
                         anchor_x="center", align="right")
        arcade.draw_text("INSTRUCTIONS (I)", WIDTH/2, 0.5 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50),
                         anchor_x="center", align="right")
        arcade.draw_text("SCOREBOARD (S)", WIDTH/2, 0.3 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50),
                         anchor_x="center", align="right")

        arcade.draw_text("Press (N) to go to the next game",
                         0.01 * WIDTH, 0.003 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)),
                         anchor_x="left", align="left")

        arcade.draw_text("Created by Sridhar Sairam - Jan 2020",
                         0.99 * WIDTH, 0.003 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)),
                         anchor_x="right", align="left")

    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        global mode
        if key == 112:  # P for Play
            mode = "ask player name"
            self.window.show_view(SriGameView())
        elif key == 105:  # I for Instructions
            mode = "instructions"
            self.window.show_view(SriInstructionsView(self))
        elif key == 115:  # S for Scoreboard
            mode = "scoreboard"
            self.window.show_view(SriScoreBoardView(self))
        elif key == 110:  # N for Next Game
            self.window.next_view()


class SriAskPlayerNameView(arcade.View):
    name = ""
    name_specification_text = ("Please type your name | Your name must be 5 characters or shorter, using only letters")
    button_text = "Press (ENTER) when complete | Press (ESC) to go to the Menu"

    def __init__(self):
        super().__init__()
        SriAskPlayerNameView.name = ""

    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)

    def on_draw(self):
        arcade.start_render()

        # Labels
        arcade.draw_text(SriAskPlayerNameView.name_specification_text,
                         0.5 * WIDTH, HEIGHT - (0.03 * HEIGHT),
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)),
                         anchor_x="center", align="right")
        arcade.draw_text(SriAskPlayerNameView.button_text,
                         0.5 * WIDTH, HEIGHT - (0.07 * HEIGHT),
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)),
                         anchor_x="center", align="right")

        # Name
        arcade.draw_text(f'Name: "{SriAskPlayerNameView.name}"',
                         0.5 * WIDTH, 0.5 * HEIGHT,
                         TEXT_COLOR, font_size=(0.02 * (HEIGHT + WIDTH)),
                         anchor_x="center", align="center")

    def update(self, delta_time: float):
        pass

    def on_key_press(self, key, modifiers):
        global mode
        if key == 65307:  # ESCAPE
            mode = "menu"
            self.window.show_view(SriMenuView(self))
        elif key == 65288:  # BACKSPACE
            SriAskPlayerNameView.name = SriAskPlayerNameView.name[:-1]
        elif key == 65293:  # ENTER
            mode = "play"
            self.window.show_view(SriGameView())
        elif len(SriAskPlayerNameView.name) >= 5:
            # Limiting name to a maximum of 5 characters
            pass
        elif key in range(97, 122 + 1):
            SriAskPlayerNameView.name += key_code_to_letter(key)


class SriGameView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        global mode
        global cur_game

        # In essence, this is a redirecting site.

        # This is because many times, the game view is SriGameView
        # but it needs to be something else.
        if mode == "menu":
            self.window.show_view(SriMenuView(self))
        elif mode == "instructions":
            self.window.show_view(SriInstructionsView(self))
        elif mode == "scoreboard":
            self.window.show_view(SriScoreBoardView(self))
        elif mode == "play":
            cur_player = SriAskPlayerNameView.name
            cur_game = Game(cur_player)
        elif mode == "ask player name":
            self.window.show_view(SriAskPlayerNameView())

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(SCREEN_COLOR)

        global cur_game
        cur_game.update_points()

        # Titles and Related
        arcade.draw_text("Press (ESC) to go to the Menu | Use the number keys and (U) to play",
                         0.5 * WIDTH, 0.97 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)),
                         anchor_x="center", align="right")

        disp_clock = cur_game.game_display_time(1)
        cur_points = cur_game.game_score.get_points()

        disp_date = convert_date_to_words(cur_game.article.date)

        arcade.draw_text(f"Actions Performed: {cur_game.actions_performed} | Words Linked: {cur_game.game_score.get_words_linked()} | Points: {cur_points} | Time: {disp_clock}s / {cur_game.max_time}s",
                         0.5 * WIDTH, 0.035 * HEIGHT,
                         TEXT_COLOR, font_size=(0.012 * (HEIGHT + WIDTH)),
                         anchor_x="center", align="center")

        arcade.draw_text(f"{cur_game.article.title}    By: {cur_game.article.author}",
                         0.5 * WIDTH, 0.9 * HEIGHT,
                         TEXT_COLOR, font_size=(0.016 * (HEIGHT + WIDTH)),
                         anchor_x="center", align="center",
                         bold=True, italic=True)
        arcade.draw_text(f"Date: {disp_date}", 0.5 * WIDTH, 0.85 * HEIGHT,
                         TEXT_COLOR, font_size=(0.012 * (HEIGHT + WIDTH)),
                         anchor_x="center", align="center",
                         bold=True, italic=True)

        arcade.draw_text(f"Current Word: {cur_game.article.used_words[-1]}",
                         0.5 * WIDTH, 0.095 * HEIGHT,
                         TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)),
                         anchor_x="center", align="center")

        # Words to choose from
        for i, word in enumerate(cur_game.article.all_words[:5]):
            if word in cur_game.article.used_words:
                continue
            arcade.draw_text(f"{i}. {word}",
                             0.1 * WIDTH, 0.7 * HEIGHT - (i * 0.1 * HEIGHT),
                             TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)),
                             anchor_x="left", align="left")

        for i, word in enumerate(cur_game.article.all_words[5:]):
            if word in cur_game.article.used_words:
                continue
            arcade.draw_text(f"{i + 5}. {word}",
                             0.5 * WIDTH, 0.7 * HEIGHT - (i * 0.1 * HEIGHT),
                             TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)),
                             anchor_x="left", align="left")

        # End Game
        end_game_condition_1 = float(disp_clock[:-1]) >= cur_game.max_time
        end_game_condition_2 = (len(cur_game.article.used_words) ==
                                (len(cur_game.article.all_words) + 1))
        # + 1 as starting_word is not included in all_words

        if end_game_condition_1 or end_game_condition_2:
            global mode
            mode = "endgame"

            # Getting all 10 words BONUS
            if end_game_condition_2:
                time_bonus = cur_game.max_time - float(disp_clock[:-1])
                time_bonus *= 15
                time_bonus = int(time_bonus)

                cur_game.game_score.add_points(100 + time_bonus)

            self.window.show_view(SriEndGameView())

    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        if key == 65307:  # ESCAPE for menu
            global mode
            mode = "menu"
            self.window.show_view(SriMenuView(self))

        # Selecting a word
        number = key_code_to_number(key)
        if number in range(0, 9 + 1):
            cur_game.actions_performed += 1
            if ((cur_game.article.used_words[-1])[-1].upper() ==
               (cur_game.article.all_words[number])[0].upper()):

                temp = cur_game.article.all_words[number]
                cur_game.article.used_words.append(temp)
                cur_game.game_score.add_words_linked(1)

        if key == 117:  # U for undo
            if len(cur_game.article.used_words) > 1:
                cur_game.article.used_words.pop(-1)
                cur_game.game_score.add_words_linked(-1)
                cur_game.actions_performed += 1


class SriInstructionsView(arcade.View):
    instruction_mode = "instructions"

    global PRESS_ANY_KEY_TEXT
    button_text = (PRESS_ANY_KEY_TEXT[:13] +
                   " other than (SPACE) " +
                   PRESS_ANY_KEY_TEXT[14:])

    instruction_text = """
    ----- INSTRUCTIONS -----

    The Goal:
    --------------------
    To link as many words as possible within the time limit!


    How To Link Words:
    --------------------
    Press the number key for the
    corresponding word you would like to link.

    The last letter of the current word and
    the first letter of the word you would like to link
    must be the same to be able to link words.


    More
    --------------------
    Press (U) to undo your action.

    BEWARE: There are multiple ways to link words

    """

    story_text = """
    ----- STORY -----

    One day, you're reading the newspaper.
    You read SO MANY newspaper articles today.
    You're reading some article about something ...
    You just don't know what.

    You're head is spinning with all that news.
    Then SUDDENLY ...

    *POOF*

    The words are organized in a list of 10 words.
    You inspect the words a bit ... and then ...

    You realize that you can link the words!

    You then decide to play a game with the words to relax
    your spinning head from all those articles.


    """

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)

    def on_draw(self):
        arcade.start_render()

        if SriInstructionsView.instruction_mode == "instructions":
            arcade.draw_text("Press (SPACE) to read the story",
                             0.99 * WIDTH, 0.003 * HEIGHT,
                             TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)),
                             anchor_x="right", align="left")
            arcade.draw_text(SriInstructionsView.instruction_text,
                             0.5 * WIDTH,  0 * HEIGHT,
                             TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)),
                             anchor_x="center", align="center")

        elif SriInstructionsView.instruction_mode == "story":
            arcade.draw_text("Press (SPACE) to read the instructions",
                             0.99 * WIDTH, 0.003 * HEIGHT,
                             TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)),
                             anchor_x="right", align="left")
            arcade.draw_text(SriInstructionsView.story_text,
                             0.5 * WIDTH, 0 * HEIGHT,
                             TEXT_COLOR, font_size=(0.015 * (HEIGHT + WIDTH)),
                             anchor_x="center", align="center")

        arcade.draw_text(SriInstructionsView.button_text,
                         0.01 * WIDTH, 0.003 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)),
                         anchor_x="left", align="left")

    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        if key == 32:  # SPACE for switch mode
            if SriInstructionsView.instruction_mode == "instructions":
                SriInstructionsView.instruction_mode = "story"
            elif SriInstructionsView.instruction_mode == "story":
                SriInstructionsView.instruction_mode = "instructions"
        else:  # Press any key (except space) to go to menu
            global mode
            mode = "menu"
            self.window.show_view(SriMenuView(self))


class SriScoreBoardView(arcade.View):
    nuke_counter = 0
    drop_counter = 0
    drop_rank = 0

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)

    def on_draw(self):
        arcade.start_render()

        # Score Board Title and Related
        arcade.draw_text("Score Board", WIDTH/2, 0.9 * HEIGHT,
                         TEXT_COLOR, font_size=((HEIGHT + WIDTH) // 50),
                         anchor_x="center", align="right")

        arcade.draw_text(PRESS_ANY_KEY_TEXT, 0.175 * WIDTH, 0.003 * HEIGHT,
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)),
                         anchor_x="center", align="right")

        # Scores
        top_5_games = (Game.get_top_games())[0:5]

        for i in range(len(top_5_games)):
            score_text = (f'{i + 1}.' +
                          f'"{(top_5_games[i]).game_score.get_player()}" ---- ' +
                          f'{(top_5_games[i]).game_score.get_points()} points ---- ' +
                          f'{top_5_games[i].game_score.get_words_linked()} words linked')
            arcade.draw_text(score_text,
                             WIDTH * 0.3, 0.8 * HEIGHT - HEIGHT * 0.07 * i * 2,
                             arcade.color.BLUE, 18, align="left")

    def update(self, delta_time: float):
        global save_file
        save_file.save()

    def on_key_press(self, key, modifiers):
        if key == 110:  # N for nuke
            SriScoreBoardView.nuke_counter += 1
            if SriScoreBoardView.nuke_counter >= 10:
                global save_file
                SriScoreBoardView.nuke_counter = 0
                save_file.nuke()
                save_file.load_from_file()

        elif key == 100:  # D for drop
            SriScoreBoardView.drop_counter += 1
            if SriScoreBoardView.drop_counter >= 10:
                SriScoreBoardView.drop_counter = 0
                if SriScoreBoardView.drop_rank <= len(Game.get_top_games()):
                    games = Game.get_top_games()
                    games.pop(SriScoreBoardView.drop_rank - 1)
                    Game.all_games = games

        # Dropping a specific score in the top 5
        elif key_code_to_number(key) in range(1, 5 + 1):
            SriScoreBoardView.drop_rank = key_code_to_number(key)

        # Returning to the menu
        else:
            self.window.show_view(SriMenuView(self))
            global mode
            mode = "menu"


class SriEndGameView(arcade.View):

    global PRESS_ANY_KEY_TEXT

    button_text = (PRESS_ANY_KEY_TEXT[:13] +
                   " other than the numbers  " +
                   PRESS_ANY_KEY_TEXT[14:])

    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(SCREEN_COLOR)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("Press any key (other than the numbers) to return to the menu",
                         0.5 * WIDTH, HEIGHT - (0.03 * HEIGHT),
                         TEXT_COLOR, font_size=(0.01 * (HEIGHT + WIDTH)),
                         anchor_x="center", align="center")

        global cur_game

        arcade.draw_text(f"Player: {cur_game.game_score.get_player()}\n\nWords Linked: {cur_game.game_score.get_words_linked()}\n\nPoints: {cur_game.game_score.get_points()}\n\nRank: {cur_game.game_score.find_rank()}", 0.5 * WIDTH, 0.2 * HEIGHT,
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


class Converting:
    def game_display_time(self, decimal_places: int = 3) -> str:
        if decimal_places < 0:
            decimal_places = 0

        disp_clock = delta_time(self.start_time, time())
        disp_clock = round(disp_clock, decimal_places)

        return f"{disp_clock}"

    # @staticmethod


class Game(Converting):
    """A class used to store the information about a game.

    Attributes:
        all_games (List[game]): A list of all of the Game objects created.
    """
    all_games = []

    def __init__(self, current_player: str):
        """Create a Game object and assign attributes to it.

        The Game object stores itself in the class field all_games.

        Args:
            current_player (str): The name of the current player.

        Attributes:
            game_score (Score): A Score object.
            article (Article): An Article object.
            start_time (float): The Epoch time at the start of the game.
            max_time (int): The maximum time (in seconds)
                the game should be running.
            actions_performed (int): The number of actions performed during the game.
        """
        self.game_score = Score(current_player)
        self.article = Article()
        self.start_time = time()
        self.max_time = 30
        self.actions_performed = 0
        Game.all_games.append(self)

    def calculate_points(self) -> None:
        """Calculates the current points of the game.

        Args:
            None

        Returns:
            int: the current points for the game.
        """
        base_score = 10 * self.game_score.get_words_linked()
        base_score -= self.actions_performed

        return base_score

    def update_points(self) -> None:
        """Updates the current amount of points.

        Args:
            None

        Returns:
            None
        """
        self.game_score.change_points(self.calculate_points())

    @classmethod
    def get_top_games(cls) -> None:
        """Gets the top games, sorted by score points (highest to least).

        Args:
            None

        Returns:
            List[Game]: A list of all of the games, organized by score points.
        """
        return Game.merge_sort_games_by_score(cls.all_games)

    @staticmethod
    def merge_sort_games_by_score(nums: List["Game"]) -> List["Game"]:
        """A recursive method that sorts the games based on score points

        Args:
            nums (List[Game]): A list of Game objects.

        Returns:
            List[Game]: A list of Game objects (sorted by score points).
        """
        if len(nums) <= 1:
            return nums

        midpoint = len(nums) // 2

        left_side = Game.merge_sort_games_by_score(nums[:midpoint])
        right_side = Game.merge_sort_games_by_score(nums[midpoint:])

        sorted_list = []

        left_marker = 0
        right_marker = 0

        while left_marker < len(left_side) and right_marker < len(right_side):

            if (left_side[left_marker].game_score.get_points() >
               right_side[right_marker].game_score.get_points()):
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


class Score:
    """A class used to store the information about a score."""
    def __init__(self, player: str):
        """Create a Score object and assign attributes to it.

        Args:
            player (str): The name of the player.

        Attributes:
            _points (int): The number of points.
            _player (str): The name of the player.
            _time (float): The Epoch time at the creation
                of the Score object.
            _words_linked (int): The number of words
                the player linked in the game.
        """
        self._points = 0
        self._player = player
        self._time = time()
        self._words_linked = 0

    def change_points(self, points: int) -> None:
        """Setter for _points.

        Args:
            points (int): The value that _points should be set to.

        Returns:
            None
        """
        if isinstance(points, int):
            self._points = points
        else:
            raise Exception("Points should be an integer")

    def add_points(self, points: int) -> None:
        """Allows points to be added to _points.

        Args:
            points (int): The value that should be added to _points.

        Returns:
            None
        """
        if isinstance(points, int):
            self._points += points
        else:
            raise Exception("Points should be an integer")

    def get_points(self) -> None:
        """Getter for _points.

        Args:
            None

        Returns:
            None
        """
        return self._points

    def set_player(self, player: str) -> None:
        """Setter for _player.

        Args:
            player (str): The value that _player should be set to.

        Returns:
            None
        """
        if isinstance(player, str):
            self._player = player
        else:
            self._player = str(player)

    def get_player(self) -> None:
        """Getter for _player.

        Args:
            None

        Returns:
            None
        """
        return self._player

    def set_time(self, time: float) -> None:
        """Setter for _time.

        Args:
            time (float): the value that _time should be set to.

        Returns:
            None
        """
        if isinstance(time, float) and time > 0:
            self._time = time
        else:
            raise Exception("Time should be a positive float")

    def get_time(self) -> None:
        """Getter for _time.

        Args:
            None

        Returns:
            None
        """
        return time

    def get_words_linked(self) -> None:
        """Getter for _words_linked.

        Args:
            None

        Returns:
            None
        """
        return self._words_linked

    def add_words_linked(self, num: int) -> None:
        """Allows the number of words linked to be added to.

        Args:
            num (int): The number that should be added to _words_linked.
        Returns:
            None
        """
        if isinstance(num, int):
            self._words_linked += num
        else:
            raise Exception("Points should be an integer")

    def find_rank(self) -> int:
        """Finds the rank of the current Score object.

        Args:
            None
        Returns:
            int: The rank of the current Score object.
        """
        games = Game.get_top_games()

        for i in range(len(games)):
            if games[i].game_score == self:
                rank = i
                break

        return rank + 1


class Article:
    """A class used to store the information about an article."""
    def __init__(self):
        """Create an Article object and assigns attributes to it.

        Args:
            None

        Attributes:
            title (str): The title of the article.
            author (str): The name of the author of the article.
            date (str): The date the article was published.
                Format: DD/MM/YYYY.
                DD could be D AND/OR MM could be M.
            all_words(List[str]): A list of all of the words in the article.
            used_words(List[str]): A list of all of
                the used words in the article.
            starting_word(str): The starting word of the article.
        """
        self.title = Article.make_title(3)
        self.author = f'{Article.make_name("Berock")} {Article.make_name("Obamer")}'
        self.date = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1600, 2300)}"

        self.make_game_words()
        self.starting_word = self.all_words[0]
        self.all_words = self.all_words[1:]
        self.used_words = [self.starting_word]
        random.shuffle(self.all_words)

    def make_game_words(self) -> None:
        """Curates a list of the words in the article

        Args:
            None
        Returns:
            None
        """
        all_words = get_words_by_letter()
        starting_letter = random_letter()
        starting_word = random_word_from_list(all_words[starting_letter][:])
        final_words = [starting_word]

        for i in range(10):
            letter = final_words[i][-1].upper()
            word = random_word_from_list(((all_words[letter])[:]))
            final_words.append(word)

        self.all_words = final_words

        # Debugging words
        # Uncomment if needed
        # self.all_words = "qw we er rt ty yu ui io op pa am".split()

    @staticmethod
    def make_title(num_words: int, max_length: int = 25) -> str:
        """Makes a title for the article

        Args:
            num_words (int): How long (number of words) the title should be.
            max_length (int, optional): How long (length) the tite should be.
        Returns:
            str: The title of the article.
        """
        words = get_words()
        random.shuffle(words)

        title = ""

        for i in range(num_words):
            rand_word = random.choice(words)
            rand_word = rand_word[0].upper() + rand_word[1:].lower()

            if len(title) + len(rand_word) > max_length:
                continue

            title += (rand_word + " ")

        if len(title) == 0:
            title = "News Article"

        title = title[:-1]
        # title = title[:]

        return title

    @staticmethod
    def make_name(backup: str) -> str:
        """Makes a name

        Args:
            backup (str): A backup name incase a name was not able to be made
        Returns:
            str: A name
        """
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
    """A class used to store save date information"""
    def __init__(self):
        """Create a SaveDate object and assigns attributes to it.

        Args:
            None

        Returns:
            None
        """
        global mode
        self.game_mode = "menu"
        self.games = Game.all_games

    def load_from_file(self, save_file: str = PICKLE_FILE):
        """Loads save data from file. Saves into object.

        Args:
            save_file (str, optional): The link to the save file.
        Returns:
            None
        """
        try:
            save_files = pickle.load(open(save_file, "rb"))
        except EOFError:
            self.game_mode = "menu"

        try:
            self.game_mode = save_files["game_mode"]
            self.games = save_files["games"]
        except KeyError:
            self.game_mode = "menu"
            self.games = []
        except UnboundLocalError:
            self.game_mode = "menu"
            self.games = []

        global mode
        Game.all_games = self.games
        mode = self.game_mode

    def save(self, save_file: str = PICKLE_FILE):
        """Saves object to save file.

        Args:
            save_file (str, optional): The link to the save file.
        Returns:
            None
        """
        self.games = Game.all_games

        save_files = {
            "game_mode": self.game_mode,
            "games": self.games
        }

        pickle.dump(save_files, open(save_file, "wb"))

    def nuke(self, save_file: str = PICKLE_FILE):
        """Nukes save file. (Erases save file contents).

        Args:
            save_file (str, optional): The link to the save file.
        Returns:
            None
        """
        pickle.dump({}, open(save_file, "wb"))


global save_file
save_file = SaveData()
save_file.load_from_file()


def random_word_from_list(words: List[str]) -> str:
    """Chooses and returns a random word from a list of words

    Args:
        words (List[str]): The list of words.

    Returns:
        str: the random word from the list.
    """
    random.shuffle(words)
    return words[0]


def random_letter() -> str:
    """Chooses and returns a random capital letter from the alphabet

    Args:
        None

    Returns:
        str: a random capital letter from the alphabet
    """
    rand_letter = random.randint(0, 25)
    rand_letter = LETTERS[rand_letter]
    return rand_letter


def get_words() -> List[str]:
    """Parses and creates a list of words from WORD_FILE.

    Args:
        None

    Returns:
        List[str]: A list of words from WORD_FILE.
    """
    lines = []
    with open(WORD_FILE, "r") as f:
        for line in f:
            lines.append(line.strip())

    return lines


def key_code_to_letter(key_code: int) -> str:
    """Converts key codes that correspond to letters into their corresponding letter

    Args:
        key_code (int): The key code.

    Returns:
        str: The capital letter the key code corresponds to.
    """

    # A -> 97
    # Z -> 122

    key_code -= 97

    return LETTERS[key_code]


def key_code_to_number(key_code: int) -> int:
    """Converts key codes that correspond to numbers into their corresponding number

    Args:
        key_code (int): The key code.

    Returns:
        int: The number the key code corresponds to.
    """
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
    """Returns the how much time passed from time_1 to time_2

    Args:
        time_1 (float): The first time in milliseconds.
        time_2 (float): The second time in milliseconds.

    Returns:
        float: The difference between time_2 and time_1.
    """
    return time_2 - time_1


def convert_date_to_words(slash_date: str) -> str:
    """Converts the date in slash format to the date in words

    Args:
        slash_date (str): The date in slash format. Format: DD/MM/YYYY
            DD could be D
            MM could be M
            Example: 02/10/1920
            Example: 2/7/2003

    Returns:
        str: A string of the date in words. Format: {day_of_week} {day_of_month} {month} {year}
            Example: Wednesday 15 January 2020
            Example: Friday 03 November 1876
    """
    slash_date = slash_date.split("/")

    for i in range(len(slash_date)):
        slash_date[i] = int(slash_date[i])

    words = date(day=slash_date[0],
                 month=slash_date[1],
                 year=slash_date[2]).strftime('%A %d %B %Y')

    return words


def get_words_by_letter() -> Dict[str, List[str]]:
    """Call get_words() and organizes words into a dictionary based on the first letter of the word

    Args:
        None

    Returns:
        Dict: A dictionary with 27 keys being the letters of the alphabet and ETC.
            Each value will be list of words where each word starts with the respective key.
            Any word that doesn't start with a letter in the alphabet will be placed in ETC.
    """
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
