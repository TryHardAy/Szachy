from optparse import make_option
import pygame


class Field:
    def __init__(self, pos: tuple, size: tuple, id: int, window: pygame.display):
        self._xpos = pos[0]
        self._ypos = pos[1]
        self._id = id
        self._size = size
        self._window = window
        self._row = (id - 1) // 8 + 1
        self._column = (id - 1) % 8 + 1
        self._cord = (self._xpos+1, self._ypos+1, self._size[0]-2, self._size[1]-2)
        self.obtain = None

    def row(self):
        return self._row

    def column(self):
        return self._column

    def id(self) -> int:
        return self._id

    def window(self) -> pygame.display:
        return self._window

    def xpos(self):
        return self._xpos

    def ypos(self):
        return self._ypos

    def is_mouse_on(self, mouse: tuple):
        return True if (
            (self._xpos <= mouse[0] < self._xpos + self._size[0]) and
            (self._ypos <= mouse[1] < self._ypos + self._size[1])
            ) else False

    def draw_green_rect(self):
        GREEN = (0, 255, 0)
        pygame.draw.rect(self._window, GREEN, self._cord)

    def draw_blue_rect(self):
        BLUE = (0, 0, 255)
        pygame.draw.rect(self._window, BLUE, self._cord)

    def draw_red_rect(self):
        RED = (255, 0, 0)
        pygame.draw.rect(self._window, RED, self._cord)


class Entity:
    def __init__(self, board, field: Field, image: pygame.image, color: str):
        field.obtain = self
        self._board = board
        self._field = field
        self._image = image
        self._color = color
        self._movestatus = False

    def color(self):
        return self._color

    def change_field(self, field):
        self._field = field
        self._movestatus = True

    def draw(self):
        self._field.window().blit(self._image, (self._field.xpos(), self._field.ypos()))


class King(Entity):
    def check_field(self, row, col):
        if (
            row not in (1,2,3,4,5,6,7,8)
            or col not in (1,2,3,4,5,6,7,8)
            ):
            return
        field = self._board.find_by_row_column(row, col)
        if field.obtain is not None:
            if field.obtain.color() != self._color:
                self._attack_tiles.append(field)
            return
        self._move_tiles.append(field)

    def make_options(self):
        self._move_tiles = []
        self._attack_tiles = []

        self.check_field(self._field.row()+1, self._field.column())
        self.check_field(self._field.row()+1, self._field.column()+1)
        self.check_field(self._field.row(), self._field.column()+1)
        self.check_field(self._field.row()-1, self._field.column()+1)
        self.check_field(self._field.row()-1, self._field.column())
        self.check_field(self._field.row()-1, self._field.column()-1)
        self.check_field(self._field.row(), self._field.column()-1)
        self.check_field(self._field.row()+1, self._field.column()-1)

        return self._move_tiles, self._attack_tiles


class Bishop(Entity):
    def check_fields(self, rowcor, colcor):
        for x in range(1, 8):
            if (
                self._field.row()+rowcor*x not in (1,2,3,4,5,6,7,8)
                or self._field.column()+colcor*x not in (1,2,3,4,5,6,7,8)
                ):
                break
            field = self._board.find_by_row_column(self._field.row()+rowcor*x, self._field.column()+colcor*x)
            if field.obtain is not None:
                if field.obtain.color() != self._color:
                    self._attack_tiles.append(field)
                break
            self._move_tiles.append(field)

    def make_options(self):
        self._move_tiles = []
        self._attack_tiles = []

        self.check_fields(1,1)
        self.check_fields(1,-1)
        self.check_fields(-1,1)
        self.check_fields(-1,-1)

        return self._move_tiles, self._attack_tiles


class Horse(Entity):
    def check_field(self, row, column):
        if (
            row not in (1,2,3,4,5,6,7,8)
            or column not in (1,2,3,4,5,6,7,8)
            ):
            return
        field = self._board.find_by_row_column(row, column)
        if field.obtain is not None:
            if field.obtain.color() != self._color:
                self._attack_tiles.append(field)
            return
        self._move_tiles.append(field)

    def  make_options(self):
        self._move_tiles = []
        self._attack_tiles = []

        self.check_field(self._field.row()+1, self._field.column()-2)
        self.check_field(self._field.row()+1, self._field.column()+2)
        self.check_field(self._field.row()-1, self._field.column()-2)
        self.check_field(self._field.row()-1, self._field.column()+2)
        self.check_field(self._field.row()+2, self._field.column()-1)
        self.check_field(self._field.row()+2, self._field.column()+1)
        self.check_field(self._field.row()-2, self._field.column()-1)
        self.check_field(self._field.row()-2, self._field.column()+1)

        return self._move_tiles, self._attack_tiles


class Tower(Entity):
    def _check_field_vertical(self, cor):
        for x in range(1, 8):
            if 0 < self._field.id() + cor*x*8 <= 64:
                id = self._field.id() + cor*x*8
            else:
                break
            field = self._board.ff_by_id(id)
            if field.obtain is not None:
                if field.obtain.color() != self._color:
                    self._attack_tiles.append(field)
                break
            self._move_tiles.append(field)

    def _check_field_horizontal(self, cor):
        for x in range(1, 8):
            if 0 < self._field.id() + cor*x <= 64:
                id = self._field.id() + cor*x
            else:
                break
            field = self._board.ff_by_id(id)
            if field.row() != self._field.row():
                break
            if field.obtain is not None:
                if field.obtain.color() != self._color:
                    self._attack_tiles.append(field)
                break
            self._move_tiles.append(field)

    def make_options(self):
        self._move_tiles = []
        self._attack_tiles = []

        self._check_field_vertical(1)
        self._check_field_vertical(-1)
        self._check_field_horizontal(1)
        self._check_field_horizontal(-1)

        return self._move_tiles, self._attack_tiles


class Queen(Tower):
    def check_fields(self, rowcor, colcor):
        for x in range(1, 8):
            if (
                self._field.row()+rowcor*x not in (1,2,3,4,5,6,7,8)
                or self._field.column()+colcor*x not in (1,2,3,4,5,6,7,8)
                ):
                break
            field = self._board.find_by_row_column(self._field.row()+rowcor*x, self._field.column()+colcor*x)
            if field.obtain is not None:
                if field.obtain.color() != self._color:
                    self._attack_tiles.append(field)
                break
            self._move_tiles.append(field)

    def make_options(self):
        self._move_tiles, self._attack_tiles = super().make_options()

        self.check_fields(1,1)
        self.check_fields(1,-1)
        self.check_fields(-1,1)
        self.check_fields(-1,-1)

        return self._move_tiles, self._attack_tiles


class Pown(Entity):
    def _check_field(self, cor):
        id = self._field.id() + cor if self._color == 'black' else self._field.id() - cor
        field = self._board.ff_by_id(id)
        if (
            (field.row() == self._field.row() + 1
            or field.row() == self._field.row() - 1)
            and field.obtain is not None
            and field.obtain.color() != self.color()
            ):
            return field
        return None

    def make_options(self):
        move_tiles = []
        attack_tiles = []

        id = self._field.id() + 8 if self._color == 'black' else self._field.id() - 8
        field = self._board.ff_by_id(id)
        if field.obtain is None:
            move_tiles.append(field)

            if not self._movestatus:
                id = self._field.id() + 16 if self._color == 'black' else self._field.id() - 16
                field = self._board.ff_by_id(id)
                if field.obtain is None:
                    move_tiles.append(field)

        field = self._check_field(7)
        if field is not None:
            attack_tiles.append(field)

        field = self._check_field(9)
        if field is not None:
            attack_tiles.append(field)

        return move_tiles, attack_tiles


class Board:
    def __init__(self, fields: list, window: pygame.display, black_figures=None, white_figures=None):
        self._fields = fields
        self._bfigures = black_figures
        self._wfigures = white_figures
        self._window = window

    def set_black_figures(self, figures):
        self._bfigures = figures

    def set_white_figures(self, figures):
        self._wfigures = figures

    def ff_by_id(self, id: int) -> Field:
        return self._fields[(id - 1) // 8][(id - 1) % 8]

    def find_by_row_column(self, row, column):
        return self._fields[row-1][column-1]

    def del_figure(self, figure):
        self._bfigures.remove(figure) if figure.color() == 'black' else self._wfigures.remove(figure)

    def draw_figures(self):
        for figure in self._bfigures:
            figure.draw()
        for figure in self._wfigures:
            figure.draw()

    def where_mouse(self, mouse: tuple):
        xspos = 0 if 0 <= mouse[0] < self._window.get_width() // 2 else 4
        yspos = 0 if 0 <= mouse[1] < self._window.get_height() // 2 else 4
        for y in range(4):
            for x in range(4):
                field = self._fields[yspos + y][xspos + x]
                if field.is_mouse_on(mouse):
                    return field
        return None

    def move_figure(self, sfield, efield):
        if efield.obtain is None:
            figure = sfield.obtain
            sfield.obtain = None
            figure.change_field(efield)
            efield.obtain = figure

    def kill_and_move(self, sfield, efield):
        field = efield.obtain
        efield.obtain = None
        self.del_figure(field)
        self.move_figure(sfield, efield)
