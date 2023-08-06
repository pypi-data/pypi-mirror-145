import datetime
import time

import pandas as pd
from loguru import logger

import ofanalysis.const as const
import ofanalysis.utility as ut


class FundVest:
    """
    基金持仓信息
    从韭圈儿获取数据并原始存入mongodb->raw....
    构建实例的时候，传入六位基金代码将从数据库里面提取数据
        如果数据库里面没有该基金，则从韭圈儿上获取数据并存入数据库
        如果数据库里有该基金，则和当前运行日期比较，如果已经超过一个季度，则更新数据库
        如果传入参数force_update_db，则从韭圈儿上获取数据并存入数据库
        参数：cate_source: 'sw_category'-申万 / 'zz_category'-中证 / 'wind_category'-万得
        参数：date 季度最后一天，例如：20211231。如果传入的日期不是季度最后一天，则自动转换成最后一天
    """

    def __init__(self, fund_code: str, cate_source: str, date: str, force_update_db: bool = False):
        self.__v_init(fund_code, date, cate_source)

        # 从db中获取数据
        item_list = ut.db_get_dict_from_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_VEST_RAW,
            query_dict={
                'fund_code': self.code,
                'cate_source': self.cate_source,
                'date': self.date
            }
        )
        if len(item_list) != 1:  # 不存在数据，或者有冗余数据。先删除冗余数据，在插入新数据
            ut.db_del_dict_from_mongodb(
                mongo_db_name=const.MONGODB_DB_JIUQUAN,
                col_name=const.MONGODB_COL_JQ_FUND_VEST_RAW,
                query_dict={
                    'fund_code': self.code,
                    'cate_source': self.cate_source,
                    'date': self.date
                }
            )
            item_raw = self.__save_fund_vest_raw_to_db(self.__retrieve_fund_vest_raw_from_jiuquan())
        else:
            item_raw = item_list[0]
            existed_q = pd.Period(item_raw['retrieve_date'], 'Q')
            now_q = pd.Period(self.__today, 'Q')
            if (now_q > existed_q) or force_update_db:  # 数据是上季度的，需要从韭圈儿更新，或者传入参数强制更新
                ut.db_del_dict_from_mongodb(
                    mongo_db_name=const.MONGODB_DB_JIUQUAN,
                    col_name=const.MONGODB_COL_JQ_FUND_VEST_RAW,
                    query_dict={
                        'fund_code': self.code,
                        'cate_source': self.cate_source,
                        'date': self.date
                    }
                )
                item_raw = self.__save_fund_vest_raw_to_db(self.__retrieve_fund_vest_raw_from_jiuquan())

        self.__populate_item_raw_to_object(item_raw)

    def __v_init(self, fund_code: str, date: str, cate_source: str):
        self.code = fund_code
        self.date = ut.get_q_end(date)
        self.cate_source = cate_source
        self.__today = datetime.date.today()

    def __retrieve_fund_vest_raw_from_jiuquan(self):
        logger.info('retrieving <%s><%s><%s> fund vest from Jiuquan...' % (self.code, self.cate_source, self.date))
        request_param = {
            "code": self.code,
            "category": self.cate_source,
            'date': self.date,
            "type": "pc",
            # "data_source": "xichou",  # 字段不同基金不一样，暂时注释，好像不影响
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000)),
        }
        dict_fund_vest_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v2/fund-lists/fundinvest',
            headers=const.JIUQUAN_HEADER,
            request_param=request_param
        )
        if (dict_fund_vest_raw is None) or (len(dict_fund_vest_raw) == 0):
            logger.info('Get %s fund vest failed...' % self.code)

        return dict_fund_vest_raw

    def __save_fund_vest_raw_to_db(self, dict_fund_vest_raw):
        '''
        在插入数据库之前，在传入的Dict中添加fund_code, retrieve_date, date, cate_source字段
        :param dict_fund_vest_raw:
        :return:
        '''
        dict_fund_vest_raw['fund_code'] = self.code
        dict_fund_vest_raw['retrieve_date'] = self.__today.strftime('%Y%m%d')
        dict_fund_vest_raw['cate_source'] = self.cate_source
        dict_fund_vest_raw['date'] = self.date

        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_JIUQUAN,
            col_name=const.MONGODB_COL_JQ_FUND_VEST_RAW,
            target_dict=dict_fund_vest_raw
        )
        return dict_fund_vest_raw

    def __populate_item_raw_to_object(self, item_raw):
        self.gp = GP(item_raw['gp'], self.date)
        self.zq = ZQ(item_raw['zq'])
        self.zc = ZC(item_raw['zc'])
        self.jj = JJ(item_raw['jj'])
        self.hy = HY(item_raw['hy'])
        self.all_period_list = item_raw['total_time']

    def retrieve_all_period_and_category_from_jiuquan(self):
        for period in self.all_period_list:
            for cate_source in ['sw_category', 'zz_category', 'wind_category']:
                FundVest(fund_code=self.code, cate_source=cate_source, date=period)
                time.sleep(1)


class GP:
    def __init__(self, gp_dict: dict, period_date):
        self.desc = gp_dict['desc']
        self.perect = gp_dict['perect']
        self.time = gp_dict['time']
        if len(gp_dict['avg']) != 0:
            self.pe_avg = gp_dict['avg']['pe_avg']
            self.pb_avg = gp_dict['avg']['pb_avg']
            self.roe_avg = gp_dict['avg']['roe_avg']
            self.shizhi_avg = gp_dict['avg']['shizhi_avg']
        # self.df_holding = pd.DataFrame(gp_dict['list'])
        self.__period_date = period_date
        if len(gp_dict['list']) != 0:
            self.df_holding = self.__get_stock_increase(pd.DataFrame(gp_dict['list']))

    def __get_stock_increase(self, holding_df):
        """
        将韭圈儿持仓数据，加上对应下一个季度持仓股票的涨跌幅 <- 数据源为tushare db
        :param holding_df:
        :return: 组装好的df
        """
        start_date = self.__period_date
        end_date = ut.get_q_end(
            (pd.to_datetime(start_date) + datetime.timedelta(days=1)).strftime('%Y%m%d')
        )
        holding_df.insert(13, 'cq+1 % increase', 0.0)
        for code in holding_df['code']:
            ts_code_list = ut.db_get_dict_from_mongodb(  # 通过code获取ts_code
                mongo_db_name=const.MONGODB_DB_TUSHARE,
                col_name=const.MONGODB_COL_TS_STOCK_BASIC,
                query_dict={
                    'symbol': code
                }
            )
            if len(ts_code_list) != 1:
                continue
            ts_code = ts_code_list[0]['ts_code']
            stock_price_list = ut.db_get_dict_from_mongodb(
                mongo_db_name=const.MONGODB_DB_TUSHARE,
                col_name=const.MONGODB_COL_TS_STOCK_DAILY,
                query_dict={
                    'ts_code': ts_code,
                    'trade_date': {
                        '$gte': start_date,
                        '$lte': end_date
                    }
                }
            )
            stock_price_df = pd.DataFrame(stock_price_list).sort_values(by='trade_date', ascending=False)
            end_price = stock_price_df.loc[0, 'close']
            start_price = stock_price_df.loc[(len(stock_price_df) - 2), 'open']
            increase = (end_price - start_price) / start_price * 100
            holding_df.loc[holding_df['code'] == code, 'cq+1 % increase'] = increase
        holding_df = ut.convert_float_for_dataframe_columns(holding_df, ['cq+1 % increase'], 2, False)
        return holding_df


class ZQ:
    def __init__(self, zq_dict: dict):
        self.perect = zq_dict['perect']
        self.time = zq_dict['time']
        self.df_holding = pd.DataFrame(zq_dict['list'])


class ZC:
    def __init__(self, zc_dict: dict):
        try:
            self.desc = zc_dict['desc']
            self.df_holding = pd.DataFrame(zc_dict['series'])[['name', 'data']]
        except Exception:
            logger.warning(f'No data of ZC')
        else:
            pass


class JJ:
    def __init__(self, jj_dict: dict):
        self.perect = jj_dict['perect']
        self.time = jj_dict['time']
        self.df_holding = pd.DataFrame(jj_dict['list'])


class HY:
    def __init__(self, hy_dict: dict):
        try:
            self.df_holding = pd.DataFrame(hy_dict['series'])[['name', 'data']]
        except Exception:
            logger.warning('No data of HY')
        else:
            pass


class FG:
    def __init__(self, fg_dict: dict):
        self.time = fg_dict['update_time']
        self.desc = fg_dict['desc']
        self.df_holding = pd.DataFrame(fg_dict['series'])[['name', 'data']]
