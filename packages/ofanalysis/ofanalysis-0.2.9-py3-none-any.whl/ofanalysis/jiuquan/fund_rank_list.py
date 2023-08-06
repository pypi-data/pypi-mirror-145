import datetime
import time

import pandas as pd
from loguru import logger

import ofanalysis.const as const
import ofanalysis.utility as ut


class FundRankList:
    """
    基金不同分配排行榜
    从韭圈儿获取数据并原始存入mongodb->raw....
    构建实例的时候，相应的参数，具体见__init__方法说明
        如果数据库里面没有该排名，则从韭圈儿上获取数据并存入数据库
        如果数据库里有该排名，则和当前运行日期比较，如果已经超过一个季度，则更新数据库
        如果传入参数force_update_db，则从韭圈儿上获取数据并存入数据库
    """

    def __init__(self, type_name: str, cate_l1: str = None,
                 cate_l2: str = None, force_update_db: bool = False, retrieve_type_cate_md: bool = False):
        '''
        :param type_name: 排名名称，可以从fundb.cn基金排名获取，或者从__retrieve_fund_rank_list_metadata()获取
        :param cate_l1: 分类1，可以从fundb.cn基金排名获取，或者从__retrieve_fund_rank_list_metadata()获取，cate_id：999 获取所有
        :param cate_l2: 分类2，可以从fundb.cn基金排名获取，或者从__retrieve_fund_rank_list_metadata()获取，cate_id：999 获取所有
        :param force_update_db:
        '''
        self.__retrieve_fund_rank_list_metadata(retrieve_type_cate_md)
        self.__v_init(type_name=type_name, cate_l1=cate_l1, cate_l2=cate_l2)
        # 从db中获取数据
        item_list = ut.db_get_dict_from_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_RANK_LIST_RAW,
            query_dict={
                'type_name': self.type_name,
                'cate_l1': self.cate_l1,
                'cate_l2': self.cate_l2
            }
        )
        if len(item_list) != 1:  # 不存在数据，或者有冗余数据。先删除冗余数据，在插入新数据
            ut.db_del_dict_from_mongodb(
                mongo_db_name=const.MONGODB_DB_JIUQUAN,
                col_name=const.MONGODB_COL_JQ_FUND_RANK_LIST_RAW,
                query_dict={
                    'type_name': self.type_name,
                    'cate_l1': self.cate_l1,
                    'cate_l2': self.cate_l2
                }
            )
            item_raw = self.__save_fund_rank_list_raw_to_db(self.__retrieve_fund_rank_list_raw_from_jiuquan())
        else:
            item_raw = item_list[0]
            existed_q = pd.Period(item_raw['retrieve_date'], 'Q')
            now_q = pd.Period(self.__today, 'Q')
            if (now_q > existed_q) or force_update_db:  # 数据是上季度的，需要从韭圈儿更新，或者传入参数强制更新
                ut.db_del_dict_from_mongodb(
                    mongo_db_name=const.MONGODB_DB_JIUQUAN,
                    col_name=const.MONGODB_COL_JQ_FUND_RANK_LIST_RAW,
                    query_dict={
                        'type_name': self.type_name,
                        'cate_l1': self.cate_l1,
                        'cate_l2': self.cate_l2
                    }
                )
                item_raw = self.__save_fund_rank_list_raw_to_db(self.__retrieve_fund_rank_list_raw_from_jiuquan())

        self.__populate_item_raw_to_object(item_raw)

    def __v_init(self, type_name: str, cate_l1: str = None, cate_l2: str = None):
        self.type_name = type_name
        self.__type_id = self.__dict_type[type_name]['type_id']
        self.__type_filed = self.__dict_type[type_name]['filed']
        self.__type_default_source = self.__dict_type[type_name]['default_source']
        if cate_l1 or cate_l2:
            self.cate_l1 = cate_l1
            self.cate_l2 = cate_l2
            self.__cate_id = self.__dict_cate[cate_l1][cate_l2]['cate_id']
        else:  # 默认为全部
            self.cate_l1 = '全部'
            self.cate_l2 = '全部'
            self.__cate_id = '-999'

        self.__today = datetime.date.today()

    def __retrieve_fund_rank_list_metadata(self, retrieve_online: bool = False):
        """
        从韭圈中获排行榜列表；分类列表
        :return:
        """
        if retrieve_online:
            data_type = {
                "type": "pc",
                # "data_source": "xichou",
                "version": "1.8.9",
                "authtoken": const.JIUQUAN_TOKEN,
                "act_time": int(round(time.time() * 1000))
            }

            data_cate = {
                "type": "pc",
                # "data_source": "xichou",
                # "version": "1.8.9",
                "authtoken": const.JIUQUAN_TOKEN,
                "act_time": int(round(time.time() * 1000)),
            }

            dict_rank_list_type_raw = ut.request_post_json(
                api_url='https://api.jiucaishuo.com/v2/fund-lists/getallfundrank',
                headers=const.JIUQUAN_HEADER,
                request_param=data_type
            )
            dict_rank_list_cate_raw = ut.request_post_json(
                api_url='https://api.jiucaishuo.com/v2/fund-lists/fundcate',
                headers=const.JIUQUAN_HEADER,
                request_param=data_cate
            )

            dict_cate = dict()
            dict_type = dict()
            for type_raw_item in dict_rank_list_type_raw:
                dict_type[type_raw_item['name']] = {
                    'type_id': type_raw_item['id'],
                    'desc': type_raw_item['desc'],
                    'filed': type_raw_item['filed'],
                    'default_source': type_raw_item['default_source'],
                    'column_list': [x['name'] for x in type_raw_item['lists']]
                }

            cate_raw = dict_rank_list_cate_raw['new_cate_sec']  # 经过研究，当前20220203，cate_raw的new_cate_sec里是最新分类方法，包括自带层级
            for cate_raw_item in cate_raw:
                dict_cate[cate_raw_item['type_name']] = dict()
                for child_cate_item in cate_raw_item['child']:
                    dict_cate[cate_raw_item['type_name']][child_cate_item['type_name']] = {
                        'cate_id': child_cate_item['id'],
                    }

            jiuquan_cate_raw = dict_rank_list_cate_raw['xc_cate_fir']
            dict_cate['韭圈分类'] = dict()
            for jiuquan_cate_dict in jiuquan_cate_raw:
                if int(jiuquan_cate_dict['parent_id']) == 0:
                    dict_cate['韭圈分类'][jiuquan_cate_dict['type_name']] = {
                        'cate_id': jiuquan_cate_dict['id'],
                    }


            ut.db_del_dict_from_mongodb(  # 清空数据
                mongo_db_name=const.MONGODB_DB_JIUQUAN,
                col_name=const.MONGODB_COL_JQ_FUND_TYPE_CATE_MD,
                query_dict={}
            )
            dict_type['md_name'] = 'type'
            dict_cate['md_name'] = 'cate'
            ut.db_save_dict_to_mongodb(
                mongo_db_name=const.MONGODB_DB_JIUQUAN,
                col_name=const.MONGODB_COL_JQ_FUND_TYPE_CATE_MD,
                target_dict=[dict_type, dict_cate]
            )
        else:
            result_list = ut.db_get_dict_from_mongodb(
                mongo_db_name=const.MONGODB_DB_JIUQUAN,
                col_name=const.MONGODB_COL_JQ_FUND_TYPE_CATE_MD,
                query_dict={}
            )
            for item in result_list:
                if item['md_name'] == 'type':
                    dict_type = item
                elif item['md_name'] == 'cate':
                    dict_cate = item
        self.__dict_type = dict_type
        self.__dict_cate = dict_cate

    def __retrieve_fund_rank_list_raw_from_jiuquan(self):
        logger.info('retrieving <%s><%s><%s> rank list from Jiuquan...' % (self.type_name, self.cate_l1, self.cate_l2))
        request_data = {
            "cate_id": self.__cate_id,
            "type_id": self.__type_id,
            "filed": self.__type_filed,
            "page": 1,
            "page_size": 20000,
            "data_source": 'xichou' if self.cate_l1=='韭圈分类' else 'jq',  # 韭圈分类是xichou，其他的是jq
            "type": "pc",
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000)),
        }
        dict_fund_rank_list_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v2/fund-lists/fundpcrank',
            headers=const.JIUQUAN_HEADER,
            request_param=request_data
        )
        if (dict_fund_rank_list_raw is None) or (len(dict_fund_rank_list_raw) == 0):
            logger.info('Get fund rank<%s><%s><%s> list failed...' % (self.type_name, self.cate_l1, self.cate_l2))

        return dict_fund_rank_list_raw

    def __save_fund_rank_list_raw_to_db(self, dict_fund_rank_list_raw: dict):
        '''
        在插入数据库之前，在传入的Dict中添加type_name, cate_l1, cate_l2, column_list, retrieve_date字段
        :param dict_fund_rank_list_raw:
        :return:
        '''
        dict_fund_rank_list_raw['type_name'] = self.type_name
        dict_fund_rank_list_raw['cate_l1'] = self.cate_l1
        dict_fund_rank_list_raw['cate_l2'] = self.cate_l2
        dict_fund_rank_list_raw['column_list'] = self.__dict_type[self.type_name]['column_list']
        dict_fund_rank_list_raw['retrieve_date'] = self.__today.strftime('%Y%m%d')

        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_RANK_LIST_RAW,
            target_dict=dict_fund_rank_list_raw
        )
        return dict_fund_rank_list_raw

    def __populate_item_raw_to_object(self, item_raw):
        df_list = []
        for info in item_raw['list']:
            src = {}
            name = info['name']
            src[item_raw['column_list'][0]] = name
            src['基金代码'] = info['code']
            a_lists = info['list']
            for i in range(len(item_raw['column_list'][1:])):
                value = str(a_lists[i])
                src[item_raw['column_list'][i + 1]] = value
            df_list.append(src)
        self.df_rank_list = pd.DataFrame(df_list)
        self.df_numeric_rank_list = ut.get_numeric_df_by_column(
            target_df=self.df_rank_list,
            ignore_column_list=['基金名称', '基金代码']
        )
        self.all_ranking_type = list(self.__dict_type.keys())
        self.all_ranking_type.remove('md_name')

    def retrieve_all_fund_rank_list(self):
        for rank_type in self.__dict_type.keys():
            if rank_type == 'md_name':
                continue
            for cate_l1 in self.__dict_cate.keys():
                if cate_l1 == '全部' or cate_l1 == 'md_name':
                    continue
                for cate_l2 in self.__dict_cate[cate_l1].keys():
                    FundRankList(
                        type_name=rank_type,
                        cate_l1=cate_l1,
                        cate_l2=cate_l2
                    )
                    # time.sleep(1)
            FundRankList(type_name=rank_type)
