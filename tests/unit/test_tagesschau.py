from tagesschauscraper import tagesschau
from datetime import date
from bs4 import BeautifulSoup
import pytest




html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

archive_header_html = """
<div class="trenner">
        <div class="trenner__text">
            <div class="trenner__text__topline">
                Archiv
            </div>
            <div class="trenner__text__headline">
                <h2>Meldungen</h2>
            </div>
        </div>
</div>
"""


def test_required_attributes_exist():
    soup = BeautifulSoup(archive_header_html, 'html.parser')
    assert tagesschau.required_attributes_exist(soup)


def test_bs4():
    soup = BeautifulSoup(html_doc, 'html.parser')
    r = soup.find("p", {"class": "title"}).get_text(strip=True)
    print(r)
    assert "The Dormouse's story" == r

def test_if_available_category_is_recognized():
    assert tagesschau.is_selected_in_categories("wirtschaft")
    
    
def test_if_not_available_category_leads_to_false():
    assert not tagesschau.is_selected_in_categories("test category")
    
def test_creation_of_request_params():
    expected_params = {
        "datum": "2023-02-04",
        "filter": "wirtschaft"
    }
    archiveFilter = tagesschau.ArchiveFilter(date(2023, 2, 4), "wirtschaft")
    request_params = tagesschau.create_request_params(archiveFilter)
    assert request_params == expected_params