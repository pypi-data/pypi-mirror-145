from kocrawl.answerer.rent_answerer import RentAnswerer
from kocrawl.base import BaseCrawler
from kocrawl.editor.rent_editor import RentEditor
from kocrawl.searcher.rent_searcher import RentSearcher


class RentCrawler(BaseCrawler):
    def request(self, location: str, category: str) -> str:
        """
        지도를 크롤링합니다.
        (try-catch로 에러가 나지 않는 함수)
        :param location: 지역
        :param place: 장소
        :return: 해당지역 장소
        """

        try:
            return self.request_debug(location, category)[0]
        except Exception:
            return RentAnswerer().sorry(
                "해당 지역은 알 수 없습니다."
            )

    def request_dict(self, location: str, category: str ):
        """
        지도를 크롤링합니다.
        (try-catch로 에러가 나지 않는 함수)
        :param location: 지역
        :param category: 자전거 or 전기자동차
        :return: 해당지역 장소
        """

        try:
            return self.request_debug(location, category)[1]
        except Exception:
            return RentAnswerer().sorry(
                "해당 지역은 알 수 없습니다."
            )

    def request_debug(self, location: str, category: str):
        """
        :param location: 지역
        :param category: 자전거 or 전기차
        :return: 만들어진진 문장
        """
        result_dict = RentSearcher().search_naver_map(location, category)
        result = RentEditor().edit_rent(location, category,  result_dict)
        result = RentAnswerer().rent_form(location, category, result)
        return result, result_dict