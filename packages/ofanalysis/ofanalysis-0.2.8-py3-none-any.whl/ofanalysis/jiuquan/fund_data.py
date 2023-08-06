import datetime
import time

import pandas as pd
from loguru import logger

import ofanalysis.const as const
import ofanalysis.utility as ut


class FundData:
    """
    基金总结信息
    从韭圈儿获取数据并原始存入mongodb->raw....
    构建实例的时候，传入六位基金代码将从数据库里面提取数据
        如果数据库里面没有该基金，则从韭圈儿上获取数据并存入数据库
        如果数据库里有该基金，则和当前运行日期比较，如果已经超过一个季度，则更新数据库
        如果传入参数force_update_db，则从韭圈儿上获取数据并存入数据库
    """

    def __init__(self, fund_code: str, force_update_db: bool = False):
        self.__v_init(fund_code)

        # 从db中获取数据
        item_list = ut.db_get_dict_from_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_DATA_RAW,
            query_dict={
                'fund_code': self.code
            }
        )
        if len(item_list) != 1:  # 不存在数据，或者有冗余数据。先删除冗余数据，在插入新数据
            ut.db_del_dict_from_mongodb(
                mongo_db_name=const.MONGODB_DB_JIUQUAN,
                col_name=const.MONGODB_COL_JQ_FUND_DATA_RAW,
                query_dict={
                    'fund_code': self.code
                }
            )
            item_raw = self.__save_fund_data_raw_to_db(self.__retrieve_fund_data_raw_from_jiuquan())
        else:
            item_raw = item_list[0]
            existed_q = pd.Period(item_raw['retrieve_date'], 'Q')
            now_q = pd.Period(self.__today, 'Q')
            if (now_q > existed_q) or force_update_db:  # 数据是上季度的，需要从韭圈儿更新，或者传入参数强制更新
                ut.db_del_dict_from_mongodb(
                    mongo_db_name=const.MONGODB_DB_JIUQUAN,
                    col_name=const.MONGODB_COL_JQ_FUND_DATA_RAW,
                    query_dict={
                        'fund_code': self.code
                    }
                )
                item_raw = self.__save_fund_data_raw_to_db(self.__retrieve_fund_data_raw_from_jiuquan())

        self.__populate_item_raw_to_object(item_raw)

    def __v_init(self, fund_code: str):
        self.code = fund_code
        self.__today = datetime.date.today()

    def __retrieve_fund_data_raw_from_jiuquan(self):
        logger.info(f'Retrieving fund data from jiuquan for <{self.code}>')
        request_param = {
            "fund_code": self.code,
            "type": "pc",
            # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000)),
        }
        list_fund_data_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v2/fund-details/getdatas',
            headers=const.JIUQUAN_HEADER,
            request_param=request_param
        )
        if (list_fund_data_raw is None) or (len(list_fund_data_raw) == 0):
            logger.info('Get %s fund data failed...' % self.code)
        # 将返回的list列表，转换成dict
        dict_fund_data_raw = dict()
        for item in list_fund_data_raw:
            dict_fund_data_raw[item['name']] = item['tags']
        return dict_fund_data_raw

    def __save_fund_data_raw_to_db(self, dict_fund_data_raw):
        '''
        在插入数据库之前，在传入的Dict中添加fund_code, retrieve_date字段
        :param dict_fund_data_raw:
        :return:
        '''
        dict_fund_data_raw['fund_code'] = self.code
        dict_fund_data_raw['retrieve_date'] = self.__today.strftime('%Y%m%d')

        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_DATA_RAW,
            target_dict=dict_fund_data_raw
        )
        return dict_fund_data_raw

    def __populate_item_raw_to_object(self, item_raw):
        self.df_manager = pd.DataFrame(item_raw['基金经理'])
        if 'name' in self.df_manager.columns:
            self.df_manager = self.df_manager[['left_title', 'info', 'name']].rename(
                columns={'left_title': 'type', 'name': 'conclusion'})
        else:
            self.df_manager = self.df_manager[['left_title', 'info']].rename(columns={'left_title': 'type'})
        self.df_manager.insert(0, 'category', '基金经理')

        self.df_jingongli = pd.DataFrame(item_raw['进攻力'])
        if 'name' in self.df_jingongli.columns:
            self.df_jingongli = self.df_jingongli[['left_title', 'info', 'name']].rename(
                columns={'left_title': 'type', 'name': 'conclusion'})
        else:
            self.df_jingongli = self.df_jingongli[['left_title', 'info']].rename(columns={'left_title': 'type'})
        self.df_jingongli.insert(0, 'category', '进攻力')

        self.df_fangyuli = pd.DataFrame(item_raw['防御力'])
        if 'name' in self.df_fangyuli.columns:
            self.df_fangyuli = self.df_fangyuli[['left_title', 'info', 'name']].rename(
                columns={'left_title': 'type', 'name': 'conclusion'})
        else:
            self.df_fangyuli = self.df_fangyuli[['left_title', 'info']].rename(columns={'left_title': 'type'})
        self.df_fangyuli.insert(0, 'category', '防御力')

        self.df_holding_profile = pd.DataFrame(item_raw['持仓特征'])
        if 'name' in self.df_holding_profile.columns:
            self.df_holding_profile = self.df_holding_profile[['left_title', 'info', 'name']].rename(
                columns={'left_title': 'type', 'name': 'conclusion'})
        else:
            self.df_holding_profile = self.df_holding_profile[['left_title', 'info']].rename(
                columns={'left_title': 'type'})
        self.df_holding_profile.insert(0, 'category', '持仓特征')

        self.df_other_profile = pd.DataFrame(item_raw['其他特征'])
        if 'name' in self.df_other_profile.columns:
            self.df_other_profile = self.df_other_profile[['left_title', 'info', 'name']].rename(
                columns={'left_title': 'type', 'name': 'conclusion'})
        else:
            self.df_other_profile = self.df_other_profile[['left_title', 'info']].rename(columns={'left_title': 'type'})
        self.df_other_profile.insert(0, 'category', '其他特征')

        self.compound_data_df = pd.concat(
            [self.df_manager, self.df_jingongli, self.df_fangyuli, self.df_holding_profile, self.df_other_profile],
            axis=0,
            ignore_index=True
        )
