from kocrawl.term import TermCrawler
from unittest import TestCase


class MapTest(TestCase):

    def test(self):
        crawler = TermCrawler()
        output = crawler.request_debug("ESG")
        self.assertIsInstance(output, tuple)
        print(output)
