from kocrawl.rent import RentCrawler
from unittest import TestCase


class RentTest(TestCase):

    def test(self):
        crawler = RentCrawler()

        output = crawler.request_debug("서울 성동구","전기차")
        self.assertIsInstance(output, tuple)
        print(output)