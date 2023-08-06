from unittest import TestCase

from ofanalysis.jiuquan.fund_info import FundInfo


class TestFundInfo(TestCase):
    def test_get_fund_info(self):
        fund_info_class = FundInfo(fund_code='001645', force_update_db=False)
        print()
