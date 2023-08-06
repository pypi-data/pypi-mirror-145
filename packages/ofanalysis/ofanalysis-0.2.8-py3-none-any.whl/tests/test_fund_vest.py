from unittest import TestCase

from ofanalysis.jiuquan.fund_vest import FundVest


class TestFundVest(TestCase):
    def setUp(self) -> None:
        self.fund_vest_object = FundVest(fund_code='519195',
                                                   date='20210930',
                                                   cate_source='sw_category',
                                                   force_update_db=False)
        print()

    def test_retrieve_all_period_and_category_from_jiuquan(self):
        # self.fund_vest_object.retrieve_all_period_and_category_from_jiuquan()
        pass
