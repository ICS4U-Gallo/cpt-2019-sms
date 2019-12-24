class View:
    """
    TODO:Thoughts:
    - is there a need for a close()/on_close() method?
    """
    def __init__(self):
        self.window = None
        self.button_list: List[gui.TextButton] = []
        self.dialogue_box_list: List[gui.DialogueBox] = []
        self.text_list: List[gui.Text] = []
        self.textbox_time = 0.0
        self.textbox_list: List[gui.TextBox] = []
        self.key = None

    def update(self, delta_time: float):
        """To be overridden"""
        try:
            self.textbox_time += delta_time
            seconds = self.textbox_time % 60
            if seconds >= 0.115:
                if self.textbox_list:
                    for textbox in self.textbox_list:
                        textbox.update(delta_time, self.key)
                    self.textbox_time = 0.0
        except AttributeError:
            pass


    def on_update(self, delta_time: float):
        """To be overridden"""
        pass


    def on_draw(self):
        """Called when this view should draw"""
        try:
            if self.button_list:
                for button in self.button_list:
                    button.draw()
        except AttributeError:
            pass
        try:
            if self.text_list:
                for text in self.text_list:
                    text.draw()
        except AttributeError:
            pass
        pass
        try:
            if self.dialogue_box_list:
                for dialogue_box in self.dialogue_box_list:
                    if dialogue_box.active:
                        dialogue_box.on_draw()
        except AttributeError:
            pass
        try:
            if self.textbox_list:
                for textbox in self.textbox_list:
                    textbox.draw()
        except AttributeError:
            pass


    def on_show(self):
        """Called when this view is shown"""
        pass


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        Override this function to add mouse functionality.

        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        """
        pass


    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Override this function to add mouse button functionality.

        :param float x: x position of the mouse
        :param float y: y position of the mouse
        :param int button: What button was hit. One of:
                           arcade.MOUSE_BUTTON_LEFT, arcade.MOUSE_BUTTON_RIGHT,
                           arcade.MOUSE_BUTTON_MIDDLE
        :param int modifiers: Shift/click, ctrl/click, etc.
        """
        try:
            if self.button_list:
                for button_widget in self.button_list:
                    button_widget.check_mouse_press(x, y)
        except AttributeError:
            pass
        try:
            if self.dialogue_box_list:
                for dialogue_box in self.dialogue_box_list:
                    if dialogue_box.active:
                        dialogue_box.on_mouse_press(x, y, button, modifiers)
        except AttributeError:
            pass

        try:
            if self.textbox_list:
                for textbox in self.textbox_list:
                    textbox.check_mouse_press(x, y)
        except AttributeError:
            pass


    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, _buttons: int, _modifiers: int):
        """
        Override this function to add mouse button functionality.

        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        :param int _buttons: Which button is pressed
        :param int _modifiers: Ctrl, shift, etc.
        """
        self.on_mouse_motion(x, y, dx, dy)


    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """
        Override this function to add mouse button functionality.

        :param float x:
        :param float y:
        :param int button:
        :param int modifiers:
        """
        try:
            if self.button_list:
                for button_widget in self.button_list:
                    button_widget.check_mouse_release(x, y)
        except AttributeError:
            pass
        try:
            if self.dialogue_box_list:
                for dialogue_box in self.dialogue_box_list:
                    if dialogue_box.active:
                        dialogue_box.on_mouse_release(x, y, button, modifiers)
        except AttributeError:
            pass
        try:
            if self.textbox_list:
                for textbox in self.textbox_list:
                    textbox.check_mouse_release(x, y)
        except AttributeError:
            pass


    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """
        User moves the scroll wheel.

        :param int x:
        :param int y:
        :param int scroll_x:
        :param int scroll_y:
        """
        pass


    def on_key_press(self, symbol: int, modifiers: int):
        """
        Override this function to add key press functionality.

        :param int symbol: Key that was hit
        :param int modifiers: If it was shift/ctrl/alt
        """
        try:
            self.key = symbol
        except AttributeError:
            pass


    def on_key_release(self, _symbol: int, _modifiers: int):
        """
        Override this function to add key release functionality.

        :param int _symbol: Key that was hit
        :param int _modifiers: If it was shift/ctrl/alt
        """
        try:
            self.key = None
        except AttributeError:
            pass
