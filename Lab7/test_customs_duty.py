import math

from hypothesis import given, strategies as st
from customs_duty import parse_declaration, duty_amount, hs_chapter


@given(st.text() | st.none())
def test_parse_declaration_no_crash(s):
    try:
        parse_declaration(s)
    except Exception as e:
        assert False, f"parse_declaration crashed with: {e!r}"


@given(st.text() | st.none())
def test_duty_amount_no_crash(s):
    try:
        duty_amount(s)
    except Exception as e:
        assert False, f"duty_amount crashed with: {e!r}"


@given(st.text() | st.none())
def test_hs_chapter_no_crash(s):
    try:
        hs_chapter(s)
    except Exception as e:
        assert False, f"hs_chapter crashed with: {e!r}"


# ---- Extra property checks on results (outputs must be sane, not just non-crashing) ----

@given(st.text() | st.none())
def test_parse_declaration_result_is_valid(s):
    result = parse_declaration(s)
    if result is not None:
        category, value = result
        assert isinstance(category, str) and category != ""
        assert math.isfinite(value) and value >= 0


@given(st.text() | st.none())
def test_duty_amount_result_is_valid(s):
    result = duty_amount(s)
    if result is not None:
        assert math.isfinite(result) and result >= 0


@given(st.text() | st.none())
def test_hs_chapter_result_is_valid(s):
    result = hs_chapter(s)
    if result is not None:
        assert isinstance(result, int) and 1 <= result <= 99


# ---- Sanity checks on well-formed input ----

def test_known_good_inputs():
    assert parse_declaration("Electronics: 25000") == ("electronics", 25000.0)
    assert duty_amount("25000@20") == 5000.0
    assert hs_chapter("8517.12") == 85