from kocrawl.answerer.rent_answerer import RentAnswerer
from kocrawl.base import BaseCrawler
from kocrawl.editor.rent_editor import RentEditor
from kocrawl.searcher.rent_searcher import RentSearcher


class RentCrawler(BaseCrawler):
    def request(self, location: str, kinds: str, item: str) -> str:
        """
        지도를 크롤링합니다.
        (try-catch로 에러가 나지 않는 함수)

        :param location: 지역
        :param place: 장소
        :return: 해당지역 장소
        """

        try:
            return self.request_debug(location, kinds, item)[0]
        except Exception:
            return RentAnswerer().sorry(
                "해당 지역은 알 수 없습니다."
            )

    def request_dict(self, location: str, kinds: str, item: str):
        """
        지도를 크롤링합니다.
        (try-catch로 에러가 나지 않는 함수)

        :param location: 지역
        :param place: 장소
        :return: 해당지역 장소
        """

        try:
            return self.request_debug(location, kinds, item)[1]
        except Exception:
            return RentAnswerer().sorry(
                "해당 지역은 알 수 없습니다."
            )

    def request_debug(self, location: str, kinds: str, item: str):
        """
        :param location: 지역
        :param kinds: 자전거 or 전기차
        :param item: 충전소, 대여, 등등의 키워드
        :return: 만들어진진 문장
        """
        result_dict = RentSearcher().search_naver_map(location, kinds, item)
        result = RentEditor().edit_rent(location, kinds, item, result_dict)
        result = RentAnswerer().rent_form(location, kinds, item, result)
        return result, result_dict
