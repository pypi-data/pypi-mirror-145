import json
import urllib
from abc import ABCMeta, abstractmethod
from urllib.request import urlopen, Request

import bs4
import requests

from bs4 import BeautifulSoup
from kocrawl.base import BaseCrawler
from kocrawl.decorators import searcher


@searcher
class BaseSearcher(BaseCrawler, metaclass=ABCMeta):

    @abstractmethod
    def _make_query(self, *args, **kwargs):
        raise NotImplementedError

    def __bs4(self, url: str, query: str) -> bs4.BeautifulSoup:
        """
        beautiful soup 4를 이용하여 정적 웹페이지에 대한 크롤링을 시도합니다.

        :param url: 베이스 url
        :param query: 검색할 쿼리
        :return: parsing된 html
        """

        if query:
            url += urllib.parse.quote(query)

        if "search.naver?query=" in url:
            url += "&dicType=1"

        out = bs4.BeautifulSoup(urlopen(Request(url, headers=self.headers)).read(), 'html.parser')
        return out

    def _bs4_contents(self, url: str, selectors: list, query: str = ""):
        """
        beautiful soup 4를 이용하여 정적 웹페이지에 대한 크롤링을 시도합니다.
        셀렉터를 적용하여 입력한 셀렉터에 해당하는 태그 안의 contents를 로드합니다.

        :param url: 베이스 url
        :param selectors: 검색할 셀렉터
        :param query: 검색할 쿼리
        :return: 크롤링된 콘텐츠
        """

        html=requests.get('https://search.naver.com/search.naver?query='+query)
        soup= BeautifulSoup(html.text,'html.parser')
        out = self.__bs4(url, query)
        try:
            crawled = []
            for selector in selectors:
                if selector == '.temperature_text':
                    t0=soup.select('.temperature_text')[0]
                    t1 = soup.select('.cell_temperature')[1].contents[1]
                    t2 = soup.select('.cell_temperature')[2].contents[1]
                    crawled.append(t0.contents[1].contents[1])
                    crawled.append(t1.contents[1].contents[1])
                    crawled.append(t1.contents[5].contents[1])
                    crawled.append(t2.contents[1].contents[1])
                    crawled.append(t2.contents[5].contents[1])

                elif selector == '.inner > .list_box > .week_list':
                    w0 = soup.select('.weather.before_slash')[0]
                    w1 = soup.select('.cell_weather')[1]
                    w2 = soup.select('.cell_weather')[2]
                    #0오늘,1내일,2모레

                    crawled.append(w0.contents[0])
                    crawled.append(w1.contents[1].contents[3].contents[0].contents[0])
                    crawled.append(w1.contents[3].contents[3].contents[0].contents[0])
                    crawled.append(w2.contents[1].contents[3].contents[0].contents[0])
                    crawled.append(w2.contents[3].contents[3].contents[0].contents[0])

                else:
                    for s in out.select(selector):
                        crawled.append(s.contents)

            return crawled
        except Exception:
            return None

    def _bs4_content(self, url: str, query: str = ""):
        """
        beautiful soup 4를 이용하여 정적 웹페이지에 대한 크롤링을 시도합니다.
        셀렉터를 적용하여 입력한 셀렉터에 해당하는 태그 안의 contents를 로드합니다.

        :param url: 베이스 url
        :param selectors: 검색할 셀렉터
        :param query: 검색할 쿼리
        :return: 크롤링된 콘텐츠
        """
        req = requests.get(url + query)
        html = req.content.decode('utf-8', 'replace')
        soup = BeautifulSoup(html, 'html.parser')

        try:
            crawled = []
            t0 = soup.select('._3Apve')
            t1 = soup.select('._3hCbH')

            crawled.append(t0[0].contents[0])
            crawled.append(t1[0].contents[0])
            crawled.append(t0[1].contents[0])
            crawled.append(t1[1].contents[0])
            crawled.append(t0[2].contents[0])
            crawled.append(t1[2].contents[0])

            return crawled
        except Exception:
            return None


    def _bs4_documents(self, url: str, selectors: list, query: str = ""):
        """
        beautiful soup 4를 이용하여 정적 웹페이지에 대한 크롤링을 시도합니다.
        셀렉터를 적용하여 입력한 셀렉터에 해당하는 태그를 포함한 모든 document 구조를 로드합니다.

        :param url: 베이스 url
        :param selectors: 검색할 셀렉터
        :param query: 검색할 쿼리
        :return: 크롤링된 콘텐츠
        """

        out = self.__bs4(url, query)
        try:
            crawled = []
            for selector in selectors:
                for s in out.select(selector):
                    crawled.append(s)
            return crawled
        except Exception:
            return None

    def _json(self, url: str, query: str):
        """
        json을 이용하여 동적 웹페이지에 대한 크롤링을 시도합니다.

        :param url: 베이스 url
        :param query: 검색할 쿼리
        :return: 크롤링된 json 파일
        """

        if query:
            url += urllib.parse.quote(query)

        req = requests.get(url, headers=self.headers)
        if req.status_code == requests.codes.ok:
            loaded_data = json.loads(req.text)
            return loaded_data
        else:
            return None
