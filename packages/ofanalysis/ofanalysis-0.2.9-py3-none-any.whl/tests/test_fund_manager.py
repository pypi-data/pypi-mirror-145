from unittest import TestCase

from ofanalysis.jiuquan.fund_manager import FundManager


class TestFundManager(TestCase):
    def test_fund_manger(self):
        fund_manager_object = FundManager(
            manager_id='3030343335'
        )
        print()
