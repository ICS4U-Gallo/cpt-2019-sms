import arcade
import settings
import math
import random
import pickle
from time import strftime, gmtime
import copy
from typing import List, Dict, Tuple

user = None
winner = None
game = None
game_view = None
data = []

#what do i encapsulate?

class Sudoku:
    ALL_START_BOARDS: List[List[int]] = [
            [[7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]],
            
            [[0, 4, 0, 8, 0, 5, 2, 0, 0],
            [0, 2, 0, 0, 4, 0, 0, 5, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 9, 0, 0, 0, 3, 1, 2, 0],
            [1, 0, 6, 0, 7, 8, 0, 0, 3],
            [3, 7, 0, 9, 0, 4, 0, 8, 0],
            [0, 0, 0, 0, 0, 6, 7, 0, 0],
            [0, 0, 8, 3, 5, 9, 0, 1, 0],
            [0, 1, 9, 0, 0, 7, 6, 0, 0]],

            [[0, 6, 0, 3, 0, 0, 8, 0, 4],
            [5, 3, 7, 0, 9, 0, 0, 0, 0],
            [0, 4, 0, 0, 0, 6, 3, 0, 7],
            [0, 9, 0, 0, 5, 1, 2, 3, 8],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [7, 1, 3, 6, 2, 0, 0, 4, 0],
            [3, 0, 6, 4, 0, 6, 0, 1, 0],
            [0, 0, 0, 0, 6, 0, 5, 2, 3],
            [1, 0, 2, 0, 0, 9, 0, 8, 0]]
    ]

    def __init__(self, start_board: List[List[int]], user: "User") -> None:
        self.start_board = start_board
        self.user = user
        self.columns: int = 9
        self.rows: int = 9
        self.board: List[List[int]] = copy.deepcopy(start_board)
        self.selected: Tuple[int, int] = (math.ceil(self.columns / 2), math.ceil(self.rows / 2))
        self.temp_values: Dict[Tuple[int, int]] = {(i, j):[] for i in range(self.columns) for j in range(self.rows)}
        self.x_gap: int = settings.WIDTH / self.columns
        self.y_gap: int = settings.HEIGHT / self.rows
        self.pencil_mode: bool = False
        self.incorrect_coordinates: List[Tuple[int, int]] = []
        self.validate_button: Sprite = arcade.Sprite(center_x=133.33, center_y=50)
        self.validate_button.texture: Sprite.texture = arcade.make_soft_circle_texture(65,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)
        self.solve_button: Sprite = arcade.Sprite(center_x=666.66, center_y=50)
        self.solve_button.texture: Sprite.texture = arcade.make_soft_circle_texture(65,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)
        self.reset_button: Sprite = arcade.Sprite(center_x=751.5, center_y=575)
        self.reset_button.texture: Sprite.texture = arcade.make_soft_circle_texture(37,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)
        self.pencil_button: Sprite = arcade.Sprite(center_x=400, center_y=50)
        self.pencil_button.texture: Sprite.texture = arcade.make_soft_circle_texture(65,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)

    def reset_board(self) -> None:
        self.board = copy.deepcopy(self.start_board)
        self.temp_values = {(i, j):[] for i in range(9) for j in range(9)}
        self.incorrect_coordinates = []

    def find_temp_value(self, target, coordinate) -> None:
        present = False
        for i, num in enumerate(self.temp_values[coordinate]):
            if num == target:
                del self.temp_values[coordinate][i]
                present = True
        if not present:
            self.temp_values[coordinate].append(target)
    
    def find_empty(self) -> Tuple[int, int]:
        for row in range(self.rows):
            for column in range(self.columns):
                if not self.board[row][column]:
                    return (row, column)
        return None

    def solve(self) -> bool:
        if not self.find_empty() and not self.find_invalid():
            return True
        else:
            coordinate = self.find_empty()
            row = coordinate[0]
            column = coordinate[1]

        for i in range(1, 10):
            self.board[row][column] = i
            result = self.find_invalid()
            if (row, column) in result:
                self.board[row][column] = 0
                continue
            
            if self.solve():
                return True
            
            self.board[row][column] = 0
        
        return False

    def find_invalid(self) -> List[Tuple[int, int]]:
        all_invalid_coordinates = []
        for column in range(self.columns):
            for row in range(self.rows):
                target = self.board[row][column]
                #row check
                for y in range(self.rows):
                    if target == self.board[y][column] and row != y and self.board[y][column] != 0:
                        coordinate = (y, column)
                        all_invalid_coordinates.append(coordinate)

        for row in range(self.rows):
            for column in range(self.columns):
                target = self.board[row][column]
                #column check
                for x in range(self.columns):
                    if target == self.board[row][x] and column != x and self.board[row][x] != 0:
                        coordinate = (row, x)
                        all_invalid_coordinates.append(coordinate)
        
        for row in range(self.rows):
            for column in range(self.columns):
                if not self.board[row][column]:
                    continue

                coordinate = (row, column)
                target = self.board[row][column]
                block_x = column // 3
                block_y = row // 3

                if block_x == 0:
                    start_x = 0
                    multiplier_x = 0
                elif block_x == 1:
                    start_x = 3
                    multiplier_x = 1
                else:
                    start_x = 6
                    multiplier_x = 2
                
                if block_y == 0:
                    start_y = 0
                    multiplier_y = 0
                elif block_y == 1:
                    start_y = 3
                    multiplier_y = 1
                else:
                    start_y = 6
                    multiplier_y = 2
                
                block = self.board[start_y:start_y+3]
                for y in range(len(block)):
                    new_row = block[y][start_x:start_x+3]
                    for x, number in enumerate(new_row):
                        number_coordinate_y = y + 3 * multiplier_y
                        number_coordinate_x = x + 3 * multiplier_x
                        number_coordinate = (number_coordinate_y, number_coordinate_x)
                        if number == target and number_coordinate != coordinate:
                            all_invalid_coordinates.append(coordinate)

        invalid_coordinates = []
        for coordinate in all_invalid_coordinates:
            y = coordinate[0]
            x = coordinate[1]
            if self.start_board[y][x] == 0:
                #can implement search here
                invalid_coordinates.append(coordinate)

        if not invalid_coordinates:
            return []

        return set(invalid_coordinates)

    def sort_temp_values(self, numbers: List[int]) -> List[int]:
        if len(numbers) <= 1:
            return numbers
        
        mid = len(numbers) // 2
        left_side = self.sort_temp_values(numbers[:mid])
        right_side = self.sort_temp_values(numbers[mid:])
        sorted_list = []
        
        left_pointer = 0
        right_pointer = 0

        while left_pointer < len(left_side) and right_pointer < len(right_side):
            if left_side[left_pointer] < right_side[right_pointer]:
                sorted_list.append(left_side[left_pointer])
                left_pointer += 1
            else:
                sorted_list.append(right_side[right_pointer])
                right_pointer += 1
        
        while left_pointer < len(left_side):
            sorted_list.append(left_side[left_pointer])
            left_pointer += 1
    
        while right_pointer < len(right_side):
            sorted_list.append(right_side[right_pointer])
            right_pointer += 1

        return sorted_list

    def display_temp_values(self) -> None:
        for y in range(self.rows):
            for x in range(self.columns):
                coordinate = (y, x)
                text = ' ' + ''.join(str(num) for num in self.temp_values[coordinate])
                translated_x = self.x_gap * (3/2) + ((self.x_gap) * (x - 1))
                translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y)
                arcade.draw_text(text, translated_x, translated_y - 70,
                         arcade.color.RED,font_size=10, font_name='arial', anchor_x="center")

    def display_grid(self) -> None:
        # REMOVE -- y_bottom is 100 and y_top is 550
        x_start = settings.WIDTH / 9
        y_pos = settings.HEIGHT / 6

        # HORIZONTAL LINES
        for i in range(1, self.columns):
            x_pos = x_start * i

            if i % 3 != 0:
                thickness = 1
                color = arcade.color.LIGHT_SLATE_GRAY
            else:
                thickness *= 3
                color = user.get_preferred_color()

            arcade.draw_rectangle_filled(x_pos, settings.HEIGHT / 1.865, thickness, settings.HEIGHT / (4/3), color)
        
        # VERTICAL LINES
        for i in range(1, self.rows):
            y_pos += (settings.HEIGHT / (4/3)) / 9

            if i % 3 != 0:
                thickness = 1
                color = arcade.color.LIGHT_SLATE_GRAY
            else:
                thickness *= 3
                color = user.get_preferred_color()

            arcade.draw_rectangle_filled(settings.WIDTH / 2, y_pos, thickness, settings.WIDTH, color, tilt_angle=90)

    def display_numbers(self) -> None:
        for row in range(self.rows):
            for column in range(self.columns):
                if self.start_board[row][column]:
                    x = column
                    y = row
                    translated_x = self.x_gap * (3/2) + ((self.x_gap) * (x - 1))
                    translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y)
                    arcade.draw_circle_filled(translated_x, translated_y - 51, 17, arcade.color.PAYNE_GREY)
                    # STARTING NUMBERS
                    arcade.draw_text(str(self.start_board[row][column]), translated_x, translated_y - 60,
                         arcade.color.LIGHT_GRAY,font_size=18, font_name='arial', anchor_x="center")
                elif self.board[row][column]:
                    x = column
                    y = row
                    translated_x = self.x_gap * (3/2) + ((self.x_gap) * (x - 1))
                    translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y)

                    if self.selected == (column + 1, row + 1):
                        arcade.draw_text(str(self.board[row][column]), translated_x, translated_y - 60,
                        # INPUTTED NUMBERS WHILE SELECTED
                         arcade.color.BLACK,font_size=18, font_name='arial', anchor_x="center")
                    else:
                        # INPUTTED NUMBERS
                        arcade.draw_text(str(self.board[row][column]), translated_x, translated_y - 60,
                            user.get_preferred_color(),font_size=18, font_name='arial', anchor_x="center")

    def display_selected(self) -> None:
        x = self.selected[0]
        y = self.selected[1]
        translated_x = self.x_gap / 2 + ((self.x_gap) * (x - 1))
        translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y) 
        arcade.draw_circle_filled(translated_x, translated_y - 1, 17, user.get_preferred_color())

    def display_incorrect_background(self, coordinate: Tuple[int, int]) -> None:
        x = coordinate[1]
        y = coordinate[0]
        if self.board[y][x] == 0:
            return None 
        translated_x = self.x_gap / 2 + ((self.x_gap) * (x - 1))
        translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y)      
        arcade.draw_circle_filled(translated_x + 88.88, translated_y - 51, 17, arcade.color.CADMIUM_RED)
        arcade.draw_text(str(self.board[y][x]), translated_x + 88.88, translated_y - 60,
                            arcade.color.GHOST_WHITE,font_size=18, font_name='arial', anchor_x="center")

class User:
    def __init__(self, name: str, preferred_color: "texture"):
        self._name = name
        self._preferred_color = preferred_color

    def get_name(self) -> str:
        return self._name

    def set_name(self, value: str) -> None:
        self._name = value
    
    def get_preferred_color(self) -> "color":
        return self._preferred_color

    def set_preferred_color(self, value: "color") -> None:
        self._preferred_color = value

    def display_name(self, x: int, y: int, center: bool=False):
        if center:
            arcade.draw_text(f"User: {self._name}", x, y, self._preferred_color, 
                            font_size=13, font_name='arial', anchor_x='center')
        else:
            arcade.draw_text(f"User: {self._name}", x, y, self._preferred_color, 
                        font_size=13, font_name='arial')

    @staticmethod
    def display_unpersonalized_name(x, y, center=False):
        if center:
            arcade.draw_text(f"User: Anon", x, y, arcade.color.WHITE, 
                            font_size=13, font_name='arial', anchor_x='center')
        else:
            arcade.draw_text("User: Anon", x, y, arcade.color.WHITE, 
                        font_size=13, font_name='arial')

class Winner(User):
    _all_winners = data

    def __init__(self, name: str, preferred_color: "color", time: float) -> None:
        super().__init__(name, preferred_color)
        self._time = time
    
    def get_name(self) -> str:
        return self._name

    def set_name(self, value: str) -> None:
        self._name = value

    def get_preferred_color(self) -> "color":
        return self._preferred_color
    
    def set_preferred_color(self, value: "color") -> None:
        self._preferred_color = value

    def get_time(self) -> float:
        return self._time

    def set_time(self, value: float) -> None:
        self._time = value

    @classmethod
    def create_anon_winner(cls, color, time):
        return cls('Anonymous', color, time)
    
    @classmethod
    def sort_all_winner_times(cls):
        sorted = False
        times_through = 0

        while not sorted:
            sorted = True
            for i in range(len(cls._all_winners) - 1 - times_through):
                if cls._all_winners[i]._time > cls._all_winners[i + 1]._time:
                    cls._all_winners[i], cls._all_winners[i + 1] = cls._all_winners[i + 1], cls._all_winners[i]
                    sorted = False
            times_through += 1

    @classmethod
    def display_all_winner_info(cls):
        y_pos = 500
        i = 0
        for i in range(len(cls._all_winners)):
            if i > 9:
                break
            text = f"{i + 1}. {cls._all_winners[i]._name} ------- {cls._all_winners[i]._time}s"
            arcade.draw_text(text, settings.WIDTH / 2, y_pos,
                        cls._all_winners[i]._preferred_color, font_size=15, font_name='arial', anchor_x="center")
            y_pos -= 50


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.play_button = arcade.Sprite(center_x=settings.WIDTH / 2, center_y=500)
        self.play_button.texture = arcade.make_soft_square_texture(50,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)
        self.instruction_button = arcade.Sprite(center_x=settings.WIDTH / 2, center_y=350)
        self.instruction_button.texture = arcade.make_soft_square_texture(50,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)
        self.leaderboard_button = arcade.Sprite(center_x=settings.WIDTH / 2, center_y = 200)
        self.leaderboard_button.texture = arcade.make_soft_square_texture(50,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)
        self.quit_button = arcade.Sprite(center_x=50, center_y = 550)
        self.quit_button.texture = arcade.make_soft_square_texture(50,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)

    def on_show(self):
        arcade.set_background_color(arcade.color.EERIE_BLACK)
    
    def on_draw(self):
        arcade.start_render()
        if not user.get_name():
            user.display_unpersonalized_name(settings.WIDTH - 150, 575)
        else:
            user.display_name(settings.WIDTH - 150, 575)
        arcade.draw_text('SUDOKU', settings.WIDTH / 2, 550, user.get_preferred_color(), 
                        font_size = 30, font_name = 'arial', anchor_x='center')
        self.play_button.draw()
        arcade.draw_text('P', settings.WIDTH / 2, 485, user.get_preferred_color(), 
                        font_size = 30, font_name = 'arial', anchor_x='center')
        arcade.draw_text('LAY', settings.WIDTH / 2 + 25, 485, user.get_preferred_color(), 
                        font_size = 30, font_name = 'arial')
        self.instruction_button.draw()
        arcade.draw_text('I', settings.WIDTH / 2, 335, user.get_preferred_color(), 
                        font_size = 30, font_name = 'arial', anchor_x='center')
        arcade.draw_text('NSTRUCTIONS', settings.WIDTH / 2 + 25, 335, user.get_preferred_color(), 
                        font_size = 30, font_name = 'arial')
        self.leaderboard_button.draw()
        arcade.draw_text('L', settings.WIDTH / 2, 185, user.get_preferred_color(), 
                        font_size = 30, font_name = 'arial', anchor_x='center')
        arcade.draw_text('EADERBOARD', settings.WIDTH / 2 + 25, 185, user.get_preferred_color(), 
                        font_size = 30, font_name = 'arial')
        self.quit_button.draw()
        arcade.draw_text('Q', 50, 535, user.get_preferred_color(), 
                        font_size = 30, font_name = 'arial', anchor_x='center')
        arcade.draw_text('UIT', 50 + 55, 535, user.get_preferred_color(), 
                        font_size = 30, font_name = 'arial', anchor_x='center')
    
    def on_mouse_press(self, x, y, button, modifiers):
        global game_view, game
        if self.play_button.collides_with_point([x, y]):
            game_view = MaxGameView()
            board_index = random.randrange(len(Sudoku.ALL_START_BOARDS))
            game = Sudoku(Sudoku.ALL_START_BOARDS[board_index], user)
            self.window.show_view(game_view)
        if self.instruction_button.collides_with_point([x, y]):
            instruction_view = Instructions()
            self.window.show_view(instruction_view)
        if self.leaderboard_button.collides_with_point([x, y]):
            leaderboard_view = LeaderboardView()
            self.window.show_view(leaderboard_view)
        if self.quit_button.collides_with_point([x, y]):
            self.window.next_view()
            

class Instructions(arcade.View):
    def __init__(self):
        super().__init__()
        with open('sudoku_instructions.txt', 'r', errors='ignore') as f:
            self.contents = f.read()
    
    def on_show(self):
        arcade.set_background_color(arcade.color.EERIE_BLACK)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == 65307:
            try:
                self.window.show_view(menu_view)
            except:
                menu_view = MenuView()
                self.window.show_view(menu_view)
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.contents, settings.WIDTH - 450, 200, user.get_preferred_color(), 
                        font_size = 13, font_name = 'arial', anchor_x='center')

class MaxGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.seconds_elapsed = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.EERIE_BLACK)
    
    def on_draw(self):
        self.timer = strftime("%H:%M:%S", gmtime(self.seconds_elapsed))
        arcade.start_render()
        arcade.draw_text(self.timer, settings.WIDTH / 2, 565,
                         arcade.color.LIGHT_GRAY,font_size=18, font_name='arial', anchor_x="center")
        
        game.display_selected()
        if not user.get_name():
            user.display_unpersonalized_name(settings.WIDTH / 2, 550, True)
        else:
            user.display_name(settings.WIDTH / 2, 550, True)
        if game.incorrect_coordinates:
            for coordinate in game.incorrect_coordinates:
                game.display_incorrect_background(coordinate)
        game.display_grid()
        game.display_numbers()
        game.display_temp_values()

        game.validate_button.draw()
        game.solve_button.draw()
        game.reset_button.draw()
        game.pencil_button.draw()

        arcade.draw_text('V', 133.33, 30,
                         user.get_preferred_color(),font_size=40, font_name='arial', anchor_x="center")
        arcade.draw_text('P', 400, 30,
                         user.get_preferred_color(),font_size=40, font_name='arial', anchor_x="center")
        arcade.draw_text('S', 666.66, 30,
                         user.get_preferred_color(),font_size=40, font_name='arial', anchor_x="center")
        arcade.draw_text('R', 750, 565,
                         user.get_preferred_color(),font_size=20, font_name='arial', anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        x = game.selected[0] - 1
        y = game.selected[1] - 1
        coordinate = (y, x)
        
        if not game.pencil_mode:
            if game.temp_values[(y, x)]:
                game.temp_values[(y, x)] = []
            if game.start_board[y][x]:
                    pass
            elif symbol == 49:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 1
                    game.incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 1
            elif symbol == 50:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 2
                    game.incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 2
            elif symbol == 51:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 3
                    game.incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 3
            elif symbol == 52:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 4
                    game.incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 4
            elif symbol == 53:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 5
                    game.incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 5
            elif symbol == 54:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 6
                    game.incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 6
            elif symbol == 55:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 7
                    game.incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 7
            elif symbol == 56:
                
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 8
                    game.incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 8
            elif symbol == 57:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 9
                    game.incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 9
            elif symbol == 65288 or symbol == 48:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 0
                    game.incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 0
            else:
                pass
        
        if game.pencil_mode:
            if game.start_board[y][x]:
                    pass
            elif symbol == 49:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 0
                    game.incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(1, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(1, coordinate)
            elif symbol == 50:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 0
                    game.incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(2, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(2, coordinate)
            elif symbol == 51:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 0
                    game.incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(3, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(3, coordinate)
            elif symbol == 52:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 0
                    game.incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(4, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(4, coordinate)
            elif symbol == 53:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 0
                    game.incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(5, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(5, coordinate)
            elif symbol == 54:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 0
                    game.incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(6, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(6, coordinate)
            elif symbol == 55:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 0
                    game.incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(7, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(7, coordinate)
            elif symbol == 56:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 0
                    game.incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(8, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(8, coordinate)
            elif symbol == 57:
                if coordinate in game.incorrect_coordinates:
                    game.board[y][x] = 0
                    game.incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(9, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(9, coordinate)
            else:
                pass
            for y in range(game.rows):
                for x in range(game.columns):
                    coordinate = (y, x)
                    numbers = game.temp_values[coordinate]
                    game.temp_values[coordinate] = game.sort_temp_values(numbers)

        if symbol == 65307:
            pause_screen = PauseScreen(self)
            self.window.show_view(pause_screen)
        else:
            pass
    
    def on_update(self, delta_time):
        self.seconds_elapsed += delta_time
    
    def on_mouse_press(self, x, y, button, modifiers):
        global winner
        x_coordinate = math.ceil(x / (settings.WIDTH / 9))
        y_coordinate = 11 - math.ceil((y - (settings.HEIGHT / 12)) / (settings.HEIGHT / 12))
        if x_coordinate <= 9 and y_coordinate <= 9 and x_coordinate > 0 and y_coordinate > 0:
            game.selected = (x_coordinate, y_coordinate)
        
        if game.validate_button.collides_with_point([x, y]):
            game.incorrect_coordinates = game.find_invalid()
            if not game.incorrect_coordinates and not game.find_empty():
                if not user.get_name():
                    winner = Winner.create_anon_winner(user.get_preferred_color(), round(self.seconds_elapsed, 1))
                else:
                    winner = Winner(user.get_name(), user.get_preferred_color(), round(self.seconds_elapsed, 1))
                
                data.append(winner)
                
                with open("sudoku_data.p", "wb") as f:
                    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

                win_view = WinView(self.seconds_elapsed)
                self.window.show_view(win_view)
        
        if game.solve_button.collides_with_point([x, y]):
            game.board = copy.deepcopy(game.start_board)
            game.solve()
            game.temp_values = {(i, j):[] for i in range(9) for j in range(9)}


        if game.reset_button.collides_with_point([x, y]):
            game.reset_board()

        if game.pencil_button.collides_with_point([x, y]):
            if game.pencil_mode == True:
                game.pencil_mode = False
                game.pencil_button.texture = arcade.make_soft_circle_texture(65,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)
            else:
                game.pencil_mode = True
                game.pencil_button.texture = arcade.make_soft_circle_texture(65,
                                                               arcade.color.BOSTON_UNIVERSITY_RED,
                                                               outer_alpha=255)

class PauseScreen(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.EERIE_BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('>PRESS <ESCAPE> TO GIVE UP', settings.WIDTH / 2, settings.HEIGHT / 2,
                         arcade.color.LIGHT_GRAY,font_size=25, font_name='arial', anchor_x="center")
        arcade.draw_text('>PRESS <ENTER> TO RESUME GAME', settings.WIDTH / 2, settings.HEIGHT / 1.5,
                         arcade.color.LIGHT_GRAY,font_size=25, font_name='arial', anchor_x="center")
        arcade.draw_text('>PRESS <M> TO RETURN TO THE MENU', settings.WIDTH / 2, settings.HEIGHT / 3,
                         arcade.color.LIGHT_GRAY, font_size=25, font_name='arial', anchor_x="center")


    def on_key_press(self, symbol, modifiers):
        if symbol == 65307: # escape
            self.window.next_view()
        elif symbol == 65293: # enter
            self.window.show_view(self.game_view)
        elif symbol == 109: # M
            try:
                self.window.show_view(menu_view)
            except:
                menu_view = MenuView()
                self.window.show_view(menu_view)
        else:
            pass

class IntroductionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.text = 'USERNAME: '
        self.preferred_color = None
        self.green_button = arcade.Sprite(center_x=settings.WIDTH / 2, center_y=500)
        self.green_button.texture = arcade.make_soft_square_texture(50,
                                                               arcade.color.GREEN_YELLOW,
                                                               outer_alpha=255)
        self.blue_button = arcade.Sprite(center_x=settings.WIDTH / 2, center_y=350)
        self.blue_button.texture = arcade.make_soft_square_texture(50,
                                                               arcade.color.BLIZZARD_BLUE,
                                                               outer_alpha=255)
        self.white_button = arcade.Sprite(center_x=settings.WIDTH / 2, center_y = 200)
        self.white_button.texture = arcade.make_soft_square_texture(50,
                                                               arcade.color.WHITE,
                                                               outer_alpha=255)
        self.key_translator = {
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
    
    def on_show(self):
        arcade.set_background_color(arcade.color.EERIE_BLACK)

    def on_draw(self):
        arcade.start_render()
        if not self.preferred_color:
            arcade.draw_text('CLICK YOUR PREFERRED COLOR', settings.WIDTH / 2, settings.HEIGHT - 50,
                            arcade.color.LIGHT_GRAY,font_size=15, font_name='arial', anchor_x="center")
            self.green_button.draw()
            self.blue_button.draw()
            self.white_button.draw()
        else:
            arcade.draw_text(self.text, settings.WIDTH / 2, settings.HEIGHT / 2, arcade.color.BLIZZARD_BLUE, font_size=25, anchor_x='center')
            arcade.draw_text('TYPE IN YOUR USERNAME AND PRESS <ENTER> TO CONTINUE', settings.WIDTH / 2, settings.HEIGHT - 50,
                            arcade.color.LIGHT_GRAY,font_size=15, font_name='arial', anchor_x="center")
    
    def on_key_press(self, symbol, modifiers):
        global user
        if self.preferred_color:
            try:
                for num_symbol, value in self.key_translator.items():
                    if symbol == 65288 and len(self.text) > 1:
                        self.text = self.text[:10]
                    elif num_symbol == symbol:
                        if len(self.text) > 18:
                            break
                        else:
                            letter = value
                            self.text += letter
                    else:
                        continue
            except:
                pass
            if symbol == 65293:
                name = self.text[10:]
                user = User(name, self.preferred_color)
                menu_view = MenuView()
                self.window.show_view(menu_view)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.green_button.collides_with_point([x, y]):
            self.preferred_color = arcade.color.GREEN_YELLOW
        if self.blue_button.collides_with_point([x, y]):
            self.preferred_color = arcade.color.BLIZZARD_BLUE
        if self.white_button.collides_with_point([x, y]):
            self.preferred_color = arcade.color.WHITE

class LeaderboardView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.EERIE_BLACK)
        Winner._all_winners = data
        Winner.sort_all_winner_times()
        

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('>PRESS <M> TO RETURN TO MENU', settings.WIDTH / 2, settings.HEIGHT - 50,
                         arcade.color.LIGHT_GRAY,font_size=25, font_name='arial', anchor_x="center")
        Winner.display_all_winner_info()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == 109: # M
            try:
                self.window.show_view(menu_view)
            except:
                menu_view = MenuView()
                self.window.show_view(menu_view)

class WinView(arcade.View):
    def __init__(self, time):
        super().__init__()
        self.time = round(time, 1)
    
    def on_show(self):
        arcade.set_background_color(arcade.color.EERIE_BLACK)
    
    def on_draw(self):
        arcade.start_render()
        if not user.get_name():
            text = f'Congratulation on winning, Anonymous! You completed this board with a time of: {self.time}'
        else:
            text = f'Congratulation on winning, {user.get_name()}! You completed this board with a time of: {self.time}'
        arcade.draw_text(text, settings.WIDTH / 2, settings.HEIGHT / 2,
                        user.get_preferred_color(), font_size=15, font_name='arial', anchor_x="center")
        arcade.draw_text('To return to the menu, press <M>', settings.WIDTH / 2, settings.HEIGHT / 1.5,
                        user.get_preferred_color(), font_size=15, font_name='arial', anchor_x="center")
        arcade.draw_text('To see the leaderboard, press <L>', settings.WIDTH / 2, settings.HEIGHT / 3,
                        user.get_preferred_color(), font_size=15, font_name='arial', anchor_x="center")
    
    def on_key_press(self, symbol, modifiers):
        if symbol == 109:
            global game, game_view
            del game
            del game_view
            try:
                self.window.show_view(menu_view)
            except:
                menu_view = MenuView()
                self.window.show_view(menu_view)
        if symbol == 108:
            board_index = random.randrange(len(Sudoku.ALL_START_BOARDS))
            leaderboard = LeaderboardView()
            self.window.show_view(leaderboard)

if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector
    with open("sudoku_data.p", "rb") as f:
        data = pickle.load(f)
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    introduction_view = IntroductionView()
    menu_view = MenuView()
    window.show_view(introduction_view)
    arcade.run()