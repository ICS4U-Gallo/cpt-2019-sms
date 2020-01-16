import arcade
import settings
import random
from typing import List

total_points = str(0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "MATCH OFF"

# game states
MENU = 0
INSTRUCTIONS = 1
GAME_RUNNING = 2
LEADERBOARD = 3


def calculate_points(shapes: int) -> int:
    '''takes cleared shapes and calculates the point value
    Args:
        shapes = amount of shapes cleared
    Returns:
        point score
    '''
    if shapes == 1:
        return 10

    return 10 + calculate_points(shapes - 1)


class Slide:
    '''creates slides
    Attributes:
        slide_name(str) = name of the slide
    '''

    def __init__(self, slide_name: str):
        '''creates a sldie object
        Args:
            slide_name: name of slide
        '''
        self._slide_name = slide_name

    def get_slide_name(self):
        '''gets the name of the slide
        Returns:
            Name of the slide
        '''
        return self._slide_name

    def set_slide_name(self, value: List[str]):
        '''sets a new name for the slide
        '''
        self._slide_name = value

    @classmethod
    def create_title(cls, title: str):
        '''creates a title for a slide
        Args:
            title: desired text for the title
        Returns:
            Title on a slide
        '''

        return arcade.draw_text(title, settings.WIDTH / 2, 540, arcade.color.BLACK, 30, font_name='GARA',
                                anchor_x="center")


class Leaderboard(Slide):
    '''creates a leaderboard
    Attributes:
        high_scores(list): list of pre-loaded high scores
    '''

    def __init__(self):
        '''create a leaderboard object
        Args:
            high_scores: a list of pre-set high scores
        '''
        self._high_scores = [["Lauren", 600], ["Stevo", 550], ["Charlotte", 500], ["Vince", 450],
                             ["You", int(total_points)]]

    def get_high_scores(self):
        '''gets the list of highscores
        Returns:
            List of highscores
        '''
        return self._high_scores

    def set_high_scores(self, value: List):
        '''sets a new list of highscores
        '''
        self._high_scores = value

    def sort_scores(self):
        '''bubble sorts the list of highscores by score value
        '''
        is_sorted = False
        times_through = 0

        while not is_sorted:
            is_sorted = True
            for i in range(len(self._high_scores) - 1 - times_through):
                a = self._high_scores[i][1]
                b = self._high_scores[i + 1][1]
                c = self._high_scores[i]
                d = self._high_scores[i + 1]
                if a < b:
                    self._high_scores[i] = d
                    self._high_scores[i + 1] = c
                    is_sorted = False
            times_through += 1

    @classmethod
    def create_divider(cls, y_coord: int):
        '''creates a horizontal divider for the leaderboard
        Args:
            y_coord: y location of the horizontal line
        Returns:
            Divider on leaderboard
        '''
        return arcade.draw_line(0, y_coord, settings.WIDTH, y_coord, arcade.color.BLACK)


class SarahGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.current_state = MENU

    def draw_menu(self):
        arcade.draw_rectangle_filled(x, 400, 50, 50, arcade.color.BANANA_YELLOW)
        arcade.draw_circle_filled(x + 134, 100, 25, arcade.color.BABY_BLUE)
        arcade.draw_rectangle_filled(x + 297, 125, 50, 50, arcade.color.FOREST_GREEN)
        arcade.draw_circle_filled(x - 469, 200, 25, arcade.color.BABY_BLUE)
        arcade.draw_circle_filled(x - 165, 135, 25, arcade.color.RED)
        arcade.draw_rectangle_filled(x - 333, 150, 50, 50, arcade.color.FOREST_GREEN)
        arcade.draw_rectangle_filled(x, 570, 50, 50, arcade.color.BANANA_YELLOW)
        arcade.draw_circle_filled(x + 150, 526, 25, arcade.color.BABY_BLUE)
        arcade.draw_rectangle_filled(x + 300, 560, 50, 50, arcade.color.FOREST_GREEN)
        arcade.draw_circle_filled(x - 450, 530, 25, arcade.color.BABY_BLUE)
        arcade.draw_circle_filled(x - 150, 550, 25, arcade.color.RED)
        arcade.draw_rectangle_filled(x - 300, 574, 50, 50, arcade.color.FOREST_GREEN)
        arcade.draw_rectangle_filled(x, 250, 50, 50, arcade.color.BANANA_YELLOW)
        arcade.draw_circle_filled(x + 210, 206, 25, arcade.color.BABY_BLUE)
        arcade.draw_rectangle_filled(x + 450, 310, 50, 50, arcade.color.FOREST_GREEN)
        arcade.draw_circle_filled(x - 360, 400, 25, arcade.color.BABY_BLUE)
        arcade.draw_circle_filled(x - 180, 270, 25, arcade.color.RED)
        arcade.draw_rectangle_filled(x - 340, 304, 50, 50, arcade.color.FOREST_GREEN)

        arcade.draw_text(SCREEN_TITLE, settings.WIDTH / 2, 400, arcade.color.BLACK, 60, font_name='GARA',
                         anchor_x="center")

        output = "Press Space to Continue"
        arcade.draw_text(output, settings.WIDTH / 2, 250, arcade.color.BLACK, 24, font_name='GARA', anchor_x="center")

    def draw_instructions(self):
        Slide.create_title("MATCH OFF INSTRUCTIONS")

        output = "The objective of the game is to match the colours in sets of 3, each matched shape is worth 10 points."
        arcade.draw_text(output, settings.WIDTH / 2, 500, arcade.color.BLACK, 14, font_name='GARA', anchor_x="center")

        output = "There are 60 seconds to attempt to attain the highest score."
        arcade.draw_text(output, settings.WIDTH / 2, 450, arcade.color.BLACK, 14, font_name='GARA', anchor_x="center")

        output = "Use the mouse to click on the desired colour."
        arcade.draw_text(output, settings.WIDTH / 2, 400, arcade.color.BLACK, 14, font_name='GARA', anchor_x="center")

        output = " Clicking on a colour that does not match the previous colour will cancel the selection."
        arcade.draw_text(output, settings.WIDTH / 2, 350, arcade.color.BLACK, 14, font_name='GARA', anchor_x="center")

        output = "A high score could snag a spot on the leaderboard!"
        arcade.draw_text(output, settings.WIDTH / 2, 300, arcade.color.BLACK, 14, font_name='GARA', anchor_x="center")

        output = "If you would like to leave the game at any time, press enter."
        arcade.draw_text(output, settings.WIDTH / 2, 250, arcade.color.BLACK, 14, font_name='GARA', anchor_x="center")

        output = "Press Space to Start the Game!"
        arcade.draw_text(output, settings.WIDTH / 2, 50, arcade.color.BLACK, 18, font_name='GARA', anchor_x="center")

        arcade.draw_rectangle_filled(x, 200, 50, 50, arcade.color.BANANA_YELLOW)
        arcade.draw_circle_filled(x + 150, 100, 25, arcade.color.BABY_BLUE)
        arcade.draw_rectangle_filled(x + 300, 125, 50, 50, arcade.color.FOREST_GREEN)
        arcade.draw_circle_filled(x - 450, 175, 25, arcade.color.BABY_BLUE)
        arcade.draw_circle_filled(x - 150, 135, 25, arcade.color.RED)
        arcade.draw_rectangle_filled(x - 300, 150, 50, 50, arcade.color.FOREST_GREEN)

    def draw_game(self):
        global x

        for i in self.gsqsprites:
            i.draw()

        for i in self.ysqsprites:
            i.draw()

        for i in self.rcirsprites:
            i.draw()

        for i in self.bcirsprites:
            i.draw()

        time = f"Time: {str(int((round(self.timer))))}"
        arcade.draw_text(time, settings.WIDTH / 2, settings.HEIGHT / 8,
                         arcade.color.BLACK, font_size=18, font_name='GARA', anchor_x="center")

        arcade.draw_text(total_points, settings.WIDTH / 2, settings.HEIGHT / 16,
                         arcade.color.BLACK, font_size=30, font_name='GARA', anchor_x="center")

    def draw_leaderboard(self):
        # leaderboard slide
        arcade.draw_rectangle_filled(x, 570, 50, 50, arcade.color.BANANA_YELLOW)
        arcade.draw_circle_filled(x + 150, 526, 25, arcade.color.BABY_BLUE)
        arcade.draw_rectangle_filled(x + 300, 560, 50, 50, arcade.color.FOREST_GREEN)
        arcade.draw_circle_filled(x - 450, 530, 25, arcade.color.BABY_BLUE)
        arcade.draw_circle_filled(x - 150, 550, 25, arcade.color.RED)
        arcade.draw_rectangle_filled(x - 300, 574, 50, 50, arcade.color.FOREST_GREEN)

        Leaderboard.create_divider(settings.HEIGHT / 6)
        Leaderboard.create_divider((settings.HEIGHT / 6) * 2)
        Leaderboard.create_divider((settings.HEIGHT / 6) * 3)
        Leaderboard.create_divider((settings.HEIGHT / 6) * 4)
        Leaderboard.create_divider((settings.HEIGHT / 6) * 5)

        rankings = Leaderboard()
        rankings.sort_scores()

        arcade.draw_text(f"1. {rankings._high_scores[0][0]}---------------{rankings._high_scores[0][1]}",
                         settings.WIDTH / 10, (settings.HEIGHT / 6) * 5 - 50, arcade.color.BLACK,
                         font_size=24, font_name='GARA')
        arcade.draw_text(f"2. {rankings._high_scores[1][0]}---------------{rankings._high_scores[1][1]}",
                         settings.WIDTH / 10, (settings.HEIGHT / 6) * 4 - 50, arcade.color.BLACK,
                         font_size=24, font_name='GARA')
        arcade.draw_text(f"3. {rankings._high_scores[2][0]}---------------{rankings._high_scores[2][1]}",
                         settings.WIDTH / 10, (settings.HEIGHT / 6) * 3 - 50, arcade.color.BLACK,
                         font_size=24, font_name='GARA')
        arcade.draw_text(f"4. {rankings._high_scores[3][0]}---------------{rankings._high_scores[3][1]}",
                         settings.WIDTH / 10, (settings.HEIGHT / 6) * 2 - 50, arcade.color.BLACK,
                         font_size=24, font_name='GARA')
        arcade.draw_text("Press Enter to continue", settings.WIDTH / 2, 30, arcade.color.BLACK, font_size=30,
                         anchor_x="center", font_name='GARA')

        Leaderboard.create_title("LEADERBOARD")

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        global x
        x = 0

        self.counter = 35
        self.prevselection = -1
        self.timer = 60

        self.gsqsprites = []
        self.ysqsprites = []
        self.rcirsprites = []
        self.bcirsprites = []

        self.gsqselected = []
        self.ysqselected = []
        self.rcirselected = []
        self.bcirselected = []

        # randomly draws all sprites
        for i in range(self.counter):
            speedgsq = random.uniform(0.01, 1)
            speedysq = random.uniform(-1, -0.01)
            speedrcir = random.uniform(-1, -0.01)
            speedbcir = random.uniform(0.01, 1)
            gsq_posy = random.randrange(0, SCREEN_HEIGHT)
            ysq_posy = random.randrange(0, SCREEN_HEIGHT)
            rcir_posy = random.randrange(0, SCREEN_HEIGHT)
            bcir_posy = random.randrange(0, SCREEN_HEIGHT)
            gsq_posx = random.randrange(-1750, SCREEN_WIDTH)
            ysq_posx = random.randrange(SCREEN_WIDTH, 1750)
            rcir_posx = random.randrange(SCREEN_WIDTH, 1750)
            bcir_posx = random.randrange(-1750, SCREEN_WIDTH)

            # define greensquare
            self.gsq = arcade.Sprite(center_x=gsq_posx, center_y=gsq_posy)
            self.gsq.texture = arcade.make_soft_square_texture(50, arcade.color.FOREST_GREEN, outer_alpha=200)
            self.gsq.change_x = speedgsq

            self.gsqsprites.append(self.gsq)
            self.gsqselected.append(False)  # False means not selected

            # define yellowsquare
            self.ysq = arcade.Sprite(center_x=ysq_posx, center_y=ysq_posy)
            self.ysq.texture = arcade.make_soft_square_texture(50, arcade.color.BANANA_YELLOW, outer_alpha=200)
            self.ysq.change_x = speedysq

            self.ysqsprites.append(self.ysq)
            self.ysqselected.append(False)  # False means not selected

            # define redcircle
            self.rcir = arcade.Sprite(center_x=rcir_posx, center_y=rcir_posy)
            self.rcir.texture = arcade.make_soft_circle_texture(50, arcade.color.RED, outer_alpha=200)
            self.rcir.change_x = speedrcir

            self.rcirsprites.append(self.rcir)
            self.rcirselected.append(False)  # False means not selected

            # define bluecircle
            self.bcir = arcade.Sprite(center_x=bcir_posx, center_y=bcir_posy)
            self.bcir.texture = arcade.make_soft_circle_texture(50, arcade.color.BABY_BLUE, outer_alpha=200)
            self.bcir.change_x = speedbcir

            self.bcirsprites.append(self.bcir)
            self.bcirselected.append(False)  # False means not selected

    def on_draw(self):
        arcade.start_render()

        if self.current_state == MENU:
            self.draw_menu()
        elif self.current_state == INSTRUCTIONS:
            self.draw_instructions()
            self.timer = 60
        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        else:
            self.draw_leaderboard()

    def on_key_press(self, key, modifiers):
        # changes slides
        if key == arcade.key.SPACE:
            if self.current_state == MENU:
                self.current_state = INSTRUCTIONS
            elif self.current_state == INSTRUCTIONS:
                self.current_state = GAME_RUNNING

        # skips the entire game
        if key == arcade.key.ENTER:
            self.director.next_view()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        global total_points

        self.select = [self.gsqselected, self.ysqselected, self.rcirselected, self.bcirselected]
        self.sprite = [self.gsqsprites, self.ysqsprites, self.rcirsprites, self.bcirsprites]
        self.color = [arcade.make_soft_square_texture(50, arcade.color.FOREST_GREEN, outer_alpha=200),
                      arcade.make_soft_square_texture(50, arcade.color.BANANA_YELLOW, outer_alpha=200),
                      arcade.make_soft_circle_texture(50, arcade.color.RED, outer_alpha=200),
                      arcade.make_soft_circle_texture(50, arcade.color.BABY_BLUE, outer_alpha=200)]

        self.gsqrid = []
        self.ysqrid = []
        self.rcirrid = []
        self.bcirrid = []

        self.gsqclicked = 0
        self.ysqclicked = 0
        self.rcirclicked = 0
        self.bcirclicked = 0

        # invalid selection
        for i in range(len(self.gsqsprites)):
            if self.gsqsprites[i].collides_with_point((x, y)) and self.prevselection != 0:

                for j in range(len(self.select[self.prevselection])):
                    self.select[self.prevselection][j] = False
                    self.sprite[self.prevselection][j].texture = self.color[self.prevselection]

                self.prevselection = 0

        for i in range(len(self.ysqsprites)):
            if self.ysqsprites[i].collides_with_point((x, y)) and self.prevselection != 1:

                for j in range(len(self.select[self.prevselection])):
                    self.select[self.prevselection][j] = False
                    self.sprite[self.prevselection][j].texture = self.color[self.prevselection]

                self.prevselection = 1

        for i in range(len(self.rcirsprites)):
            if self.rcirsprites[i].collides_with_point((x, y)) and self.prevselection != 2:

                for j in range(len(self.select[self.prevselection])):
                    self.select[self.prevselection][j] = False
                    self.sprite[self.prevselection][j].texture = self.color[self.prevselection]

                self.prevselection = 2

        for i in range(len(self.bcirsprites)):
            if self.bcirsprites[i].collides_with_point((x, y)) and self.prevselection != 3:

                for j in range(len(self.select[self.prevselection])):
                    self.select[self.prevselection][j] = False
                    self.sprite[self.prevselection][j].texture = self.color[self.prevselection]

                self.prevselection = 3

        for i in range(len(self.gsqsprites)):
            if self.gsqsprites[i].collides_with_point((x, y)):

                if not self.gsqselected[i]:  # character has not been clicked on before

                    self.gsqsprites[i].texture = arcade.make_soft_square_texture(50, arcade.color.FOREST_GREEN)

                elif self.gsqselected[i]:  # character texture is returned to before being tampered with
                    self.gsqsprites[i].texture = arcade.make_soft_square_texture(50, arcade.color.FOREST_GREEN,
                                                                                 outer_alpha=200)

                self.gsqselected[i] = not (self.gsqselected[i])

        for i in range(len(self.ysqsprites)):
            if self.ysqsprites[i].collides_with_point((x, y)):

                if not self.ysqselected[i]:  # character has not been clicked on before
                    self.ysqsprites[i].texture = arcade.make_soft_square_texture(50, arcade.color.BANANA_YELLOW)

                elif self.ysqselected[i]:  # character texture is returned to before being tampered with
                    self.ysqsprites[i].texture = arcade.make_soft_square_texture(50, arcade.color.BANANA_YELLOW,
                                                                                 outer_alpha=200)

                self.ysqselected[i] = not (self.ysqselected[i])

        for i in range(len(self.rcirsprites)):
            if self.rcirsprites[i].collides_with_point((x, y)):

                if not self.rcirselected[i]:  # character has not been clicked on before
                    self.rcirsprites[i].texture = arcade.make_soft_circle_texture(50, arcade.color.RED)

                elif self.rcirselected[i]:  # character texture is returned to before being tampered with
                    self.rcirsprites[i].texture = arcade.make_soft_circle_texture(50, arcade.color.RED, outer_alpha=200)

                self.rcirselected[i] = not (self.rcirselected[i])

        for i in range(len(self.bcirsprites)):
            if self.bcirsprites[i].collides_with_point((x, y)):

                if not self.bcirselected[i]:  # character has not been clicked on before
                    self.bcirsprites[i].texture = arcade.make_soft_circle_texture(50, arcade.color.BABY_BLUE)

                elif self.bcirselected[i]:  # character texture is returned to before being tampered with
                    self.bcirsprites[i].texture = arcade.make_soft_circle_texture(50, arcade.color.BABY_BLUE,
                                                                                  outer_alpha=200)

                self.bcirselected[i] = not (self.bcirselected[i])

        # removes greensquare triplets
        for i in range(len(self.gsqselected)):
            if self.gsqselected[i]:
                self.gsqclicked += 1

        if self.gsqclicked >= 3:
            for i in range(len(self.gsqselected)):
                if self.gsqselected[i]:
                    self.gsqrid.append(i)
            total_points = str(int(total_points) + calculate_points(self.gsqclicked))

            # bubble sort to reverse list
            gsq_sorted = False
            while not gsq_sorted:
                gsq_sorted = True
                for i in range(len(self.gsqrid) - 1):
                    b = self.gsqrid[i]
                    a = self.gsqrid[i + 1]
                    if a > b:
                        self.gsqrid[i] = a
                        self.gsqrid[i + 1] = b
                        gsq_sorted = False

            for i in self.gsqrid:
                del self.gsqselected[i]
                del self.gsqsprites[i]

        # removes yellowsquare triplets
        for i in range(len(self.ysqselected)):
            if self.ysqselected[i]:
                self.ysqclicked += 1

        if self.ysqclicked >= 3:
            for i in range(len(self.ysqselected)):
                if self.ysqselected[i]:
                    self.ysqrid.append(i)
            total_points = str(int(total_points) + calculate_points(self.ysqclicked))

            # bubble sort to reverse list
            ysq_sorted = False
            while not ysq_sorted:
                ysq_sorted = True
                for i in range(len(self.ysqrid) - 1):
                    b = self.ysqrid[i]
                    a = self.ysqrid[i + 1]
                    if a > b:
                        self.ysqrid[i] = a
                        self.ysqrid[i + 1] = b
                        ysq_sorted = False

            for i in self.ysqrid:
                del self.ysqselected[i]
                del self.ysqsprites[i]

        # removes redcircle triplets
        for i in range(len(self.rcirselected)):
            if self.rcirselected[i]:
                self.rcirclicked += 1

        if self.rcirclicked >= 3:
            for i in range(len(self.rcirselected)):
                if self.rcirselected[i]:
                    self.rcirrid.append(i)
            total_points = str(int(total_points) + calculate_points(self.rcirclicked))

            # bubble sort to reverse list
            rcir_sorted = False
            while not rcir_sorted:
                rcir_sorted = True
                for i in range(len(self.rcirrid) - 1):
                    b = self.rcirrid[i]
                    a = self.rcirrid[i + 1]
                    if a > b:
                        self.rcirrid[i] = a
                        self.rcirrid[i + 1] = b
                        rcir_sorted = False

            for i in self.rcirrid:
                del self.rcirselected[i]
                del self.rcirsprites[i]

        # removes bluecircle triplets
        for i in range(len(self.bcirselected)):
            if self.bcirselected[i]:
                self.bcirclicked += 1

        if self.bcirclicked >= 3:
            for i in range(len(self.bcirselected)):
                if self.bcirselected[i]:
                    self.bcirrid.append(i)
            total_points = str(int(total_points) + calculate_points(self.bcirclicked))

            # bubble sort to reverse list
            bcir_sorted = False
            while not bcir_sorted:
                bcir_sorted = True
                for i in range(len(self.bcirrid) - 1):
                    b = self.bcirrid[i]
                    a = self.bcirrid[i + 1]
                    if a > b:
                        self.bcirrid[i] = a
                        self.bcirrid[i + 1] = b
                        bcir_sorted = False

            for i in self.bcirrid:
                del self.bcirselected[i]
                del self.bcirsprites[i]

    def update(self, delta_time: float):
        global x
        x += 1
        if x == 1450:
            x = -310

        self.timer -= delta_time

        self.gsq.update()
        self.ysq.update()
        self.rcir.update()
        self.bcir.update()

        for c in self.gsqsprites:
            c.update()

        for c in self.ysqsprites:
            c.update()

        for c in self.rcirsprites:
            c.update()

        for c in self.bcirsprites:
            c.update()

        if self.current_state == GAME_RUNNING and self.timer <= 0:
            self.current_state = LEADERBOARD


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
    my_view = SarahGameView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
