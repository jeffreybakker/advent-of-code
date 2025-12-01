from .puzzle_1 import apply_iterative as apply_instruction


def test_land_on_zero():
    new_position, through_zero = apply_instruction(50, -50)
    assert new_position == 0
    assert through_zero == 1


def test_negative():
    new_position, through_zero = apply_instruction(5, -10)
    assert new_position == 95
    assert through_zero == 1


def test_positive():
    new_position, through_zero = apply_instruction(95, 10)
    assert new_position == 5
    assert through_zero == 1


def test_no_zero():
    new_position, through_zero = apply_instruction(5, 0)
    assert new_position == 5
    assert through_zero == 0

    new_position, through_zero = apply_instruction(50, 10)
    assert new_position == 60
    assert through_zero == 0

    new_position, through_zero = apply_instruction(50, -10)
    assert new_position == 40
    assert through_zero == 0


def test_from_zero():
    new_position, through_zero = apply_instruction(0, -10)
    assert new_position == 90
    assert through_zero == 0

    new_position, through_zero = apply_instruction(0, 10)
    assert new_position == 10
    assert through_zero == 0
