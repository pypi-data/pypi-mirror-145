from unittest import TestCase

from ofanalysis.jiuquan.fund_rank_list import FundRankList
import ofanalysis.utility as ut


class TestFundRankList(TestCase):
    def setUp(self) -> None:
        self.fund_rank_list_object = FundRankList(
            type_name='收益率排名',
            cate_l1='行业赛道',
            cate_l2='医药生物',
            retrieve_type_cate_md=False
        )
        print()

    def test_format_rank_list(self):
        result2 = ut.get_numeric_df_by_column(
            self.fund_rank_list_object.df_rank_list, ignore_column_list=['基金名称', '基金代码'])
        print()

    def test_retrieve_all_fund_rank_list(self):
        self.fund_rank_list_object.retrieve_all_fund_rank_list()
        print()
