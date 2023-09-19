import pytest


def test_is_element():
    with open("tests/data/teaser-snippet.html", "r") as f:
        html = f.read()
    pytest.fail()


def test_is_text_in_element():
    with open("tests/data/teaser-snippet.html", "r") as f:
        html = f.read()
        pytest.fail()
