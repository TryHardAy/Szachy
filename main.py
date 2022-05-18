import pygame
import os
from classes import (
    Field,
    Board,
    King,
    Queen,
    Bishop,
    Pown,
    Tower,
    Horse,
)

WIDTH = 800
HEIGHT = 800
EDGE_SIZE = 24

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

turn = 'white'

highlight_ff = None
highlight_nf = None
highlight_ef = None

def create_fields():
    fields = []
    field_width = (WIDTH - EDGE_SIZE * 2) / 8
    field_height = (HEIGHT - EDGE_SIZE * 2) / 8
    for i in range(8):
        row = []
        for j in range(8):
            pos = (24 + field_width * j, 24 + field_height * i)
            row.append(Field(pos, (field_width, field_height), i * 8 + j + 1, WINDOW))
        fields.append(row)
    return fields


def load_and_transform(path: str):
    return pygame.transform.scale(pygame.image.load(path), ((WIDTH - EDGE_SIZE * 2) / 8, (HEIGHT - EDGE_SIZE * 2) / 8))


def change_turn():
    global turn
    turn = 'white' if turn == 'black' else 'black'


def draw_window():
    if highlight_ff is not None:
        highlight_ff.draw_green_rect()

    if highlight_nf is not None:
        for field in highlight_nf:
            field.draw_blue_rect()

    if highlight_ef is not None:
        for field in highlight_ef:
            field.draw_red_rect()

    board.draw_figures()


def move(mouse):
    if highlight_nf is not None:
        for field in highlight_nf:
            if field.is_mouse_on(mouse):
                board.move_figure(highlight_ff, field)
                change_turn()

    if highlight_ef is not None:
        for field in highlight_ef:
            if field.is_mouse_on(mouse):
                board.kill_and_move(highlight_ff, field)
                change_turn()


def main():
    pygame.display.set_caption("Szachy")
    background = pygame.image.load(os.path.join('plansza', 'szachownica.jpg'))

    KING_WHITE_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'krol_bialy.png'))
    QUEEN_WHITE_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'krolowa_biala.png'))
    BISHOP_WHITE_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'goniec_bialy.png'))
    HORSE_WHITE_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'kon_bialy.png'))
    TOWER_WHITE_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'wieza_biala.png'))
    POWN_WHITE_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'pionek_bialy.png'))

    KING_BLACK_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'krol_czarny.png'))
    QUEEN_BLACK_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'krolowa_czarna.png'))
    BISHOP_BLACK_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'goniec_czarny.png'))
    HORSE_BLACK_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'kon_czarny.png'))
    TOWER_BLACK_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'wieza_czarna.png'))
    POWN_BLACK_IMAGE = load_and_transform(os.path.join('figury_szachowe', 'pionek_czarny.png'))

    black_figures = []
    white_figures = []

    fields = create_fields()
    global board
    board = Board(fields, WINDOW)

    black_figures.append(King(board, board.ff_by_id(5), KING_BLACK_IMAGE, 'black'))
    black_figures.append(Queen(board, board.ff_by_id(4), QUEEN_BLACK_IMAGE, 'black'))
    black_figures.append(Bishop(board, board.ff_by_id(3), BISHOP_BLACK_IMAGE, 'black'))
    black_figures.append(Bishop(board, board.ff_by_id(6), BISHOP_BLACK_IMAGE, 'black'))
    black_figures.append(Horse(board, board.ff_by_id(2), HORSE_BLACK_IMAGE, 'black'))
    black_figures.append(Horse(board, board.ff_by_id(7), HORSE_BLACK_IMAGE, 'black'))
    black_figures.append(Tower(board, board.ff_by_id(1), TOWER_BLACK_IMAGE, 'black'))
    black_figures.append(Tower(board, board.ff_by_id(8), TOWER_BLACK_IMAGE, 'black'))
    for num in range(8):
        black_figures.append(Pown(board, board.ff_by_id(num + 9), POWN_BLACK_IMAGE, 'black'))

    white_figures.append(King(board, board.ff_by_id(61), KING_WHITE_IMAGE, 'white'))
    white_figures.append(Queen(board, board.ff_by_id(60), QUEEN_WHITE_IMAGE, 'white'))
    white_figures.append(Bishop(board, board.ff_by_id(59), BISHOP_WHITE_IMAGE, 'white'))
    white_figures.append(Bishop(board, board.ff_by_id(62), BISHOP_WHITE_IMAGE, 'white'))
    white_figures.append(Horse(board, board.ff_by_id(58), HORSE_WHITE_IMAGE, 'white'))
    white_figures.append(Horse(board, board.ff_by_id(63), HORSE_WHITE_IMAGE, 'white'))
    white_figures.append(Tower(board, board.ff_by_id(57), TOWER_WHITE_IMAGE, 'white'))
    white_figures.append(Tower(board, board.ff_by_id(64), TOWER_WHITE_IMAGE, 'white'))
    for num in range(8):
        white_figures.append(Pown(board, board.ff_by_id(num + 49), POWN_WHITE_IMAGE, 'white'))

    board.set_black_figures(black_figures)
    board.set_white_figures(white_figures)

    global highlight_ff
    global highlight_nf
    global highlight_ef

    clock = pygame.time.Clock()
    run = True

    while run:

        clock.tick(60)
        WINDOW.blit(background, (0, 0))

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                move(mouse)

                field = board.where_mouse(mouse)
                if field is not None and field.obtain and field.obtain.color() == turn:
                    highlight_ff = field
                    highlight_nf, highlight_ef = field.obtain.make_options()
                else:
                    highlight_ff = None
                    highlight_nf = None
                    highlight_ef = None

        draw_window()

        pygame.display.update()


if __name__ == "__main__":
    main()
