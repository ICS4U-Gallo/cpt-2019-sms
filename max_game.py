import arcade
import settings
import math
import random
from time import strftime, gmtime
import copy

game = []
incorrect_coordinates = []
all_start_boards = [
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

class Sudoku:
    def __init__(self, start_board):
        self.columns = 9
        self.rows = 9
        self.start_board = start_board
        self.board = copy.deepcopy(start_board)
        self.selected = (math.ceil(self.columns / 2), math.ceil(self.rows / 2))
        self.temp_values = {(i, j):[] for i in range(9) for j in range(9)}
        self.x_gap = settings.WIDTH / self.columns
        self.y_gap = settings.HEIGHT / self.rows
        self.pencil_mode = False
        self.validate_button = arcade.Sprite(center_x=133.33, center_y=50)
        self.validate_button.texture = arcade.make_soft_circle_texture(65,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)
        self.solve_button = arcade.Sprite(center_x=666.66, center_y=50)
        self.solve_button.texture = arcade.make_soft_circle_texture(65,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)
        self.reset_button = arcade.Sprite(center_x=750, center_y=575)
        self.reset_button.texture = arcade.make_soft_circle_texture(35,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)
        self.pencil_button = arcade.Sprite(center_x=400, center_y=50)
        self.pencil_button.texture = arcade.make_soft_circle_texture(65,
                                                               arcade.color.LIGHT_SLATE_GRAY,
                                                               outer_alpha=255)

    def reset_board(self):
        self.board = copy.deepcopy(self.start_board)
        self.temp_values = {(i, j):[] for i in range(9) for j in range(9)}

    def find_temp_value(self, target, coordinate):
        present = False
        for i, num in enumerate(self.temp_values[coordinate]):
            if num == target:
                del self.temp_values[coordinate][i]
                present = True
        if not present:
            self.temp_values[coordinate].append(target)
    
    def find_empty(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if not self.board[row][column]:
                    return (row, column)
        return None

    def solve(self):
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
            

    def find_invalid(self):
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

    def sort_temp_values(self):
        for y in range(self.rows):
            for x in range(self.columns):
                coordinate = (y, x)
                times_through = 0
                sorted = False
                while not sorted:
                    sorted = True
                    for i in range(len(self.temp_values[coordinate]) - 1 - times_through):
                        if self.temp_values[coordinate][i] > self.temp_values[coordinate][i + 1]:
                            self.temp_values[coordinate][i], self.temp_values[coordinate][i + 1] = self.temp_values[coordinate][i + 1], self.temp_values[coordinate][i]
                            sorted = False
                        else:
                            pass
                    times_through += 1

    def display_temp_values(self):
        for y in range(self.rows):
            for x in range(self.columns):
                coordinate = (y, x)
                text = ' ' + ''.join(str(num) for num in self.temp_values[coordinate])
                translated_x = self.x_gap * (3/2) + ((self.x_gap) * (x - 1))
                translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y)
                arcade.draw_text(text, translated_x, translated_y - 70,
                         arcade.color.RED,font_size=10, font_name='arial', anchor_x="center")

    def display_grid(self):
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
                color = arcade.color.BLIZZARD_BLUE

            arcade.draw_rectangle_filled(x_pos, settings.HEIGHT / 1.865, thickness, settings.HEIGHT / (4/3), color)
        
        # VERTICAL LINES
        for i in range(1, self.rows):
            y_pos += (settings.HEIGHT / (4/3)) / 9

            if i % 3 != 0:
                thickness = 1
                color = arcade.color.LIGHT_SLATE_GRAY
            else:
                thickness *= 3
                color = arcade.color.BLIZZARD_BLUE

            arcade.draw_rectangle_filled(settings.WIDTH / 2, y_pos, thickness, settings.WIDTH, color, tilt_angle=90)

    def display_numbers(self):
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
                            arcade.color.BLIZZARD_BLUE,font_size=18, font_name='arial', anchor_x="center")

    def display_selected(self):
        x = self.selected[0]
        y = self.selected[1]
        translated_x = self.x_gap / 2 + ((self.x_gap) * (x - 1))
        translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y) 
        arcade.draw_circle_filled(translated_x, translated_y - 1, 17, arcade.color.BLIZZARD_BLUE)

    def display_incorrect_background(self, coordinate):
        x = coordinate[1]
        y = coordinate[0]
        translated_x = self.x_gap / 2 + ((self.x_gap) * (x - 1))
        translated_y = settings.HEIGHT / (settings.HEIGHT / 575) - ((settings.HEIGHT / 12) * y)      
        arcade.draw_circle_filled(translated_x + 88.88, translated_y - 51, 17, arcade.color.CADMIUM_RED)
        arcade.draw_text(str(self.board[y][x]), translated_x + 88.88, translated_y - 60,
                            arcade.color.GHOST_WHITE,font_size=18, font_name='arial', anchor_x="center")

class Winner:
    all_winners = []

    def __init__(self, name, time):
        self.name = name
        self.time = time
        all_winners.append(self)
    
    @classmethod
    def create_anon_winner(cls, time):
        return Winner('Anonymous', time)


class Menu(arcade.View):
    pass

class Instructions(arcade.View):
    pass

class MaxGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.seconds_elapsed = 0

    def on_show(self):
        global game
        arcade.set_background_color(arcade.color.EERIE_BLACK)
        # if/else statement is necessary for the game instance to be created when the program runs from max_game.py and main.py
        if game != []:
            pass
        else:
            board_index = random.randrange(len(all_start_boards))
            game = Sudoku(all_start_boards[board_index])
    
    def on_draw(self):
        self.timer = strftime("%H:%M:%S", gmtime(self.seconds_elapsed))
        arcade.start_render()
        arcade.draw_text(self.timer, settings.WIDTH / 2, 565,
                         arcade.color.LIGHT_GRAY,font_size=18, font_name='arial', anchor_x="center")
        game.display_grid()
        game.display_selected()
        game.display_numbers()
        game.display_temp_values()

        if incorrect_coordinates:
            for coordinate in incorrect_coordinates:
                game.display_incorrect_background(coordinate)

        game.validate_button.draw()
        game.solve_button.draw()
        game.reset_button.draw()
        game.pencil_button.draw()

        arcade.draw_text('V', 133.33, 30,
                         arcade.color.BLIZZARD_BLUE,font_size=40, font_name='arial', anchor_x="center")
        arcade.draw_text('P', 400, 30,
                         arcade.color.BLIZZARD_BLUE,font_size=40, font_name='arial', anchor_x="center")
        arcade.draw_text('S', 666.66, 30,
                         arcade.color.BLIZZARD_BLUE,font_size=40, font_name='arial', anchor_x="center")
        arcade.draw_text('R', 750, 565,
                         arcade.color.BLIZZARD_BLUE,font_size=20, font_name='arial', anchor_x="center")

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
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 1
                    incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 1
            elif symbol == 50:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 2
                    incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 2
            elif symbol == 51:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 3
                    incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 3
            elif symbol == 52:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 4
                    incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 4
            elif symbol == 53:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 5
                    incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 5
            elif symbol == 54:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 6
                    incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 6
            elif symbol == 55:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 7
                    incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 7
            elif symbol == 56:
                
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 8
                    incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 8
            elif symbol == 57:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 9
                    incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 9
            elif symbol == 65288 or symbol == 48:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 0
                    incorrect_coordinates.remove(coordinate)
                else:
                    game.board[y][x] = 0
            else:
                pass
        
        if game.pencil_mode:
            if game.start_board[y][x]:
                    pass
            elif symbol == 49:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 0
                    incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(1, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(1, coordinate)
            elif symbol == 50:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 0
                    incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(2, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(2, coordinate)
            elif symbol == 51:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 0
                    incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(3, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(3, coordinate)
            elif symbol == 52:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 0
                    incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(4, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(4, coordinate)
            elif symbol == 53:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 0
                    incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(5, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(5, coordinate)
            elif symbol == 54:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 0
                    incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(6, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(6, coordinate)
            elif symbol == 55:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 0
                    incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(7, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(7, coordinate)
            elif symbol == 56:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 0
                    incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(8, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(8, coordinate)
            elif symbol == 57:
                if coordinate in incorrect_coordinates:
                    game.board[y][x] = 0
                    incorrect_coordinates.remove(coordinate)
                    game.find_temp_value(9, coordinate)
                else:
                    game.board[y][x] = 0
                    game.find_temp_value(9, coordinate)
            else:
                pass
            game.sort_temp_values()

        if symbol == 65307:
            pause_screen = PauseScreen(self)
            self.window.show_view(pause_screen)
        else:
            pass
    
    def on_update(self, delta_time):
        self.seconds_elapsed += delta_time
    
    def on_mouse_press(self, x, y, button, modifiers):
        global incorrect_coordinates
        x_coordinate = math.ceil(x / (settings.WIDTH / 9))
        y_coordinate = 11 - math.ceil((y - (settings.HEIGHT / 12)) / (settings.HEIGHT / 12))
        if x_coordinate <= 9 and y_coordinate <= 9 and x_coordinate > 0 and y_coordinate > 0:
            game.selected = (x_coordinate, y_coordinate)
        
        if game.validate_button.collides_with_point([x, y]):
            incorrect_coordinates = game.find_invalid()
        
        if game.solve_button.collides_with_point([x, y]):
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


    def on_key_press(self, symbol, modifiers):
        if symbol == 65307: # escape
            self.window.next_view()
        elif symbol == 65293: # enter
            self.window.show_view(self.game_view)
        else:
            pass

class Leaderboard(arcade.View):
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
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    game_view = MaxGameView()
    window.show_view(game_view)
    arcade.run()

if __name__ != "__main__":
    #set-up for main.py
    game_view = MaxGameView()