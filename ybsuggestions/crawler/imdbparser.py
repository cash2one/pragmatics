from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import quote_plus
from bs4 import BeautifulSoup


class IMDbSearchParser:
    def __init__(self):
        self.search_url = 'http://akas.imdb.com/search/'
        self.response = None
        self.soup = None
        self.search_kind = None
        self.search_value = None

    def _make_request(self, url):
        if not url:
            self.response = None
            return

        try:
            req = Request(url, None, headers={'User-Agent': 'Mozilla/5.0', "Accept-Language": "en-US,en;q=0.5"})
        except ValueError:
            self.response = None
            return

        try:
            self.response = urlopen(req)
        except URLError as e:
            raise ValueError('HTTP endpoint cannot be reached')

    def _make_soup(self):
        if not self.response:
            raise ValueError('Response not set')

        self.soup = BeautifulSoup(self.response.read(), 'html.parser')

    def _get_elements_by_class(self, element, class_):
        if not self.soup:
            raise ValueError('Soup not set')
        if not class_:
            return []

        return self.soup.find_all(element, class_)

    @staticmethod
    def _parse_movie_item(item):
        if not item:
            return None

        try:
            cover = item.find(class_="lister-item-image").find("img")['loadlate']
            if 'nopicture' not in cover:
                cover = cover.replace('67_', '182_')\
                                .replace('98_', '268_')\
                                .replace(',67', ',182')\
                                .replace(',98', ',268')
                # cover = cover[0]+'@._V1_UX182_CR0,0182,268_AL_.jpg'
            else:
                cover = None
        except TypeError:
            cover = None

        title = item.find(class_="lister-item-content").find("a").string
        genres = item.find(class_="lister-item-content").find(class_="genre").string.strip().split(", ")

        try:
            rating = float(item.find(class_="ratings-imdb-rating")["data-value"])
        except TypeError:
            rating = 0

        movie_info = {
            'title': title,
            'genres': genres,
            'rating': rating,
            'cover': cover
        }

        return movie_info

    def find_movies_by_title(self, title, only_first=False):
        if not title:
            return None

        self._make_request(self.search_url+'title?title='+quote_plus(title)+'&view=advanced')
        self._make_soup()

        found_items = self._get_elements_by_class('div', 'lister-item mode-advanced')
        movies_infos = []
        if not found_items:
            return movies_infos

        if only_first:
            found_items = found_items[:1]

        for item in found_items:
            movies_infos.append(IMDbSearchParser._parse_movie_item(item))

        return movies_infos

