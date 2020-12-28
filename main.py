import pygame as pg
from constants import *
from math import floor

WINDOW_SIZE = (800, 600)
WINDOW_TITLE = "Tic-Tac-Toe"
CELL_SIZE = 100
FIELD_LINE_WIDTH = 5
FIELD_Y = 50
TICKRATE = 60


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

        player1 = Player("Petr", CROSS)
        player2 = Player("Vasyan", ZERO)
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

                        if self._game_manager.check_win():
                            win_type = self._game_manager.check_win()
                            name = self._game_manager.get_player_name(win_type)
                            print("Player", name,"won!")

            pg.display.flip()
            clock.tick(TICKRATE)

    def get_click_area(self, x, y):
        x1 = self._field_widget.x
        y1 = FIELD_Y
        x2 = x1 + self._field_widget.width
        y2 = y1 + self._field_widget.height
        if self.is_in_rect(x, y, x1, y1, x2, y2):
            return "FIELD"

    def is_in_rect(self, x, y, x1, y1, x2, y2):
        return x >= x1 and y >= y1 and x <= x2 and y <= y2


class GameManager:
    """Game manager, running proccesses."""
    def __init__(self, player1, player2):
        self._players = [player1, player2]
        self._curplayer = 0
        self.field = GameField(3, 3)

    def handle_click(self, x, y):
        if self.field.cells[y][x] == 0:
            self.field.cells[y][x] = self._players[self._curplayer].cell_type
            self._curplayer = 1 - self._curplayer

    def check_win(self):
        cells = self.field.cells

        for y in range(self.field.height):
            if cells[y][0] != VOID:
                if cells[y][0] == cells[y][1] and cells[y][1] == cells[y][2]:
                    return cells[y][0]

        for x in range(self.field.width):
            if cells[0][x] != VOID:
                if cells[0][x] == cells[1][x] and cells[1][x] == cells[2][x]:
                    return cells[0][x]

        if cells[0][0] != VOID:
            if cells[0][0] == cells[1][1] and cells[1][1] == cells[2][2]:
                return cells[0][0]

        if cells[0][0] != VOID:
            if cells[2][0] == cells[1][1] and cells[1][1] == cells[0][2]:
                return cells[2][0]

        return VOID

    def get_player_name(self, sought_type):
        for player in self._players:
            if player.cell_type == sought_type:
                return player.name


class GameField:
    """Class of game field.

    Contains information about cells on the field.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[VOID]*self.width for i in range(self.height)]


class GameFieldView:
    """Game field widget.

    Reflects field on window, initially handles click on field.
    """
    def __init__(self, screen, field):
        self.field = field
        self.width = (self.field.width*CELL_SIZE +
                            FIELD_LINE_WIDTH*(self.field.width - 1))
        self.height = (self.field.height*CELL_SIZE +
                            FIELD_LINE_WIDTH*(self.field.height - 1))
        self.screen = screen
        cross_image = pg.image.load("resources/cross.png").convert_alpha()
        zero_image = pg.image.load("resources/zero.png").convert_alpha()
        cell_res = (CELL_SIZE, CELL_SIZE)
        self._cross_image = pg.transform.scale(cross_image, cell_res)
        self._zero_image = pg.transform.scale(zero_image, cell_res)
        window_width = WINDOW_SIZE[0]
        self.x = (window_width - self.width) // 2
        self.y = FIELD_Y

    def get_cell_pos(self, x, y):
        """Returns coords of cell in field."""
        return ((x - self.x)*self.field.width//self.width,
                (y - self.y)*self.field.height//self.height)

    def draw(self):
        """Draw game field on game window."""
        pg.draw.line(self.screen, BLACK,
            (self.x + CELL_SIZE + FIELD_LINE_WIDTH//2, self.y),
            (self.x + CELL_SIZE + FIELD_LINE_WIDTH//2, self.y + self.height),
            FIELD_LINE_WIDTH)
        pg.draw.line(self.screen, BLACK,
            (self.x + 2*CELL_SIZE + floor(FIELD_LINE_WIDTH*1.5), self.y),
            (self.x + 2*CELL_SIZE + floor(FIELD_LINE_WIDTH*1.5),
             self.y + self.height),
            FIELD_LINE_WIDTH)
        pg.draw.line(self.screen, BLACK,
            (self.x, self.y + CELL_SIZE + FIELD_LINE_WIDTH//2),
            (self.x + self.width, self.y + CELL_SIZE + FIELD_LINE_WIDTH//2),
            FIELD_LINE_WIDTH)
        pg.draw.line(self.screen, BLACK,
            (self.x, self.y + 2*CELL_SIZE + floor(FIELD_LINE_WIDTH*1.5)),
            (self.x + self.width,
             self.y + 2*CELL_SIZE + floor(FIELD_LINE_WIDTH*1.5)),
            FIELD_LINE_WIDTH)

        for y in range(self.field.height):
            for x in range(self.field.width):
                if self.field.cells[y][x] == 1:
                    x_coord, y_coord = self._get_image_coords(x, y)
                    self.screen.blit(self._zero_image, (x_coord, y_coord))
                elif self.field.cells[y][x] == 2:
                    x_coord, y_coord = self._get_image_coords(x, y)
                    self.screen.blit(self._cross_image, (x_coord, y_coord))

    def _get_image_coords(self, i, j):
        x = self.x + i*(CELL_SIZE + FIELD_LINE_WIDTH)
        y = self.y + j*(CELL_SIZE + FIELD_LINE_WIDTH)
        return x, y


def main():
    window = GameWindow()
    window.main_loop()
    pg.quit()


if __name__ == '__main__':
    main()
