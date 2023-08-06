import datetime
import time

import pandas as pd
from loguru import logger

import ofanalysis.const as const
import ofanalysis.utility as ut


class FundManager:
    """
    基金经理信息
    从韭圈儿获取数据并原始存入mongodb->raw....
    构建实例的时候，传入基金经理id，将从数据库里面提取数据
        如果数据库里面没有该经理数据，则从韭圈儿上获取数据并存入数据库
        如果数据库里有该基金，则和当前运行日期比较，如果已经超过一个季度，则更新数据库
        如果传入参数force_update_db，则从韭圈儿上获取数据并存入数据库
    """

    def __init__(self, manager_id: str, force_update_db: bool = False):
        self.__v_init(manager_id)

        # 从db中获取数据
        item_list = ut.db_get_dict_from_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_MANAGER_RAW,
            query_dict={
                'manager_id': self.manager_id
            }
        )
        if len(item_list) != 1:  # 不存在数据，或者有冗余数据。先删除冗余数据，在插入新数据
            ut.db_del_dict_from_mongodb(
                mongo_db_name=const.MONGODB_DB_JIUQUAN,
                col_name=const.MONGODB_COL_JQ_FUND_MANAGER_RAW,
                query_dict={
                    'manager_id': self.manager_id
                }
            )
            item_raw = self.__save_fund_manager_raw_to_db(self.__retrieve_fund_manager_raw_from_jiuquan())
        else:
            item_raw = item_list[0]
            existed_q = pd.Period(item_raw['retrieve_date'], 'Q')
            now_q = pd.Period(self.__today, 'Q')
            if (now_q > existed_q) or force_update_db:  # 数据是上季度的，需要从韭圈儿更新，或者传入参数强制更新
                ut.db_del_dict_from_mongodb(
                    mongo_db_name=const.MONGODB_DB_JIUQUAN,
                    col_name=const.MONGODB_COL_JQ_FUND_MANAGER_RAW,
                    query_dict={
                        'manager_id': self.manager_id
                    }
                )
                item_raw = self.__save_fund_manager_raw_to_db(self.__retrieve_fund_manager_raw_from_jiuquan())

        self.__populate_item_raw_to_object(item_raw)

    def __v_init(self, manager_id):
        self.manager_id = manager_id
        self.__today = datetime.date.today()
        self.personal_detail = PersonalDetail(self.manager_id)
        self.total_stock_holding = TotalStockHolding(self.manager_id)
        self.managed_fund = ManagedFund(self.manager_id)
        self.managed_fund_prize = ManagedFundPrize(self.manager_id)
        self.jiuquan_score = JiuquanScore(self.manager_id)
        self.indicator = Indicator(self.manager_id)

    def __retrieve_fund_manager_raw_from_jiuquan(self):
        logger.info(f'Retrieve fund manager for <{self.manager_id}>')
        # 分别从韭圈儿获取数据
        self.personal_detail.retrieve_data_from_jiuquan()
        self.total_stock_holding.retrieve_data_from_jiuquan()
        self.managed_fund.retrieve_data_from_jiuquan()
        self.jiuquan_score.retrieve_data_from_jiuquan(self.personal_detail.manager_tag_list)
        self.managed_fund_prize.retrieve_data_from_jiuquan()
        self.indicator.retrieve_data_from_jiuquan(self.personal_detail.manager_name,
                                                  self.personal_detail.manager_tag_list)

        dict_fund_manager_raw = dict()
        dict_fund_manager_raw['personal_detail'] = self.personal_detail.dict_raw
        dict_fund_manager_raw['total_stock_holding'] = self.total_stock_holding.dict_raw
        dict_fund_manager_raw['managed_fund'] = self.managed_fund.dict_raw
        dict_fund_manager_raw['jiuquan_score'] = self.jiuquan_score.dict_raw
        dict_fund_manager_raw['managed_fund_prize'] = self.managed_fund_prize.dict_raw
        dict_fund_manager_raw['indicator'] = self.indicator.dict_raw

        return dict_fund_manager_raw

    def __save_fund_manager_raw_to_db(self, dict_fund_manager_raw):
        '''
        在插入数据库之前，在传入的Dict中添加manager_id, manager_name, retrieve_date字段
        :param dict_fund_manager_raw:
        :return:
        '''
        dict_fund_manager_raw['manager_id'] = self.manager_id
        dict_fund_manager_raw['manager_name'] = self.personal_detail.manager_name
        dict_fund_manager_raw['retrieve_date'] = self.__today.strftime('%Y%m%d')

        if dict_fund_manager_raw['manager_name'] == '':
            logger.warning('基金经理{x}数据取回有误！'.format(x=dict_fund_manager_raw['manager_id']))
            return dict_fund_manager_raw

        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_MANAGER_RAW,
            target_dict=dict_fund_manager_raw
        )
        return dict_fund_manager_raw

    def __populate_item_raw_to_object(self, item_raw):
        self.manager_name = item_raw['manager_name']
        self.personal_detail.populate_item_raw_to_object(item_raw['personal_detail'])
        self.total_stock_holding.populate_item_raw_to_object(item_raw['total_stock_holding'])
        self.managed_fund.populate_item_raw_to_object(item_raw['managed_fund'])
        self.managed_fund_prize.populate_item_raw_to_object(item_raw['managed_fund_prize'])
        self.jiuquan_score.populate_item_raw_to_object(item_raw['jiuquan_score'])
        self.indicator.populate_item_raw_to_object(item_raw['indicator'])


class PersonalDetail:
    def __init__(self, manager_id: str):
        self.resume = None
        self.manager_tag_list = None
        self.manager_name = None
        self.dict_raw = None
        self.market_view_point = None
        self.position_duration = None
        self.managed_fund_size = None
        self.represent_product = None
        self.fund_num = None
        self.main_tag = None
        self.company = None
        self.score = None
        self.annual_return = None
        self.df_ob_prize = None
        self.manager_id = manager_id

    def retrieve_data_from_jiuquan(self):
        request_param = {
            "id": self.manager_id,
            "type": "pc",
            "category": "dl",
            # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000)),
        }
        dict_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v2/personlists/persondetail',
            headers=const.JIUQUAN_HEADER,
            request_param=request_param
        )
        if (dict_raw is None) or (len(dict_raw) == 0):
            logger.info('Get %s personal data failed...' % self.manager_id)
        self.manager_tag_list = dict_raw['line_tags']  # 由于jiuquan_score类要用到此字段，先提取存储
        self.manager_name = dict_raw['name']
        self.dict_raw = dict_raw

    def populate_item_raw_to_object(self, item_raw):
        self.resume = item_raw['resume']
        self.market_view_point = item_raw['marketViewPoint']
        self.position_duration = item_raw['positionDuration']
        self.managed_fund_size = item_raw['newlatestFundScale']
        self.represent_product = item_raw['representProduct']
        self.fund_num = item_raw['fundNum']
        self.main_tag = item_raw['string_tags']
        self.company = item_raw['company']
        self.score = item_raw['mark']
        self.annual_return = item_raw['avgYearReturn1']
        self.df_ob_prize = pd.DataFrame(item_raw['ob_price'])
        self.manager_tag_list = item_raw['line_tags']


class TotalStockHolding:
    def __init__(self, manager_id: str):
        self.df_total_holding = None
        self.bg_time = None
        self.df_avg_attribute = None
        self.dict_raw = None
        self.manager_id = manager_id

    def retrieve_data_from_jiuquan(self):
        request_param = {
            "id": self.manager_id,
            "type": "pc",
            "category": "dl",
            # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000)),
        }
        dict_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v2/mogul/mogul-info',
            headers=const.JIUQUAN_HEADER,
            request_param=request_param
        )
        if (dict_raw is None) or (len(dict_raw) == 0):
            logger.info('Get %s total stock holding failed...' % self.manager_id)

        self.dict_raw = dict_raw

    def populate_item_raw_to_object(self, item_raw):
        self.bg_time = item_raw['bg_time']
        self.df_avg_attribute = pd.DataFrame(item_raw['avg_arr'])
        column_list = []
        for item in item_raw['position_th']:
            if 'desc' not in item.keys():
                column_list.append(item['name'])
            else:
                column_list.append('%s(%s)' % (item['name'], item['desc']))
        df_total_holding = pd.DataFrame(columns=column_list)
        for item in item_raw['position_table_data']:
            data_list = [x['val'] for x in item['list']]
            data_list.insert(0, item['name'])
            df_total_holding.loc[item_raw['position_table_data'].index(item)] = data_list
        self.df_total_holding = df_total_holding


class ManagedFundPrize:
    def __init__(self, manager_id: str):
        self.dict_raw = None
        self.df_managed_fund_prize = None
        self.manager_id = manager_id

    def retrieve_data_from_jiuquan(self):
        request_param = {
            "id": self.manager_id,
            "type": "pc",
            "category": "dl",
            # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000)),
        }
        dict_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v2/personlists/getprice',
            headers=const.JIUQUAN_HEADER,
            request_param=request_param
        )
        if (dict_raw is None) or (len(dict_raw) == 0):
            logger.info('Get %s managed fund prize failed...' % self.manager_id)

        self.dict_raw = dict_raw

    def populate_item_raw_to_object(self, item_raw):
        if len(item_raw) > 0:
            self.df_managed_fund_prize = pd.DataFrame(item_raw)[['fund_name', 'date', 'desc']]


class ManagedFund:
    def __init__(self, manager_id: str):
        self.update_time = None
        self.df_now_managed = None
        self.df_history_managed = None
        self.dict_raw = None
        self.manager_id = manager_id

    def retrieve_data_from_jiuquan(self):
        request_param = {
            "id": self.manager_id,
            "type": "pc",
            "category": "dl",
            # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000)),
        }
        dict_now_managing_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v2/personlists/getnowfund',
            headers=const.JIUQUAN_HEADER,
            request_param=request_param
        )
        if (dict_now_managing_raw is None) or (len(dict_now_managing_raw) == 0):
            logger.info('Get %s managed fund failed...' % self.manager_id)
        self.dict_raw = dict_now_managing_raw

    def populate_item_raw_to_object(self, item_raw):
        self.update_time = item_raw['update_time']
        column_list = []
        for item in item_raw['menu']:
            if 'desc' not in item.keys():
                column_list.append(item['name'])
            else:
                column_list.append('%s(%s)' % (item['name'], item['desc']))
        df_now_managed = pd.DataFrame(columns=column_list)
        df_history_managed = pd.DataFrame(columns=column_list)
        for item in item_raw['now_list']:
            data_list = [x['val'] for x in item['list']]
            data_list.insert(0, item['name'])
            df_now_managed.loc[item_raw['now_list'].index(item)] = data_list
        self.df_now_managed = df_now_managed

        for item in item_raw['history_list']:
            data_list = [x['val'] for x in item['list']]
            data_list.insert(0, item['name'])
            df_history_managed.loc[item_raw['history_list'].index(item)] = data_list
        self.df_history_managed = df_history_managed


class JiuquanScore:
    def __init__(self, manager_id: str):
        self.dict_raw = None
        self.dict_cate_score = None
        self.manager_id = manager_id

    def retrieve_data_from_jiuquan(self, manager_tag_list: list):
        dict_consolidated_raw = dict()
        for manager_tag in manager_tag_list:
            request_param = {
                "id": self.manager_id,
                "type": "pc",
                "category": "dl",
                "category_name": manager_tag['name'],
                "classify_code": manager_tag['classify_code'],
                # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
                "version": "1.8.9",
                "authtoken": const.JIUQUAN_TOKEN,
                "act_time": int(round(time.time() * 1000)),
            }
            dict_raw = ut.request_post_json(
                api_url='https://api.jiucaishuo.com/v2/personlists/zw',
                headers=const.JIUQUAN_HEADER,
                request_param=request_param
            )
            if (dict_raw is None) or (len(dict_raw) == 0):
                logger.info('Get %s jiuquan score failed...' % self.manager_id)
            dict_consolidated_raw[manager_tag['name']] = dict_raw

        self.dict_raw = dict_consolidated_raw

    def populate_item_raw_to_object(self, item_raw):
        self.dict_cate_score = dict()
        for key in item_raw.keys():
            column_list = item_raw[key]['categories']
            if len(column_list) == 0:  # 有些基金数据不全导致exception
                return
            column_list.insert(0, 'who')
            df = pd.DataFrame(columns=column_list)
            for item in item_raw[key]['series']:
                item['data'].insert(0, item['name'])
                df.loc[item_raw[key]['series'].index(item)] = item['data']
            self.dict_cate_score[key] = df


class Indicator:
    def __init__(self, manager_id: str):
        self.draw_back = {}
        self.dabaozha = {}
        self.income = {}
        self.dict_raw = {}
        self.manager_id = manager_id

    def retrieve_data_from_jiuquan(self, manager_name: str, manager_tag_list: list, benchmark: str = '000300.SH'):
        for manager_tag in manager_tag_list:
            self.dict_raw[manager_tag['name']] = {}
            # 取经理曲线
            personline_request_param = {
                "id": self.manager_id,
                "person_name": manager_name,
                "category_name": manager_tag['name'],
                "ben": benchmark,
                "type": "pc",
                "category": "dl",
                # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
                "version": "1.8.9",
                "authtoken": const.JIUQUAN_TOKEN,
                "act_time": int(round(time.time() * 1000)),
            }
            personline_dict_raw = ut.request_post_json(
                api_url='https://api.jiucaishuo.com/v2/personlists/personline',
                headers=const.JIUQUAN_HEADER,
                request_param=personline_request_param
            )

            # 取大爆炸曲线
            dabaozha_request_param = {
                "id": self.manager_id,
                # "person_name": manager_name,
                "category_name": manager_tag['name'],
                "category_code": manager_tag['classify_code'],
                "ben": benchmark,
                "type": "pc",
                "category": "dl",
                # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
                "version": "1.8.9",
                "authtoken": const.JIUQUAN_TOKEN,
                "act_time": int(round(time.time() * 1000)),
            }
            dabaozha_dict_raw = ut.request_post_json(
                api_url='https://api.jiucaishuo.com/v2/personlists/bigdata',
                headers=const.JIUQUAN_HEADER,
                request_param=dabaozha_request_param
            )

            # 取回撤数据
            drawback_request_param = {
                "id": self.manager_id,
                # "person_name": manager_name,
                "category_name": manager_tag['name'],
                "category_code": manager_tag['classify_code'],
                "ben": benchmark,
                "type": "pc",
                "category": "dl",
                # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
                "version": "1.8.9",
                "authtoken": const.JIUQUAN_TOKEN,
                "act_time": int(round(time.time() * 1000)),
            }
            drawback_dict_raw = ut.request_post_json(
                api_url='https://api.jiucaishuo.com/v2/personlists/personhcline',
                headers=const.JIUQUAN_HEADER,
                request_param=drawback_request_param
            )
            self.dict_raw[manager_tag['name']]['personline'] = personline_dict_raw
            self.dict_raw[manager_tag['name']]['dabaozha'] = dabaozha_dict_raw
            self.dict_raw[manager_tag['name']]['drawback'] = drawback_dict_raw

    def populate_item_raw_to_object(self, item_raw):
        for key in item_raw.keys():
            income_line_data_df = pd.DataFrame()
            for item_data in item_raw[key]['personline']['series']:
                temp_df = pd.DataFrame(
                    item_data["data"], columns=["日期", item_data['name']]
                )
                temp_df["日期"] = pd.to_datetime(temp_df["日期"], unit="ms", utc=True).dt.tz_convert(
                    "Asia/Shanghai").dt.date
                temp_df["日期"] = temp_df["日期"].apply(lambda x: x.strftime('%Y%m%d'))
                temp_df.set_index(["日期"], inplace=True)
                income_line_data_df = pd.concat([income_line_data_df, temp_df], axis=1)
            income_line_data_df.sort_index(inplace=True)
            self.income[key] = income_line_data_df

            dabaozha_line_data_df = pd.DataFrame()
            for item_data in item_raw[key]['dabaozha']['series'].values():
                temp_df = pd.DataFrame(
                    item_data["data"], columns=["日期", item_data['name']]
                )
                temp_df["日期"] = pd.to_datetime(temp_df["日期"], unit="ms", utc=True).dt.tz_convert(
                    "Asia/Shanghai").dt.date
                temp_df["日期"] = temp_df["日期"].apply(lambda x: x.strftime('%Y%m%d'))
                temp_df.set_index(["日期"], inplace=True)
                dabaozha_line_data_df = dabaozha_line_data_df.loc[~dabaozha_line_data_df.index.duplicated(keep='first')]
                temp_df = temp_df.loc[~temp_df.index.duplicated(keep='first')]
                dabaozha_line_data_df = pd.concat([dabaozha_line_data_df, temp_df], axis=1)
            dabaozha_line_data_df.sort_index(inplace=True)
            self.dabaozha[key] = dabaozha_line_data_df

            draw_back_line_data_df = pd.DataFrame()
            for item_data in item_raw[key]['drawback']['hc_series']:
                temp_df = pd.DataFrame(
                    item_data["data"], columns=["日期", item_data['name']]
                )
                temp_df["日期"] = pd.to_datetime(temp_df["日期"], unit="ms", utc=True).dt.tz_convert(
                    "Asia/Shanghai").dt.date
                temp_df["日期"] = temp_df["日期"].apply(lambda x: x.strftime('%Y%m%d'))
                temp_df.set_index(["日期"], inplace=True)
                draw_back_line_data_df = pd.concat([draw_back_line_data_df, temp_df], axis=1)
            draw_back_line_data_df.sort_index(inplace=True)
            self.draw_back[key] = draw_back_line_data_df
