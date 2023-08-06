"""
@auther Youngeun
@since {4/4/2022}
@see : https://github.com/choyoungeun/kocrawl
"""
from kocrawl.answerer.eco_answerer import EcoAnswerer
from kocrawl.base import BaseCrawler
from kocrawl.searcher.eco_searcher import EcoSearcher

class EcoCrawler(BaseCrawler):

    def request(self, category: str) -> str:

        try:
            return self.request_debug(category)
        except Exception:
            return EcoAnswerer().sorry(
                "해당 활동에 대해서 알려드릴 정보가 없어요."
            )
    def request_debug(self, category: str):

        result_dict = EcoSearcher().search_eco_act(category)
        result = EcoAnswerer().eco_form(result_dict)
        return result, result_dict