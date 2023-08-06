from unittest import TestCase
from ofanalysis.jiuquan.fund_data import FundData


class TestFundData(TestCase):
    def test_get_fund_data(self):
        fund_data_class = FundData(fund_code='001645', force_update_db=False)
        print()
