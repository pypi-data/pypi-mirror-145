import datetime
import time

import pandas as pd
from loguru import logger

import ofanalysis.const as const
import ofanalysis.utility as ut


class FundInfo:
    """
    基金基础信息
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
            col_name=const.MONGODB_COL_JQ_FUND_INFO_RAW,
            query_dict={
                'fund_code': self.code
            }
        )
        if len(item_list) != 1:  # 不存在数据，或者有冗余数据。先删除冗余数据，在插入新数据
            ut.db_del_dict_from_mongodb(
                mongo_db_name=const.MONGODB_DB_JIUQUAN,
                col_name=const.MONGODB_COL_JQ_FUND_INFO_RAW,
                query_dict={
                    'fund_code': self.code
                }
            )
            item_raw = self.__save_fund_info_raw_to_db(self.__retrieve_fund_info_raw_from_jiuquan())
        else:
            item_raw = item_list[0]
            existed_q = pd.Period(item_raw['retrieve_date'], 'Q')
            now_q = pd.Period(self.__today, 'Q')
            if (now_q > existed_q) or force_update_db:  # 数据是上季度的，需要从韭圈儿更新，或者传入参数强制更新
                ut.db_del_dict_from_mongodb(
                    mongo_db_name=const.MONGODB_DB_JIUQUAN,
                    col_name=const.MONGODB_COL_JQ_FUND_INFO_RAW,
                    query_dict={
                        'fund_code': self.code
                    }
                )
                item_raw = self.__save_fund_info_raw_to_db(self.__retrieve_fund_info_raw_from_jiuquan())

        self.__populate_item_raw_to_object(item_raw)

    def __v_init(self, fund_code: str):
        self.code = fund_code
        self.__today = datetime.date.today()

    def __retrieve_fund_info_raw_from_jiuquan(self):
        logger.info(f'Retrieving fund info from jiuquan for <{self.code}>')
        request_param = {
            "code": self.code,
            "type": "pc",
            # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000)),
        }
        dict_fund_info_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v3/pc-fundlists/fundinfo',
            headers=const.JIUQUAN_HEADER,
            request_param=request_param
        )
        if (dict_fund_info_raw is None) or (len(dict_fund_info_raw) == 0):
            logger.info('Get %s fund info failed...' % self.code)

        return dict_fund_info_raw

    def __save_fund_info_raw_to_db(self, dict_fund_info_raw):
        '''
        在插入数据库之前，在传入的Dict中添加fund_code, retrieve_date字段
        :param dict_fund_info_raw:
        :return:
        '''
        dict_fund_info_raw['fund_code'] = self.code
        dict_fund_info_raw['retrieve_date'] = self.__today.strftime('%Y%m%d')

        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_INFO_RAW,
            target_dict=dict_fund_info_raw
        )
        return dict_fund_info_raw

    def __populate_item_raw_to_object(self, item_raw):
        self.category = [x['label'] for x in item_raw['keywor']]
        self.name = item_raw['name']

        data_dict = dict()
        for item in item_raw['list']:
            data_dict[item['label']] = item['value']
            if item['label'] == '基金经理':
                data_dict['基金经理id'] = item['id']

        self.type = data_dict['基金类型']
        self.total_size = data_dict['合并规模']
        self.latest_size = data_dict['最新规模']
        self.start_from = data_dict['成立日期']
        self.trade_limit = data_dict['交易限额']
        self.risk_level = data_dict['风险等级']
        self.index_type = data_dict['指数类型']
        self.manager = data_dict['基金经理']
        self.manager_id = data_dict['基金经理id']
        self.manager_level = data_dict['经理等级']
        self.manager_pk = data_dict['经理PK']
        self.fund_pk = data_dict['基金PK']
