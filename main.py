import pygame as pg
from enum import Enum
from colors import *
from math import floor

WINDOW_SIZE = (800, 600)
WINDOW_TITLE = "Tic-Tac-Toe"
CELL_SIZE = 100
FIELD_LINE_WIDTH = 5
FIELD_Y = 50
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
            self._field_widget.draw(FIELD_Y)

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
        self.field = GameField(3, 3)

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


class GameFieldView:
    """Game field widget.

    Reflects field on window, initially handles click on field.
    """
    def __init__(self, screen, field):
        self.field = field
        self.width = (self.field.width*CELL_SIZE +
                            FIELD_LINE_WIDTH*(field.width - 1))
        self.height = (self.field.height*CELL_SIZE +
                            FIELD_LINE_WIDTH*(field.height - 1))
        self.screen = screen
        cross_image = pg.image.load("resources/cross.png").convert_alpha()
        zero_image = pg.image.load("resources/zero.png").convert_alpha()
        cell_res = (CELL_SIZE, CELL_SIZE)
        self.cross_image = pg.transform.scale(cross_image, cell_res)
        self.zero_image = pg.transform.scale(zero_image, cell_res)

    def get_cell_pos(self, x, y):
        """Returns coords of cell in field."""
        return 0, 0

    def draw(self, y):
        """Draw game field on game window."""
        window_width = WINDOW_SIZE[0]
        x = (window_width - self.width) // 2
        pg.draw.line(self.screen, BLACK,
            (x + CELL_SIZE + FIELD_LINE_WIDTH//2, y),
            (x + CELL_SIZE + FIELD_LINE_WIDTH//2, y + self.height),
            FIELD_LINE_WIDTH)
        pg.draw.line(self.screen, BLACK,
            (x + 2*CELL_SIZE + floor(FIELD_LINE_WIDTH*1.5), y),
            (x + 2*CELL_SIZE + floor(FIELD_LINE_WIDTH*1.5), y + self.height),
            FIELD_LINE_WIDTH)
        pg.draw.line(self.screen, BLACK,
            (x, y + CELL_SIZE + FIELD_LINE_WIDTH//2),
            (x + self.width, y + CELL_SIZE + FIELD_LINE_WIDTH//2),
            FIELD_LINE_WIDTH)
        pg.draw.line(self.screen, BLACK,
            (x, y + 2*CELL_SIZE + floor(FIELD_LINE_WIDTH*1.5)),
            (x + self.width, y + 2*CELL_SIZE + floor(FIELD_LINE_WIDTH*1.5)),
            FIELD_LINE_WIDTH)


def main():
    window = GameWindow()
    window.main_loop()
    pg.quit()


if __name__ == '__main__':
    main()
