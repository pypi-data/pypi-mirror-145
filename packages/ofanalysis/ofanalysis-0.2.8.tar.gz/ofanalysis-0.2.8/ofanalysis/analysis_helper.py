import pandas as pd
from loguru import logger

from ofanalysis import const
import ofanalysis.utility as ut
from ofanalysis.jiuquan.fund_info import FundInfo
from ofanalysis.jiuquan.fund_manager import FundManager
from ofanalysis.jiuquan.fund_rank_list import FundRankList


class FundManagerRankAnalysis:
    """
    用于分析对象为基金经理的排名分析
    """

    def jiuquan_retrieve_all_funds_with_type(self):
        """
        从韭圈儿上取回所有《韭圈分类》为《权益型》的基金，获取每一个基金的基金经理，获取每个基金经理的净值数据
        存入mongodb数据库《MONGODB_DB_ANALYSIS_HELP》表《MONGODB_COL_ANALYSIS_HELP_MANAGER_ANALYSIS》中
        每次调用本方法，将清空数据库记录，重新写入新下载的数据
        :return:
        """
        fund_list = FundRankList(
            type_name='收益率排名',
            cate_l1='韭圈分类',
            cate_l2='权益型',
        )
        result_df = pd.DataFrame()
        for fund_code in fund_list.df_rank_list['基金代码']:
            logger.info(f'Processing <{fund_code}> ...')
            fund_info = FundInfo(fund_code)
            if not fund_info.manager_id:
                logger.info(f'<{fund_info.name}> manager is empty!')
                continue
            for id in fund_info.manager_id.split(','):
                fund_manager = FundManager(id)
            df = fund_manager.indicator.income['权益型'].drop(columns='沪深300', axis=1)
            result_df = pd.concat([df, result_df], axis=1)
        result_df = result_df.T.drop_duplicates().T
        result_df.sort_index(inplace=True)
        result_df.reset_index(inplace=True)
        # result_df.to_csv('./mgr_select.csv', index=True)
        ut.db_del_dict_from_mongodb(  # 非增量更新 先清空数据
            mongo_db_name=const.MONGODB_DB_ANALYSIS_HELP,
            col_name=const.MONGODB_COL_ANALYSIS_HELP_MANAGER_ANALYSIS,
            query_dict={}
        )
        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_ANALYSIS_HELP,
            col_name=const.MONGODB_COL_ANALYSIS_HELP_MANAGER_ANALYSIS,
            target_dict=result_df.to_dict(orient='records')
        )

    def get_profit_and_rank_from_db(self) -> (pd.DataFrame, pd.DataFrame):
        """
        从mongodb数据库《MONGODB_DB_ANALYSIS_HELP》表《MONGODB_COL_ANALYSIS_HELP_MANAGER_ANALYSIS》中
        获取基金经理净值数据，从2018年Q1开始，到2022年Q1，计算每个基金经理每个Q的净值增长情况，生成《profit_df》
        根据每个Q净值增长情况，生成每个Q的排名，生成《rank_df》
        :return: profit_df, rank_df
        """
        existed_records = ut.db_get_dict_from_mongodb(
            mongo_db_name=const.MONGODB_DB_ANALYSIS_HELP,
            col_name=const.MONGODB_COL_ANALYSIS_HELP_MANAGER_ANALYSIS,
        )
        period_dict = {
            '2018Q1': {
                'start': '20180101',
                'end': '20180331'
            },
            '2018Q2': {
                'start': '20180401',
                'end': '20180630'
            },
            '2018Q3': {
                'start': '20180701',
                'end': '20180930'
            },
            '2018Q4': {
                'start': '20181001',
                'end': '20181231'
            },
            '2019Q1': {
                'start': '20190101',
                'end': '20190331'
            },
            '2019Q2': {
                'start': '20190401',
                'end': '20190630'
            },
            '2019Q3': {
                'start': '20190701',
                'end': '20190930'
            },
            '2019Q4': {
                'start': '20191001',
                'end': '20191231'
            },
            '2020Q1': {
                'start': '20200101',
                'end': '20200331'
            },
            '2020Q2': {
                'start': '20200401',
                'end': '20200630'
            },
            '2020Q3': {
                'start': '20200701',
                'end': '20200930'
            },
            '2020Q4': {
                'start': '20201001',
                'end': '20201231'
            },
            '2021Q1': {
                'start': '20210101',
                'end': '20210331'
            },
            '2021Q2': {
                'start': '20210401',
                'end': '20210630'
            },
            '2021Q3': {
                'start': '20210701',
                'end': '20210930'
            },
            '2021Q4': {
                'start': '20211001',
                'end': '20211231'
            },
            '2022Q1': {
                'start': '20220101',
                'end': '20220331'
            },
        }
        df = pd.DataFrame(existed_records)
        df.set_index(['日期'], inplace=True)
        result_dict = {}
        for period in period_dict.keys():
            period_df = df.loc[period_dict[period]['start']: period_dict[period]['end'], ]
            period_profit = (period_df.iloc[-1] - period_df.iloc[0]) / period_df.iloc[0]
            result_dict[period] = period_profit
        profit_df = pd.DataFrame(result_dict).dropna(how='all')
        rank_dict = {}
        for name, columns in profit_df.items():
            rank_dict[name] = columns.rank(method='average')
        rank_df = pd.DataFrame(rank_dict)
        return profit_df, rank_df
