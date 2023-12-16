import pytest


def test_teaser_config():
    test_date = date(2023, 11, 4)
    test_category = "wirtschaft"
    archive_filter = ArchiveFilter(test_date, test_category)
    request_params = create_request_params(archive_filter)
    pytest.fail()


def test_article_config():
    pytest.fail()
