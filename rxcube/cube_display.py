from colorama import Fore, Back, init

from .cube import COLOUR_MAP

init()

COLORAMA_BG_MAP = {
    'w': Back.WHITE,
    'y': Back.LIGHTYELLOW_EX,
    'g': Back.GREEN,
    'r': Back.RED,
    'o': Back.YELLOW,
    'b': Back.BLUE,
}

COLORAMA_FG_MAP = {
    'w': Fore.WHITE,
    'y': Fore.LIGHTYELLOW_EX,
    'g': Fore.GREEN,
    'r': Fore.RED,
    'o': Fore.YELLOW,
    'b': Fore.BLUE,
}


def print_cube(cube):
    cube.print_cube()


def print_cube_fg_color(cube):
    sz = cube.size
    fc_size = sz * sz
    cube_face_values = [v for v in cube.to_cube_string()]
    u_face, l_face, f_face, r_face, b_face, d_face = [cube_face_values[i:i+fc_size]
                                                      for i in range(0, len(cube_face_values), fc_size)]

    u_face_rows = [u_face[i:i + sz] for i in range(0, fc_size, sz)]
    lfrb_rows = [
        l_face[i:i + sz] + f_face[i:i + sz] + r_face[i:i + sz] + b_face[i:i + sz]
        for i in range(0, fc_size, sz)
    ]
    d_face_rows = [d_face[i:i + sz] for i in range(0, fc_size, sz)]

    columns_per_cell = 3
    columns_per_row = columns_per_cell * sz
    indent_spaces = ' ' * columns_per_row
    cell_space_padding = ' ' * int((columns_per_cell - 1) / 2)

    u_face_str = '\n'.join([indent_spaces + (
        ''.join([
            f'{COLORAMA_FG_MAP[COLOUR_MAP[cell]]}{cell_space_padding}{COLOUR_MAP[cell]}{cell_space_padding}{Fore.RESET}'
            for cell in row])) for row
                            in u_face_rows])

    lfrb_rows_str = '\n'.join(
        [''.join([
            f'{COLORAMA_FG_MAP[COLOUR_MAP[cell]]}{cell_space_padding}{COLOUR_MAP[cell]}{cell_space_padding}{Fore.RESET}'
            for cell in lfrb_row]) for
            lfrb_row in lfrb_rows])

    d_face_str = '\n'.join([indent_spaces + (
        ''.join([
            f'{COLORAMA_FG_MAP[COLOUR_MAP[cell]]}{cell_space_padding}{COLOUR_MAP[cell]}{cell_space_padding}{Fore.RESET}'
            for cell in row])) for row
                            in d_face_rows])

    cube_display_str = '\n'.join([u_face_str, lfrb_rows_str, d_face_str])

    print(cube_display_str)


def print_cube_bg_color(cube):
    sz = cube.size
    fc_size = sz * sz
    cube_face_values = [v for v in cube.to_cube_string()]
    u_face, l_face, f_face, r_face, b_face, d_face = [cube_face_values[i:i+fc_size]
                                                      for i in range(0, len(cube_face_values), fc_size)]

    u_face_rows = [u_face[i:i+sz] for i in range(0, fc_size, sz)]
    lfrb_rows = [
        l_face[i:i+sz] + f_face[i:i+sz] + r_face[i:i+sz] + b_face[i:i+sz]
        for i in range(0, fc_size, sz)
    ]
    d_face_rows = [d_face[i:i+sz] for i in range(0, fc_size, sz)]

    columns_per_cell = 3
    columns_per_row = columns_per_cell * sz
    indent_spaces = ' ' * columns_per_row
    cell_space_padding = ' ' * int((columns_per_cell - 1)/2)

    u_face_str = '\n'.join([indent_spaces + (
        ''.join([f'{COLORAMA_BG_MAP[COLOUR_MAP[cell]]}{cell_space_padding}{COLOUR_MAP[cell]}{cell_space_padding}{Back.RESET}' for cell in row])) for row
                            in u_face_rows])


    lfrb_rows_str = '\n'.join(
        [''.join([f'{COLORAMA_BG_MAP[COLOUR_MAP[cell]]}{cell_space_padding}{COLOUR_MAP[cell]}{cell_space_padding}{Back.RESET}' for cell in lfrb_row]) for
         lfrb_row in lfrb_rows])

    d_face_str = '\n'.join([indent_spaces + (
        ''.join([f'{COLORAMA_BG_MAP[COLOUR_MAP[cell]]}{cell_space_padding}{COLOUR_MAP[cell]}{cell_space_padding}{Back.RESET}' for cell in row])) for row
                            in d_face_rows])

    cube_display_str = Fore.BLACK + '\n'.join([u_face_str, lfrb_rows_str, d_face_str]) + Fore.RESET

    print(cube_display_str)


def print_large_cube_bg_color(cube, rows_per_cell=3, columns_per_cell=7):
    """
              U  U  U
              U  U  U
              U  U  U
        L  L  L  F  F  F  R  R  R  B  B  B
        L  L  L  F  F  F  R  R  R  B  B  B
        L  L  L  F  F  F  R  R  R  B  B  B
              D  D  D
              D  D  D
              D  D  D

        U L F R B D

    """
    sz = cube.size
    fc_size = sz * sz
    cube_face_values = [v for v in cube.to_cube_string()]
    u_face, l_face, f_face, r_face, b_face, d_face = [cube_face_values[i:i+fc_size]
                                                      for i in range(0, len(cube_face_values), fc_size)]

    u_face_rows = [u_face[i:i+sz] for i in range(0, fc_size, sz)]
    lfrb_rows = [
        l_face[i:i+sz] + f_face[i:i+sz] + r_face[i:i+sz] + b_face[i:i+sz]
        for i in range(0, fc_size, sz)
    ]
    d_face_rows = [d_face[i:i+sz] for i in range(0, fc_size, sz)]

    columns_per_row = columns_per_cell * sz
    indent_spaces = ' ' * columns_per_row
    cell_space_padding = ' ' * int((columns_per_cell - 1)/2)

    rows_per_face = rows_per_cell * sz
    if rows_per_cell > 1:
        text_rows = [i for i in range(1,rows_per_face+1, rows_per_cell)]
    else:
        text_rows = list(range(sz))

    u_face_str_list = []
    for i in range(rows_per_face):
        row = u_face_rows[int(i / rows_per_cell)]
        is_text_value = (i in text_rows)
        row_str = indent_spaces + (''.join([
            f"{COLORAMA_BG_MAP[COLOUR_MAP[cell]]}{cell_space_padding}{COLOUR_MAP[cell].upper() if is_text_value else ' '}{cell_space_padding}{Back.RESET}"
            for cell in row]))
        u_face_str_list.append(row_str)

    u_face_str = '\n'.join(u_face_str_list)

    lfrb_row_str_list = []
    for i in range(rows_per_face):
        row = lfrb_rows[int(i / rows_per_cell)]
        is_text_value = (i in text_rows)
        row_str = ''.join([
            f"{COLORAMA_BG_MAP[COLOUR_MAP[cell]]}{cell_space_padding}{COLOUR_MAP[cell].upper() if is_text_value else ' '}{cell_space_padding}{Back.RESET}"
            for cell in row])
        lfrb_row_str_list.append(row_str)
    lfrb_rows_str = '\n'.join(lfrb_row_str_list)

    d_face_str_list = []
    for i in range(rows_per_face):
        row = d_face_rows[int(i / rows_per_cell)]
        is_text_value = (i in text_rows)
        row_str = indent_spaces + (''.join([
            f"{COLORAMA_BG_MAP[COLOUR_MAP[cell]]}{cell_space_padding}{COLOUR_MAP[cell].upper() if is_text_value else ' '}{cell_space_padding}{Back.RESET}"
            for cell in row]))
        d_face_str_list.append(row_str)

    d_face_str = '\n'.join(d_face_str_list)

    cube_display_str = Fore.BLACK + '\n'.join([u_face_str, lfrb_rows_str, d_face_str]) + Fore.RESET

    print(cube_display_str)

