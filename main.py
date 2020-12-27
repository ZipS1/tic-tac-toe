import pygame as pg
from enum import Enum

WINDOW_SIZE = (800, 600)
WINDOW_TITLE = "Tic-Tac-Toe"
GAME_FIELD_SIZE = (3, 3)
CELL_SIZE = 50


class Cell(Enum):
    VOID = 0
    CROSS = 1
    ZERO = 2


class Player:
    """Player class.

    Contains type of cell (cross, zero) and name of the player.
    """
    def __init__(self, name, cell_type):
        self.name = name
        self.cell_type = cell_type


class GameWindow:
    """Class of game window.

    Responsible for displaying game field and other buttons in window.
    Contains mainloop of the game and game manager.
    """
    def __init__(self):
        pg.init()
        self._width = WINDOW_SIZE[0]
        self._height = WINDOW_SIZE[1]
        self._title = WINDOW_TITLE
        self._screen = pg.display.set_mode((self._width, self._height))
        pg.display.set_caption(self._title)
        clock = pg.time.Clock()

        self._field_widget = GameFieldView()
        player1 = Player("Petr", Cell.CROSS)
        player2 = Player("Vasyan", Cell.ZERO)
        self._game_manager = GameManager(self.player1, self.player2)

    def main_loop(self):
        finished = False

        while not finished:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True
                elif event.type == pg.MOUSEBUTTONUP():
                    x, y = pg.mouse.get_pos()
                    click_area = self.get_click_area(x, y)

                    if click_area == "FIELD":
                        i, j = self._field_widget.get_cell_pos(x, y)
                        self._game_manager.handle_click(i, j)

    def get_click_area(self, x, y):
        pass


class GameManager:
    """Game manager, running proccesses."""
    def __init__(self, player1, player2):
        self._players = [player1, player2]
        self._current_player = 0
        game_field_width, game_field_height = GAME_FIELD_SIZE
        self._field = GameField(game_field_width, game_field_height)

    def handle_click(self, i, j):
        pass


class GameField:
    """Class of game field.

    Contains information about cells on the field.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height


class GameFieldView:
    """Game field widget.

    Reflects field on window, initially handles click on field.
    """
    def __init__(self, field):
        self.field = field
        self.width = self.field.width * CELL_SIZE
        self.height = self.field.height * CELL_SIZE
        # load cell pictures
        pass

    def get_cell_pos(self, x, y):
        """Returns coords of cell in field."""
        pass

    def draw(self):
        """Draw game field on game window."""
        pass
