from unittest import TestCase

from ofanalysis.jiuquan.fund_rank import FundRank


class TestFundRank(TestCase):
    def test_get_fund_rank(self):
        fund_rank_object = FundRank(
            fund_code='001171',
            cate_l2='消费'
        )
        print()
