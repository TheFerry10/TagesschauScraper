import pytest

from tagesschau.domain import model


@pytest.mark.parametrize(
    "html, config",
    [("archive/valid-archive.html", "archive-config.yml")],
    indirect=True,
)
def test_extract_archive(scraper):
    expected = model.Archive(
        date="3. Februar 2024",
        news_category_names=(
            "Alle Ressorts|"
            "Inland|"
            "Ausland|"
            "Wirtschaft|"
            "Wissen|"
            "Faktenfinder|"
            "Investigativ"
        ),
        news_category_links=(
            "https://www.tagesschau.de/archiv?datum=2024-02-03|"
            "https://www.tagesschau.de/archiv?datum=2024-02-03&filter=inland|"
            "https://www.tagesschau.de/archiv?datum=2024-02-03&filter=ausland|"
            "https://www.tagesschau.de/archiv?datum=2024-02-03&filter=wirtschaft|"
            "https://www.tagesschau.de/archiv?datum=2024-02-03&filter=wissen|"
            "https://www.tagesschau.de/archiv?datum=2024-02-03&filter=faktenfinder|"
            "https://www.tagesschau.de/archiv?datum=2024-02-03&filter=investigativ"
        ),
    )
    assert scraper.can_scrape()
    extracted_data = scraper.extract()
    archive_ = model.Archive(**extracted_data)
    assert archive_ == expected


@pytest.mark.parametrize(
    "html",
    ["archive/valid-archive.html"],
    indirect=True,
)
def test_extract_teaser_list(soup):
    teaser_list = model.extract_teaser_list(soup)
    teaser_dates = [t.get("data-teaserdate") for t in teaser_list]
    expected_teaser_dates = ["1706971820", "1706945197"]
    assert len(teaser_list) == 2
    assert teaser_dates == expected_teaser_dates


def test_if_available_category_is_recognized():
    assert model.is_selected_in_categories("wirtschaft")


def test_if_not_available_category_leads_to_false():
    assert not model.is_selected_in_categories("test category")


@pytest.mark.parametrize(
    "html, config",
    [("article/valid-article.html", "article-config.yml")],
    indirect=True,
)
def test_extract_article(scraper):
    expected_article = model.Article(
        topline="Test topline",
        headline="Test headline",
        metatextline="Stand: 07.10.2023 17:43 Uhr",
        subheads="Subhead 1|Subhead 2",
        abstract="Test abstract",
        paragraphs="Paragraph 1",
        tags="tag1|tag2|tag3",
        article_link="https://www.tagesschau.de/inland/dummy-article.html",
    )
    assert scraper.can_scrape()
    extracted_data = scraper.extract()
    article_ = model.Article(**extracted_data)
    assert article_ == expected_article


@pytest.mark.parametrize(
    "html, config",
    [("teaser/valid-teaser.html", "teaser-config.yml")],
    indirect=True,
)
def test_extract_teaser(scraper):
    expectedTeaser = model.Teaser(
        date="08.10.2023 • 13:17 Uhr",
        shorttext="Test short text",
        headline="Test headline",
        topline="Test topline",
        article_link="/dummy/article.html",
    )
    assert scraper.can_scrape()
    extracted_data = scraper.extract()
    teaser_ = model.Teaser(**extracted_data)
    assert teaser_ == expectedTeaser
