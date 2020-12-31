import pygame as pg
from constants import *
from math import floor

WINDOW_SIZE = (800, 600)
WINDOW_TITLE = "Tic-Tac-Toe"
GAME_FONT = "Comic Sans MS"
ANTI_ALIAS = True
INPUT_FIELD_SIZE = (500, 75)
INPUT_FIELD_BORDER_WIDTH = 3
INPUT_TEXT_INDENT_LEFT = 5
STATUS_FONT_SIZE = 60
SCORE_FONT_SIZE = 70
INPUT_FONT_SIZE = 90
CELL_SIZE = 100
FIELD_LINE_WIDTH = 5
FIELD_Y = 30
STATUS_WIDGET_DISTANCE_FROM_FIELD = 25
SCORE_WIDGET_DISTANCE_FROM_BOTTOM = 175
SCORE_DISTANCE_FROM_WORD_SCORE = 45
GAME_ROUND_DELAY = 1000
TICKRATE = 60
SCREAMER_DURATION = 20


class Player:
    """Player class.

    Contains type of cell (cross, zero) and name of the player.
    """
    def __init__(self, name, cell_type):
        self.name = name
        self.cell_type = cell_type
        self.win_count = 0


class GameWindow:
    """Class of game window.

    Responsible for displaying game field and other widgets in window.
    Contains game and name input loops and game manager.
    """
    def __init__(self, name1="Petr", name2="Vasyan"):
        pg.init()
        self._width = WINDOW_SIZE[0]
        self._height = WINDOW_SIZE[1]
        self._title = WINDOW_TITLE
        self.screen = pg.display.set_mode((self._width, self._height))
        pg.display.set_caption(self._title)

        player1 = Player(name1, CROSS)
        player2 = Player(name2, ZERO)
        self._game_manager = GameManager(player1, player2)
        field = self._game_manager.field
        self._field_widget = GameFieldView(self.screen, field)
        self._status_font = pg.font.SysFont(GAME_FONT, STATUS_FONT_SIZE)
        self._score_font = pg.font.SysFont(GAME_FONT, SCORE_FONT_SIZE)
        self._input_font = pg.font.SysFont(GAME_FONT, INPUT_FONT_SIZE)
        screamer_image = pg.image.load("resources/screamer.jpeg").convert()
        self._screamer_image = pg.transform.scale(screamer_image, WINDOW_SIZE)
        self._score = self._game_manager.get_score()
        self.clock = pg.time.Clock()

    def game_loop(self):
        finished = False
        while not finished:
            self.screen.fill(WHITE)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True
                elif event.type == pg.MOUSEBUTTONUP:
                    x, y = pg.mouse.get_pos()
                    click_area = self._get_click_area(x, y)
                    if click_area == "FIELD":
                        i, j = self._field_widget.get_cell_pos(x, y)
                        self._game_manager.handle_click(i, j)

            self._field_widget.draw()
            self._draw_score(self._score)

            if self._game_manager.check_game_ended():
                self._score = self._game_manager.get_score()
                self._draw_game_status(self._game_manager.game_status)
                pg.display.flip()
                pg.time.wait(GAME_ROUND_DELAY)
                self._game_manager.change_sides()
                self._game_manager.new_field()
            else:
                self._draw_game_status(self._game_manager.game_status)

            # THIS IS AN EASTER EGG
            #
            # if finished:
            #     self.screen.blit(self._screamer_image, (0, 0))
            #     pg.display.flip()
            #     pg.time.wait(SCREAMER_DURATION)

            pg.display.flip()
            self.clock.tick(TICKRATE)

    def _get_click_area(self, x, y):
        x1 = self._field_widget.x
        y1 = FIELD_Y
        x2 = x1 + self._field_widget.width
        y2 = y1 + self._field_widget.height
        if self._is_in_rect(x, y, x1, y1, x2, y2):
            return "FIELD"

    def _is_in_rect(self, x, y, x1, y1, x2, y2):
        return x >= x1 and y >= y1 and x <= x2 and y <= y2

    def _draw_game_status(self, status):
        status_surface = self._status_font.render(status, ANTI_ALIAS, BLACK)
        status_width  = status_surface.get_width()
        x = (self._width - status_width) // 2
        y = (self._field_widget.height +
                                STATUS_WIDGET_DISTANCE_FROM_FIELD + FIELD_Y)
        self.screen.blit(status_surface, (x, y))

    def _draw_score(self, score):
        word_surface = self._score_font.render("SCORE", ANTI_ALIAS, BLACK)
        word_width = word_surface.get_width()
        word_x = (self._width - word_width) // 2
        word_y = self._height - SCORE_WIDGET_DISTANCE_FROM_BOTTOM
        self.screen.blit(word_surface, (word_x, word_y))

        values = list(self._score.values())
        score_string = f"{values[0]} : {values[1]}"
        score_surface = self._score_font.render(score_string,
                                                ANTI_ALIAS, BLACK)
        score_width = score_surface.get_width()
        score_x = (self._width - score_width) // 2
        score_y = word_y + SCORE_DISTANCE_FROM_WORD_SCORE
        self.screen.blit(score_surface, (score_x, score_y))

    def name_input_loop(self):
        input_rect_length = INPUT_FIELD_SIZE[0]
        input_rect_height = INPUT_FIELD_SIZE[1]
        input_rect_x = (self._width - input_rect_length) // 2
        input_rect_y = (self._height - input_rect_height) // 2
        input_text_surface = self._input_font.render("Test Text",
                                                     ANTI_ALIAS, BLACK)
        input_text_x = input_rect_x + INPUT_TEXT_INDENT_LEFT
        input_text_y = (input_rect_y + input_rect_height - input_text_surface.get_height())

        finished = False
        while not finished:
            self.screen.fill(WHITE)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True

            pg.draw.rect(self.screen, BLACK,
                        (input_rect_x, input_rect_y,
                        input_rect_length, input_rect_height),
                        INPUT_FIELD_BORDER_WIDTH)
            self.screen.blit(input_text_surface, (input_text_x, input_text_y))

            pg.display.flip()
            self.clock.tick(TICKRATE)


class GameManager:
    """Class of game manager.

    Responsible for correct gameflow.
    Contains field.
    """
    def __init__(self, player1, player2):
        self._players = [player1, player2]
        self._curplayer = self._get_index_of_type(CROSS)
        self.field = GameField(3, 3)
        self.game_status = f"{self._players[self._curplayer].name}'s turn"

    def handle_click(self, x, y):
        if self.field.cells[y][x] == 0:
            self.field.cells[y][x] = self._players[self._curplayer].cell_type
            self._curplayer = 1 - self._curplayer
            self.game_status = f"{self._players[self._curplayer].name}'s turn"

            self.field.filled_cells += 1

    def check_game_ended(self):
        winning_cell = self._check_win()
        if winning_cell:
            winner = self._players[self._get_index_of_type(winning_cell)]
            name = winner.name
            winner.win_count += 1
            self.game_status = f"Player {name} won!"
            return True

        if self.field.filled_cells == self.field.width * self.field.height:
            self.game_status = "It's a draw!"
            return True

        return False

    def _check_win(self):
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

        if cells[2][0] != VOID:
            if cells[2][0] == cells[1][1] and cells[1][1] == cells[0][2]:
                return cells[2][0]

        return VOID

    def _get_index_of_type(self, sought_type):
        for ind, player in enumerate(self._players):
            if player.cell_type == sought_type:
                return ind

    def new_field(self):
        self.field.cells = [[VOID]*self.field.width
                            for i in range(self.field.height)]
        self.field.filled_cells = 0
        self.game_status = f"{self._players[self._curplayer].name}'s turn"

    def change_sides(self):
        player1, player2 = self._players
        player1.cell_type,player2.cell_type=player2.cell_type,player1.cell_type
        self._curplayer = self._get_index_of_type(CROSS)

    def get_score(self):
        player1, player2 = self._players
        return {player1.name: player1.win_count,
                player2.name: player2.win_count}


class GameField:
    """Class of game field.

    Contains information about cells on the field.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[VOID]*self.width for i in range(self.height)]
        self.filled_cells = 0


class GameFieldView:
    """Game field widget.

    Reflects field on window.
    Initially handles click on field and sends it to game manager
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
    names = window.name_input_loop()
    if names:
        player_name1, player_name2 = names
        window.game_loop(player_name1, player_name2)
    else:
        window.game_loop()
    pg.quit()


if __name__ == '__main__':
    main()
