import akshare as ak
import pandas as pd
from loguru import logger

import ofanalysis.const as const
import ofanalysis.utility as ut


class AKShareDataUpdate:
    def __init__(self):
        self.index_list = None

    def retrieve_index_value_hist(self):
        df_index_list = ak.index_value_name_funddb()
        df_index_value = pd.DataFrame()
        for index_name in df_index_list['指数名称']:
            for indicator in ['市盈率', '市净率', '股息率']:
                logger.info('retrieve %s value of %s...' % (indicator, index_name))
                index_value_hist_funddb_df = ak.index_value_hist_funddb(symbol=index_name, indicator=indicator)
                index_value_hist_funddb_df.insert(0, '指数名称', index_name)
                index_value_hist_funddb_df.insert(
                    0,
                    '指数代码',
                    df_index_list.loc[df_index_list['指数名称'] == index_name, '指数代码'].iloc[0])
                df_index_value = pd.concat([df_index_value, index_value_hist_funddb_df], axis=0)
        df_index_value['日期'] = pd.to_datetime(df_index_value['日期']).map(lambda x: x.strftime('%Y%m%d'))
        ut.db_del_dict_from_mongodb(  # 非增量更新 先清空数据
            mongo_db_name=const.MONGODB_DB_TKSHARE,
            col_name=const.MONGODB_COL_TKS_INDEX_GUZHI,
            query_dict={}
        )
        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_TKSHARE,
            col_name=const.MONGODB_COL_TKS_INDEX_GUZHI,
            target_dict=df_index_value.to_dict(orient='records')
        )

    def retrieve_fund_rating_summary(self):
        fund_rating_all_df = ak.fund_rating_all()
        ut.db_del_dict_from_mongodb(  # 非增量更新 先清空数据
            mongo_db_name=const.MONGODB_DB_TKSHARE,
            col_name=const.MONGODB_COL_TKS_FUND_RATING,
            query_dict={}
        )
        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_TKSHARE,
            col_name=const.MONGODB_COL_TKS_FUND_RATING,
            target_dict=fund_rating_all_df.to_dict(orient='records')
        )
