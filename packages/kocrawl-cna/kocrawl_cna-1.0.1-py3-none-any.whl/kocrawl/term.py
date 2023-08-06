
from kocrawl.answerer.term_answerer import TermAnswerer
from kocrawl.base import BaseCrawler
from kocrawl.editor.term_editor import TermEditor
from kocrawl.searcher.term_searcher import TermSearcher


class TermCrawler(BaseCrawler):

    def request(self, eco: str) -> str:

        try:
            return self.request_debug(eco)[0]
        except Exception:
            return TermAnswerer().sorry(
                "해당 단어에 대한 정보가 없어요."
            )

    def request_dict(self, eco: str):

        try:
            return self.request_debug(eco)[1]
        except Exception:
            return TermAnswerer().sorry(
                "해당 단어에 대한 정보가 없어요."
            )

    def request_debug(self, eco: str):

        result_dict = TermSearcher().search_term(eco)
        result_dict = TermEditor().edit_term(result_dict)
        result = TermAnswerer().term_form(result_dict)
        return result, result_dict
