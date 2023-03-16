from unittest.mock import Mock
from tagesschauscraper.retrieve import WebsiteTest
from requests import Response
import pytest


@pytest.fixture
def response_mock() -> Response:
    responseMock = Mock(spec=Response)
    responseMock.status_code = 200
    with open("tests/data/teaser-snippet.html", "r") as f:
        responseMock.text = f.read()
    return responseMock


def test_is_element(response_mock: Response) -> None:
    websiteTest = WebsiteTest(response_mock)
    assert websiteTest.is_element(
        attrs={"class": "teaser-xs__headline-wrapper"}
    )


def test_is_text_in_element(response_mock: Response) -> None:
    websiteTest = WebsiteTest(response_mock)
    text = "Nordstream-Betreiber offenbar insolvent"
    attrs = {"class": "teaser-xs__headline-wrapper"}
    assert websiteTest.is_text_in_element(target_text=text, attrs=attrs)
