import pytest
from tennis_scoring import game_score, set_winner, match_status

def test_game_start():
    assert game_score(0, 0) == "0-0"


def test_set_undecided():
    assert set_winner(3, 2) is None


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 0, "15-0"),
        (2, 1, "30-15"),
        (3, 2, "40-30"),
        (3, 3, "deuce"),
        (4, 3, "advantage A"),
        (3, 4, "advantage B"),
        (5, 3, "game A"),
        (3, 5, "game B"),
        (4, 2, "game A"),
        (2, 4, "game B"),
    ],
)
def test_game_score_returns_expected_score_or_result(a, b, expected):
    assert game_score(a, b) == expected


@pytest.mark.parametrize(("a", "b"), [(-1, 0), (0, -1)])
def test_game_score_rejects_negative_points(a, b):
    with pytest.raises(ValueError):
        game_score(a, b)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (6, 4, "A"),
        (4, 6, "B"),
        (5, 5, None),
        (6, 6, None),
        (7, 6, "A"),
        (6, 7, "B"),
    ],
)
def test_set_winner_returns_expected_result(a, b, expected):
    assert set_winner(a, b) == expected


@pytest.mark.parametrize(
    ("sets_a", "sets_b", "best_of", "expected"),
    [
        (2, 0, 3, "A wins"),
        (0, 2, 3, "B wins"),
        (1, 1, 3, "decider"),
        (0, 0, 3, "in progress"),
    ],
)
def test_match_status_returns_expected_status(sets_a, sets_b, best_of, expected):
    assert match_status(sets_a, sets_b, best_of) == expected
