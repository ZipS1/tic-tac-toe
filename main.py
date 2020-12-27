import pygame as pg
from enum import Enum
from colors import *

WINDOW_SIZE = (800, 600)
WINDOW_TITLE = "Tic-Tac-Toe"
GAME_FIELD_SIZE = (3, 3)
CELL_SIZE = 100
FIELD_LINE_WIDTH = 5
TICKRATE = 60


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
        self.screen = pg.display.set_mode((self._width, self._height))
        pg.display.set_caption(self._title)

        player1 = Player("Petr", Cell.CROSS)
        player2 = Player("Vasyan", Cell.ZERO)
        self._game_manager = GameManager(player1, player2)
        field = self._game_manager.field
        self._field_widget = GameFieldView(self.screen, field)

    def main_loop(self):
        finished = False
        clock = pg.time.Clock()
        while not finished:
            self.screen.fill(WHITE)
            self._field_widget.draw()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True
                elif event.type == pg.MOUSEBUTTONUP:
                    x, y = pg.mouse.get_pos()
                    click_area = self.get_click_area(x, y)

                    if click_area == "FIELD":
                        i, j = self._field_widget.get_cell_pos(x, y)
                        self._game_manager.handle_click(i, j)

            pg.display.flip()
            clock.tick(TICKRATE)

    def get_click_area(self, x, y):
        return "FIELD"


class GameManager:
    """Game manager, running proccesses."""
    def __init__(self, player1, player2):
        self._players = [player1, player2]
        self._current_player = 0
        self.field = GameField(*GAME_FIELD_SIZE)

    def handle_click(self, i, j):
        print("click handled")
        print(i, j)


class GameField:
    """Class of game field.

    Contains information about cells on the field.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell.VOID]*self.width for i in range(self.height)]


class GameFieldView: # field coords 400, 50
    """Game field widget.

    Reflects field on window, initially handles click on field.
    """
    def __init__(self, screen, field):
        self.field = field
        self.width = (self.field.width*CELL_SIZE
                            + FIELD_LINE_WIDTH*(field.width - 1))
        self.height = (self.field.height*CELL_SIZE
                            + FIELD_LINE_WIDTH*(field.height - 1))
        self.screen = screen
        self.cross_image = pg.image.load("resources/cross.png").convert_alpha()
        self.zero_image = pg.image.load("resources/zero.png").convert_alpha()

    def get_cell_pos(self, x, y):
        """Returns coords of cell in field."""
        return 0, 0

    def draw(self):
        """Draw game field on game window."""
        print("Draw game field...")
        print("Width", self.width)
        print("Height", self.height)



def main():
    window = GameWindow()
    window.main_loop()
    pg.quit()


if __name__ == '__main__':
    main()
