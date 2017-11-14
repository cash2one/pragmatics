import pytest
import os
os.environ["APP_SETTINGS"] = "testing"
from bs4 import BeautifulSoup
from ybsuggestions.crawler.imdbparser import IMDbSearchParser


@pytest.fixture()
def parser():
    imdb_parser = IMDbSearchParser()

    return imdb_parser


def test_imdbparser_make_request_sets_none_response_for_empty_url(parser):
    parser._make_request('')

    assert not parser.response


def test_imdbparser_make_request_sets_none_response_for_wrong_url(parser):
    parser._make_request("not-an-url")

    assert not parser.response


def test_imdbparser_make_request_raise_exception_for_not_responding_url(parser):
    with pytest.raises(ValueError) as e:
        parser._make_request("http://shoud.not.responding.com.pl")
    assert "HTTP endpoint cannot be reached" in str(e.value)


def test_imdbparser_make_request_raise_exception_for_unreachable_url(parser):
    with pytest.raises(ValueError) as e:
        parser._make_request(parser.search_url + 'zzzzfff222')
    assert "HTTP endpoint cannot be reached" in str(e.value)


def test_imdbparser_make_request_sets_response(parser):
    parser._make_request(parser.search_url + 'title?title=Private')

    assert parser.response


def test_imdbparser_make_soup_raise_exception_for_unsetted_response(parser):
    with pytest.raises(ValueError) as e:
        parser._make_soup()
    assert "Response not set" in str(e.value)


def test_imdbparser_make_soup_sets_soup(parser):
    parser._make_request(parser.search_url)
    parser._make_soup()

    assert parser.soup
    assert type(parser.soup) == BeautifulSoup


def test_imdbparser_get_elements_by_class_raise_exception_for_unsetted_soup(parser):
    parser._make_request(parser.search_url + 'title?title=Lord')

    with pytest.raises(ValueError) as e:
        parser._get_elements_by_class('div', 'lister-item mode-advanced')
    assert "Soup not set" in str(e.value)


def test_imdbparser_get_elements_by_class_finds_items_list(parser):
    parser._make_request(parser.search_url + 'title?title=Lord')
    parser._make_soup()

    assert parser._get_elements_by_class('div', 'lister')


def test_imdbparser_get_elements_by_class_finds_nothing_for_absent_element(parser):
    parser._make_request(parser.search_url + 'title?title=BlaBlaDede')
    parser._make_soup()

    assert not parser._get_elements_by_class('div', 'lister-not-here')


def test_imdbparser_parse_movie_item_finds_returns_none_invalid_item():
    assert not IMDbSearchParser._parse_movie_item(None)


def test_imdbparser_parse_movie_item_finds_creates_imdbinfo_for_valid_item(parser):
    parser._make_request(parser.search_url + 'title?title=Lord')
    parser._make_soup()
    found_items = parser._get_elements_by_class('div', 'lister-item mode-advanced')

    assert found_items

    imdb_info = IMDbSearchParser._parse_movie_item(found_items[0])

    assert imdb_info
    assert set(['title', 'rating', 'genres', 'cover']) == set(imdb_info.keys())


def test_imdbparser_find_movies_by_title_finds_nothing_for_unrecognized_title(parser):

    results = parser.find_movies_by_title('BlaBlaDede')

    assert not results


def test_imdbparser_find_movies_by_title_finds_items_for_recognized_title(parser):

    results = parser.find_movies_by_title('Lord of the Ring')

    assert results
    assert len(results) > 1


def test_imdbparser_find_movies_by_title_finds_one_item_when_this_flag_is_true(parser):

    results = parser.find_movies_by_title('Lord of the Ring', only_first=True)

    assert results
    assert len(results) == 1