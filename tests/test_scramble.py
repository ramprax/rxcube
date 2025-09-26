from rxcube.cube import make_cube
from rxcube.rubix import generate_scramble, perform_move_sequence


def test_scramble_3x3x3_001():
    cb = make_cube(3)
    s = generate_scramble(cb)
    print(s)
    assert s is not None
    assert len(s) > 0

    cb_scrambled = perform_move_sequence(' '.join(s), cb)
    assert not cb_scrambled.is_solved()


def test_scramble_2x2x2_001():
    cb = make_cube(2)
    s = generate_scramble(cb)
    print(s)
    assert s is not None
    assert len(s) > 0

    cb_scrambled = perform_move_sequence(' '.join(s), cb)
    assert not cb_scrambled.is_solved()

