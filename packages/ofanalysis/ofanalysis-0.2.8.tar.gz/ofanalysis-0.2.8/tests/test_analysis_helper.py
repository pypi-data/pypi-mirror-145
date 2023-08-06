from unittest import TestCase
from ofanalysis import analysis_helper


class TestFundManagerRankAnalysis(TestCase):
    def setUp(self) -> None:
        self.analysis_helper = analysis_helper.FundManagerRankAnalysis()

    def test_jiuquan_retrieve_all_funds_with_type(self):
        # self.analysis_helper.jiuquan_retrieve_all_funds_with_type()
        pass

    def test_get_profit_and_rank_from_db(self):
        self.analysis_helper.get_profit_and_rank_from_db()
        pass
