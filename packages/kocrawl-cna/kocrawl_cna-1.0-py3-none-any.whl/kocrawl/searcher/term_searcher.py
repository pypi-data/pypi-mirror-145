from kocrawl.searcher.base_searcher import BaseSearcher

class TermSearcher(BaseSearcher):
    def __init__(self):
        self.selectors = [[".info_area"], [".headword"], [".summary_area"]]

    def _make_query(self):
        return None

    def search_term(self, term: str) -> tuple:

        results = self._bs4_documents(
            url=self.url["naver_term"] + "search.naver?query=", selectors=self.selectors[0], query=term
        )

        # for result in results:
        #     tag = result.find('span',attrs={'class':'cite'}).text
        #     if('두산백과' in tag):

        url = self.url['naver_term'] + (results[0].find('a').get('href'))
        key = self._bs4_documents(url=url, selectors=self.selectors[1])
        result = self._bs4_documents(url=url, selectors=self.selectors[2])

        dictionary = {'term': key[0].getText(), 'meaning': result[0].getText()}

        if results.__len__() > 1:
            url = self.url['naver_term'] + (results[1].find('a').get('href'))
            key = self._bs4_documents(url=url, selectors=self.selectors[1])
            result = self._bs4_documents(url=url, selectors=self.selectors[2])

            dictionary['sim_term'] = key[0].getText()
            dictionary['sim_meaning'] = result[0].getText()

        return dictionary
