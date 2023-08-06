import datetime
import time

import pandas as pd
from loguru import logger

import ofanalysis.jiuquan.fund_info as fund_info
import ofanalysis.const as const
import ofanalysis.utility as ut


class FundRank:
    """
    基金相关排名
    从韭圈儿获取数据并原始存入mongodb->raw....
    构建实例的时候，传入六位基金代码将从数据库里面提取数据
        如果数据库里面没有该基金，则从韭圈儿上获取数据并存入数据库
        如果数据库里有该基金，则和当前运行日期比较，如果已经超过一个季度，则更新数据库
        如果传入参数force_update_db，则从韭圈儿上获取数据并存入数据库
    """

    def __init__(self, fund_code: str, cate_l2: str, force_update_db: bool = False):
        self.__v_init(fund_code, cate_l2)
        fund_category_list = fund_info.FundInfo(fund_code=fund_code).category  # 取回该基金的所属类别
        if self.cate_l2 not in fund_category_list:  # 判断给定类别是否在该基金的列表中
            logger.info('基金<%s>不具备<%s>类别；试试：%s' % (self.code, self.cate_l2, fund_category_list))
            raise Exception
        # 从db中获取数据
        item_list = ut.db_get_dict_from_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_RANK_RAW,
            query_dict={
                'fund_code': self.code,
                'cate_l2': self.cate_l2
            }
        )
        if len(item_list) != 4:  # 不存在数据，或者有冗余数据。先删除冗余数据，在插入新数据
            ut.db_del_dict_from_mongodb(
                mongo_db_name=const.MONGODB_DB_JIUQUAN,
                col_name=const.MONGODB_COL_JQ_FUND_RANK_RAW,
                query_dict={
                    'fund_code': self.code,
                    'cate_l2': self.cate_l2
                }
            )
            item_list = self.__save_fund_rank_raw_to_db(self.__retrieve_fund_rank_raw_from_jiuquan())
        else:
            item_raw = item_list[0]
            # 判断取回的4条记录是否retrieve_date相等，如果不等，删除重新取
            flag_retrieve_date_equal = True
            for item in item_list:
                if item['retrieve_date'] != item_raw['retrieve_date']:
                    flag_retrieve_date_equal = False
                    break
            existed_q = pd.Period(item_raw['retrieve_date'], 'Q')
            now_q = pd.Period(self.__today, 'Q')
            if (now_q > existed_q) or force_update_db or (
                    flag_retrieve_date_equal is False):  # 数据是上季度的，需要从韭圈儿更新，或者传入参数强制更新, 或者存量数据不一致
                ut.db_del_dict_from_mongodb(
                    mongo_db_name=const.MONGODB_DB_JIUQUAN,
                    col_name=const.MONGODB_COL_JQ_FUND_RANK_RAW,
                    query_dict={
                        'fund_code': self.code,
                        'cate_l2': self.cate_l2
                    }
                )
                item_list = self.__save_fund_rank_raw_to_db(self.__retrieve_fund_rank_raw_from_jiuquan())

        self.__populate_item_raw_to_object(item_list)

    def __v_init(self, fund_code: str, cate_l2: str, ):
        self.code = fund_code
        self.cate_l2 = cate_l2
        self.__today = datetime.date.today()

    def __retrieve_fund_rank_raw_from_jiuquan(self):
        sign_info = {
            1: '阶段涨幅',
            2: '季度涨幅',
            3: '年度涨幅',
            4: '基金大爆炸'
        }
        list_dict_fund_rank_raw = []
        for sign in range(1, 5):
            request_data = {
                "code": self.code,
                "sign": sign,
                "id": self.cate_l2,
                "name": self.cate_l2,
                # "data_source": "jq",  # 字段不同基金不一样，暂时注释，好像不影响
                "type": "pc",
                "version": "1.8.9",
                "authtoken": const.JIUQUAN_TOKEN,
                "act_time": int(round(time.time() * 1000))
            }
            dict_fund_rank_single_raw = ut.request_post_json(
                api_url='https://api.jiucaishuo.com/v2/fund-lists/fundachieve',
                headers=const.JIUQUAN_HEADER,
                request_param=request_data
            )
            if (dict_fund_rank_single_raw is None) or (len(dict_fund_rank_single_raw) == 0):
                logger.info('Get %s fund rank failed...' % self.code)
            dict_fund_rank_single_raw['rank_name'] = sign_info[sign]
            list_dict_fund_rank_raw.append(dict_fund_rank_single_raw)
        return list_dict_fund_rank_raw

    def __save_fund_rank_raw_to_db(self, list_dict_fund_rank_raw):
        '''
        在插入数据库之前，在传入的Dict中添加fund_code, cate_l2, retrieve_date字段
        :param dict_fund_rank_raw:
        :return:
        '''
        refined_list_dict_fund_rank_raw = []
        for dict_fund_rank_raw in list_dict_fund_rank_raw:
            dict_fund_rank_raw['fund_code'] = self.code
            dict_fund_rank_raw['cate_l2'] = self.cate_l2
            dict_fund_rank_raw['retrieve_date'] = self.__today.strftime('%Y%m%d')
            refined_list_dict_fund_rank_raw.append(dict_fund_rank_raw)

        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_RANK_RAW,
            target_dict=refined_list_dict_fund_rank_raw
        )
        return refined_list_dict_fund_rank_raw

    def __populate_item_raw_to_object(self, item_list):
        dict_raw = dict()
        for item in item_list:
            dict_raw[item['rank_name']] = item
        self.df_period_increase = pd.DataFrame(dict_raw['阶段涨幅']['sd_list'])
        self.df_quarter_increase = pd.DataFrame(dict_raw['季度涨幅']['sd_list'])
        self.df_year_increase = pd.DataFrame(dict_raw['年度涨幅']['sd_list'])
        self.df_dabaozha = pd.DataFrame(dict_raw['基金大爆炸']['sd_list'])
