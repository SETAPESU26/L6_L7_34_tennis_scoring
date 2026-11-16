"""Property-based tests for Lab 7's current input and scoring behavior.

"No crash" means valid inputs return the documented result and malformed
inputs raise the exception naturally produced by the current implementation.
These tests do not require malformed input to be accepted or normalized.

Expected malformed-input exceptions from tennis_scoring.py:
- parse_score: AttributeError for None; ValueError for the wrong number of
  separators or a field that int() cannot parse.
- game_lead: AttributeError for None; ValueError for the wrong number of
  separators; KeyError for a point label outside 0, 15, 30, and 40.
- set_spread: AttributeError for None; ValueError for an empty CSV, an empty
  field, or a field that int() cannot parse.
"""

import pytest
from hypothesis import example, given, settings, strategies as st

from tennis_scoring import game_lead, parse_score, set_spread


SMALL_INT = st.integers(min_value=-10**12, max_value=10**12)
MALFORMED_TEXT = st.one_of(
    st.sampled_from(
        [
            "",
            "1",
            "1-",
            "-1",
            "1-2-3",
            "a-b",
            "1-x",
            "--",
            ",",
            "1,,2",
            "0-",
        ]
    ),
    st.text(max_size=30),
)


@settings(max_examples=100)
@given(
    st.one_of(
        st.tuples(
            st.integers(min_value=0, max_value=10**12),
            st.integers(min_value=0, max_value=10**12),
        ).map(lambda pair: f"{pair[0]}-{pair[1]}"),
        MALFORMED_TEXT,
        st.none(),
    )
)
@example("0-0")
@example("3-2")
@example("")
@example("1")
@example("1-2-3")
@example("x-2")
@example(None)
@example("-1-2")
@example("1--2")
def test_parse_score_no_crash(s):
    """Valid A-B tallies parse; malformed forms raise their current errors."""
    if s is None:
        with pytest.raises(AttributeError):
            parse_score(s)
        return

    fields = s.split("-")
    if len(fields) != 2:
        with pytest.raises(ValueError):
            parse_score(s)
        return

    try:
        expected = (int(fields[0]), int(fields[1]))
    except ValueError:
        with pytest.raises(ValueError):
            parse_score(s)
    else:
        assert parse_score(s) == expected


@settings(max_examples=100)
@given(
    st.one_of(
        st.tuples(
            st.sampled_from(("0", "15", "30", "40")),
            st.sampled_from(("0", "15", "30", "40")),
        ).map(lambda pair: f"{pair[0]}-{pair[1]}"),
        MALFORMED_TEXT,
        st.none(),
    )
)
@example("0-0")
@example("40-40")
@example("0-40")
@example("")
@example("0")
@example("0-15-30")
@example("Advantage-40")
@example("x-40")
@example(None)
def test_game_lead_no_crash(s):
    """Ordinary tennis labels produce an ordinal lead; malformed input fails."""
    if s is None:
        with pytest.raises(AttributeError):
            game_lead(s)
        return

    fields = s.split("-")
    if len(fields) != 2:
        with pytest.raises(ValueError):
            game_lead(s)
        return

    point_order = {"0": 0, "15": 1, "30": 2, "40": 3}
    if fields[0] not in point_order or fields[1] not in point_order:
        with pytest.raises(KeyError):
            game_lead(s)
    else:
        expected = point_order[fields[0]] - point_order[fields[1]]
        assert game_lead(s) == expected


@settings(max_examples=100)
@given(
    st.one_of(
        st.lists(SMALL_INT, min_size=1, max_size=10).map(
            lambda values: ",".join(str(value) for value in values)
        ),
        MALFORMED_TEXT,
        st.none(),
    )
)
@example("0")
@example("-3,0,4")
@example("4,4")
@example("")
@example("1,,2")
@example("one,2")
@example(None)
def test_set_spread_no_crash(games_csv):
    """CSV integers, including negatives and singletons, return max minus min."""
    if games_csv is None:
        with pytest.raises(AttributeError):
            set_spread(games_csv)
        return

    fields = games_csv.split(",")
    try:
        values = [int(field) for field in fields]
    except ValueError:
        with pytest.raises(ValueError):
            set_spread(games_csv)
    else:
        expected = max(values) - min(values)
        assert set_spread(games_csv) == expected
