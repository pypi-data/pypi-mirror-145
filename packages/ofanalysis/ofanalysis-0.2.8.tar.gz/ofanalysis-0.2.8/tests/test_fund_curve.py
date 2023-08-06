from unittest import TestCase
from ofanalysis.jiuquan.fund_curve import FundCurve


class TestFundCurve(TestCase):
    def setUp(self) -> None:
        self.fund_curve_object = FundCurve(code='001645')
        print()

    def test_retrieve_fund_curve_and_populate(self):
        self.fund_curve_object.retrieve_fund_curve_and_populate(

        )
        print()

    def test_retrieve_dabaozha_curve_and_populate(self):
        self.fund_curve_object.retrieve_dabaozha_curve_and_populate()
        print()

    def test_retrieve_draw_back_curve_and_populate(self):
        self.fund_curve_object.retrieve_draw_back_curve_and_populate(benchmark='000905.SH')
        print()
