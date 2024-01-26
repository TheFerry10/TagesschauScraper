import pytest
from bs4 import BeautifulSoup

from tagesschauscraper.domain.article import ArticleScraper, ArticleTagNotFound


@pytest.mark.parametrize(
    "article_html,is_valid",
    [
        pytest.param("valid-article.html", True, id="valid"),
        pytest.param("invalid-article.html", False, id="invalid"),
    ],
    indirect=["article_html"],
)
def test_can_classify_article_correctly(article_html, is_valid):
    soup = BeautifulSoup(article_html, "html.parser")
    article_ = ArticleScraper(soup)
    assert article_.valid is is_valid


def test_extract_topline(valid_article: ArticleScraper):
    expected_topline = "Test topline"
    topline = valid_article.extract_topline()
    assert topline == expected_topline


def test_tag_not_found_for_invalid_article(invalid_article: ArticleScraper):
    with pytest.raises(expected_exception=ArticleTagNotFound):
        topline = invalid_article.extract_topline()


def test_extract_headline(valid_article: ArticleScraper):
    expected_headline = "Test headline"
    headline = valid_article.extract_headline()
    assert headline == expected_headline


def test_extract_metatextline(valid_article: ArticleScraper):
    expected_metatextline = "Stand: 07.10.2023 17:43 Uhr"
    metatextline = valid_article.extract_metatextline()
    assert metatextline == expected_metatextline


def test_extract_subheads(valid_article: ArticleScraper):
    expected_subheads = "|".join(["Subhead 1", "Subhead 2"])
    subheads = valid_article.extract_subheads()
    assert subheads == expected_subheads


def test_extract_abstract(valid_article: ArticleScraper):
    expected_abstract = "Test abstract"
    abstract = valid_article.extract_abstract()
    assert abstract == expected_abstract


def test_extract_paragraphs(valid_article: ArticleScraper):
    expected_paragraphs = "|".join(["Paragraph 1"])
    paragraphs = valid_article.extract_paragraphs()
    assert paragraphs == expected_paragraphs


def test_extract_tags(valid_article: ArticleScraper):
    expected_tags = "|".join(["tag1", "tag2", "tag3"])
    tags = valid_article.extract_tags()
    assert tags == expected_tags
