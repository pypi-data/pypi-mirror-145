
from kocrawl.searcher.base_searcher import BaseSearcher
import re


class RentSearcher(BaseSearcher):
    def __init__(self):

        self.data_dict = {
            # 데이터를 담을 딕셔너리 구조를 정의합니다.
            'near_name1': [] ,'near_address1': [],
            'near_name2': [] ,'near_address2': [],
            'near_name3': [], 'near_address3': []
        }

    def _make_query(self, location: str ,category: str) -> str:
        """
        검색할 쿼리를 만듭니다.
        :param location: 지역
        :param place: 장소
        :return: "지역 종류 장소"로 만들어진 쿼리
        """
        item =""
        if category in self.category['cycle']:
            category ="자전거"
            item = "대여소"
        elif category in self.category['car']:
            category ="전기차"
            item = "충전소"
        query = ' '.join([location, category, item])
        # 서울 강동구 자전거 대여소
        return query

    def search_naver_map(self, location: str, category: str) -> dict:
        """
        네이버를 이용해 날씨를 검색합니다.
        :param category:
        :param location: 지역
        :return: 크롤링된 내용
        """

        query = self._make_query(location, category)
        result = self._bs4_content(url=self.url['rent_map'],
                                   query=query)

        i = 0
        for k in self.data_dict.keys():
            self.data_dict[k] = re.sub(' ', '', result[i])
            i += 1

        return self.data_dict