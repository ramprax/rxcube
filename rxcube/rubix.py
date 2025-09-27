import itertools
import random
from functools import partial
from pathlib import Path

from .cube import from_cube_string, make_cube, OPPOSITE_FACES
from .cube_display import print_cube, print_cube_fg_color, print_cube_bg_color, print_large_cube_bg_color


def perform_move(move_str, cube):
    # print(f'Performing move {move_str} on cube {cube}')
    return cube.make_move(move_str)


def perform_move_sequence(move_sequence_str, cube):
    moves = move_sequence_str.split()
    # print(f'Performing move seq: {move_sequence_str}')
    for m in moves:
        m = m.strip().upper()
        if m:
            cube = perform_move(m, cube)
    return cube


def generate_random_moves(count, all_moves):
    return random.choices(all_moves, k=count)


def is_move_redundant(move, previous_moves):
    move_face = move[0]
    if previous_moves:
        last_move = previous_moves[-1]
        last_move_face = last_move[0]
        if move_face == last_move_face:
            return True

        last_same_face_move = None
        last_same_face_move_idx = -1
        for i, pm in enumerate(previous_moves):
            if pm[0] == move[0]:
                last_same_face_move = pm
                last_same_face_move_idx = i

        opp_face = OPPOSITE_FACES[move_face]
        non_opp_face_move_count = 0
        for i in range(last_same_face_move_idx+1, len(previous_moves)):
            _prev_move_i = previous_moves[i]
            _prev_move_i_face = _prev_move_i[0]
            if _prev_move_i_face != opp_face:
                non_opp_face_move_count += 1
        if non_opp_face_move_count <= 0:
            return True

    return False


def remove_redundant_moves(move_sequence):
    non_redundant_moves = []
    for m in move_sequence:
        if not is_move_redundant(m, non_redundant_moves):
            non_redundant_moves.append(m)
    return non_redundant_moves


def generate_scramble(cube):
    all_moves = cube.non_rotational_moves()
    random_moves = generate_random_moves(16*cube.size, all_moves)
    return remove_redundant_moves(random_moves)


def scramble(cube):
    moves = generate_scramble(cube)
    moves_str = ' '.join(moves)
    print('Scramble:', moves_str)
    scrambled_cube = perform_move_sequence(moves_str, cube)
    return scrambled_cube


def to_cube_string(cube):
    return cube.to_cube_string()


def save_to_file(cube, filepath):
    fp = Path(filepath)
    fp.write_text(to_cube_string(cube))


def load_from_file(filepath):
    fp = Path(filepath)
    return from_cube_string(fp.read_text())


def check_moves():
    cb1 = make_cube(3)
    print_cube(cb1)
    print(to_cube_string(cb1))
    # print_cube(from_cube_string('UUUUUUUUULLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBBDDDDDDDDD'))
    print('Making U move')
    cb2 = cb1.move_U()
    print_cube(cb2)
    print(to_cube_string(cb2))

    print("Making U' move")
    cb3 = cb2.move_u()
    print_cube(cb3)
    print(to_cube_string(cb3))

    print('Making R move')
    cb4 = cb3.move_R()
    print_cube(cb4)
    print(to_cube_string(cb4))

    print("Making R' move")
    cb5 = cb4.move_r()
    print_cube(cb5)
    print(to_cube_string(cb5))
    
    print("Making R U R' U' move sequence")
    cb6 = perform_move_sequence("R U R' U'", cb5)
    print_cube(cb6)
    print(to_cube_string(cb6))

    print("Making F move")
    cb7 = cb1.move_F()
    print_cube(cb7)
    print(to_cube_string(cb7))
    
    print("Making F' move")
    cb8 = cb7.move_f()
    print_cube(cb8)
    print(to_cube_string(cb8))

    print("Making L move")
    cb9 = cb8.move_L()
    print_cube(cb9)
    print(to_cube_string(cb9))

    print("Making L' move")
    cb10 = cb9.move_l()
    print_cube(cb10)
    print(to_cube_string(cb10))
    
    print("Making move seq: U R U' L' U R' U' L ")
    cb11 = perform_move_sequence("U R U' L' U R' U' L", cb10)
    print_cube(cb11)
    print(to_cube_string(cb11))
    
    print("Making move seq: U R' U' L U R U' L' ")
    cb12 = perform_move_sequence("U R' U' L U R U' L'", cb10)
    print_cube(cb12)
    print(to_cube_string(cb12))


def check_R_moves():
    cb1 = make_cube()

    print("R")
    print_cube(perform_move_sequence("R", cb1))

    print("RR")
    print_cube(perform_move_sequence("R R", cb1))

    print("RRR")
    print_cube(perform_move_sequence("R R R", cb1))

    print("RRRR")
    print_cube(perform_move_sequence("R R R R", cb1))


def check_L_moves():
    cb1 = make_cube()

    print("L")
    print_cube(perform_move_sequence("L", cb1))

    print("LL")
    print_cube(perform_move_sequence("L L", cb1))

    print("LLL")
    print_cube(perform_move_sequence("L L L", cb1))

    print("LLLL")
    print_cube(perform_move_sequence("L L L L", cb1))


def check_U_moves():
    cb1 = make_cube()

    print("U")
    print_cube(perform_move_sequence("U", cb1))

    print("UU")
    print_cube(perform_move_sequence("U U", cb1))

    print("UUU")
    print_cube(perform_move_sequence("U U U", cb1))

    print("UUUU")
    print_cube(perform_move_sequence("U U U U", cb1))

DISPLAY_MODES = ('simple', 'small_fg', 'small_bg', 'medium_bg', 'large_bg')
DISPLAY_FUNCS = {
    'simple': print_cube,
    'small_fg': print_cube_fg_color,
    'small_bg': print_cube_bg_color,
    'medium_bg': partial(print_large_cube_bg_color, columns_per_cell=5),
    'large_bg': print_large_cube_bg_color,
}

def process_cmd(m, ctx):
    m = m.upper().strip()
    if m == '0':
        sz = ctx['cube_size']
        ctx['cb'] = make_cube(sz)
    elif m == 'P':
       print(to_cube_string(ctx['cb']))
    elif m == '?' or m == '/':
        non_rotational_cube_moves = ' '.join(ctx['cb'].non_rotational_moves())
        whole_cube_rotation_moves = ' '.join(ctx['cb'].whole_cube_rotation_moves())
        print(f'''
        Control commands:
            ? or /       - Help
            ` or ~       - Status
            q            - Quit
            p            - Print Cube
            + or =       - Enhance cube display mode (size &/ color)
            - or _       - Simplify cube display mode (size &/ color)
            ] or }}       - Harder puzzle; Increase cube dimensions (from 2x2x2 to 3x3x3)
            [ or {{       - Easier puzzle; Decrease cube dimensions (from 3x3x3 to 2x2x2)
            0            - Reset Cube
            1            - Open *
            2            - Save *
            3 or #       - Scramble
        
        Cube face moves:
            {non_rotational_cube_moves}
        
        Whole cube rotations:
            {whole_cube_rotation_moves}
        ''')
        return
    elif m == '`' or m == '~':
        print(ctx)
        return
    elif m == '+' or m == '=':
        ctx['cube_display_mode'] = DISPLAY_MODES[min(DISPLAY_MODES.index(ctx['cube_display_mode']) + 1, len(DISPLAY_MODES) - 1)]
    elif m == '-' or m == '_':
        ctx['cube_display_mode'] = DISPLAY_MODES[max(DISPLAY_MODES.index(ctx['cube_display_mode']) - 1, 0)]
    elif m == '[' or m == '{':
        sz = ctx['cube_size']
        sz = max(2, sz - 1)
        cb = ctx['cb']
        if cb.size != sz:
            ctx['cb'] = cb = make_cube(sz)
            ctx['cube_size'] = sz
    elif m == ']' or m == '}':
        sz = ctx['cube_size']
        sz = min(3, sz + 1)
        cb = ctx['cb']
        if cb.size != sz:
            ctx['cb'] = cb = make_cube(sz)
            ctx['cube_size'] = sz
    elif m == '3' or m == '#':
        ctx['cb'] = scramble(ctx['cb'])
    elif m in '12':
        print('Command not implemented yet')
    else:
        try:
            ctx['cb'] = perform_move_sequence(m, ctx['cb'])
        except Exception as ex:
            print(f'Invalid command/move/move-sequence: {m} | {type(ex)}({ex})')
            process_cmd('?', ctx)
            return
    
    DISPLAY_FUNCS[ctx['cube_display_mode']](ctx['cb'])


def play_interactive():
    default_cube_file_path = Path('~').expanduser() / 'rubix.rbx'
    if default_cube_file_path.exists():
        cb = load_from_file(default_cube_file_path)
    else:
        cb = make_cube(3)
        save_to_file(cb, default_cube_file_path)
        
    ctx = { 'cb': cb, 'cube_size': cb.size, 'cube_display_mode': 'small_bg' }
    # process_cmd('?', ctx)
    process_cmd('P', ctx)
    while (m := input('Move (? for help)> ').strip().upper()) != 'Q':
        process_cmd(m, ctx)
        save_to_file(ctx['cb'], default_cube_file_path)


def main():
    # cb1 = make_cube()
    # print_cube(cb1)
    # U R U' L' U R' U' L
    # print("U R U' L' U R' U' L")
    # print_cube(perform_move_sequence("U R U' L' U R' U' L", cb1))
    play_interactive()


if __name__ == '__main__':
    main()

