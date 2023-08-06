import datetime

import pandas as pd
from loguru import logger

import ofanalysis.const as const
import ofanalysis.utility as ut


class LixingrenSWData:
    """
    实例化对象时，根据传入的code处理数据，看看是否需要更新等，确保数据库数据为最新
    数据更新频率为一周已更新，由于接口调用次数限制。如果今天日期和db中最新日期差异小于一月，则不更新
    实例化对象时，传入参数start_date和end_date，格式均为YYYYMMDD。会在init中load到变量-> self.__dict_data_raw
    实例化对象后，数据存储在self.data_dict中，通过data_dict[date][type][granularity][metricsType][indicator]来获取数据
        * type(pe-pe_ttm, pb-pb, 收盘点-cp)
        * granularity(所有-fs / 10年-y10 / 5年-5)
        * metricsType(市值加权-mcw / 市值加权-mcw / 等权-ew / 正数等权-ewpvo / 平均值-avg / 中位数-median)
        * indicator(cv-当前值 cvpos-当前分位点 minv-最小值 maxv-最大值 maxpv-最大正值 avgv-平均值)
        * indicator(q5v-50%分位点 q8v-80%分位点 q2v-20%分位点)
    """

    def __init__(self, lxr_token:str, code: str, start_date: str = None, end_date: str = None, force_update_db: bool = False):
        self.__v_init(lxr_token=lxr_token, code=code, start_date=start_date, end_date=end_date)
        # 从db中取回现有日期
        item_list = ut.db_get_distinct_from_mongodb(
            mongo_db_name=const.MONGODB_DB_LXR,
            col_name=const.MONGODB_COL_LXR_SW_IND,
            field='date',
            query_dict={
                'stockCode': self.code
            }
        )
        if (len(item_list) == 0) or force_update_db:  # 需要从API获取至db
            logger.info('选择强制更新或者mongodb中不存在code：%s数据，需要从lxr全量获取...' % self.code)
            ut.db_del_dict_from_mongodb(
                mongo_db_name=const.MONGODB_DB_LXR,
                col_name=const.MONGODB_COL_LXR_SW_IND,
                query_dict={
                    'stockCode': self.code
                })
            self.__dict_data_raw = self.__save_sw_data_to_db(self.__retrieve_sw_data())  # 重新获取
        else:  # 存在数据，需要比较当前日期和最新日期，确定是否需要更新以及更新范围
            date_list = item_list
            date_list.sort(reverse=True)
            existed_latest_date = date_list[0]
            existed_period = pd.Period(existed_latest_date, 'M')
            today_period = pd.Period(self.__today_date, 'M')
            if today_period > existed_period:  # 差异超过周期，更新数据！
                start_date = pd.to_datetime(existed_latest_date) + datetime.timedelta(days=1)
                logger.info('code：%s数据存在，db中最新日期是%s，增量更新....' % (self.code, existed_latest_date))
                self.__save_sw_data_to_db(self.__retrieve_sw_data(start_date=start_date.strftime('%Y-%m-%d')))
            else:
                logger.info('code：%s数据存在，db中最新日期是%s，无需更新....' % (self.code, existed_latest_date))
        self.__populate_item_raw_to_object()

    def __v_init(self, lxr_token:str, code: str, start_date: str = None, end_date: str = None):
        self.lxr_token = lxr_token
        self.code = code
        self.name = ''
        self.start_date = start_date
        self.end_date = end_date
        self.__today_date = datetime.date.today()
        self.__dict_data_raw = None
        self.data_dict = {}
        self.__field_params = [
            "cp",
            "pe_ttm.mcw", "pe_ttm.ew", "pe_ttm.ewpvo", "pe_ttm.avg", "pe_ttm.median",
            "pb.mcw", "pb.ew", "pb.ewpvo", "pb.avg", "pb.median",
            "pe_ttm.fs.mcw", "pe_ttm.fs.ew", "pe_ttm.fs.ewpvo", "pe_ttm.fs.avg", "pe_ttm.fs.median",
            "pb.fs.mcw", "pb.fs.ew", "pb.fs.ewpvo", "pb.fs.avg", "pb.fs.median",
            "pe_ttm.y10.mcw", "pe_ttm.y10.ew", "pe_ttm.y10.ewpvo", "pe_ttm.y10.avg", "pe_ttm.y10.median",
            "pb.y10.mcw", "pb.y10.ew", "pb.y10.ewpvo", "pb.y10.avg", "pb.y10.median",
            "pe_ttm.y5.mcw", "pe_ttm.y5.ew", "pe_ttm.y5.ewpvo", "pe_ttm.y5.avg", "pe_ttm.y5.median",
            "pb.y5.mcw", "pb.y5.ew", "pb.y5.ewpvo", "pb.y5.avg", "pb.y5.median",
        ]

    def __retrieve_sw_data(self, start_date: str = '2000-01-01'):
        logger.info(
            "retrieving sw data for %s - from <%s> to <%s>" % (
                self.code, start_date, self.__today_date.strftime("%Y-%m-%d")))
        request_params = {
            "token": self.lxr_token,
            "startDate": start_date,
            "endDate": self.__today_date.strftime("%Y-%m-%d"),
            "stockCodes": [self.code],
            "metricsList": self.__field_params
        }
        dict_sw = ut.request_post_json(
            api_url='https://open.lixinger.com/api/cn/industry/fundamental/sw_2021',
            headers=const.LIXINGREN_HEADER,
            request_param=request_params
        )
        return dict_sw

    def __save_sw_data_to_db(self, dict_sw_data):
        for item in dict_sw_data:  # 修改日期格式为YYYYMMDD
            item['date'] = pd.to_datetime(item['date']).strftime('%Y%m%d')
        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_LXR,
            col_name=const.MONGODB_COL_LXR_SW_IND,
            target_dict=dict_sw_data
        )
        return dict_sw_data

    def __populate_item_raw_to_object(self):
        self.name = const.PARAMS['lxr_sw_l1_ind'][self.code]
        if self.end_date is None:
            self.end_date = self.__today_date.strftime('%Y%m%d')
        if self.start_date is None:
            self.start_date = '20000101'
        if self.__dict_data_raw is None:  # 从db中获取相应数据
            self.__dict_data_raw = ut.db_get_dict_from_mongodb(
                mongo_db_name=const.MONGODB_DB_LXR,
                col_name=const.MONGODB_COL_LXR_SW_IND,
                query_dict={
                    'stockCode': self.code,
                    "date": {
                        "$gte": self.start_date,
                        '$lte': self.end_date,
                    }
                },
            )
        else:
            self.__dict_data_raw = [x for x in self.__dict_data_raw if (self.start_date <= x['date'] <= self.end_date)]
        for day_item in self.__dict_data_raw:
            self.data_dict[day_item['date']] = day_item
        self.date_list = [x['date'] for x in self.__dict_data_raw]

    def build_sw_ind_df(self, type: str, granularity: str, metrics_type: str):
        dt = {}
        for date in self.date_list:
            dt[date] = {
                '%s' % type: self.data_dict[date][type][granularity][metrics_type]['cv'],
                '%s当前分位点' % type: self.data_dict[date][type][granularity][metrics_type]['cvpos'],
                '80%分位点': self.data_dict[date][type][granularity][metrics_type]['q8v'],
                '50%分位点': self.data_dict[date][type][granularity][metrics_type]['q5v'],
                '20%分位点': self.data_dict[date][type][granularity][metrics_type]['q2v'],
            }
        result_df = pd.DataFrame(dt).T
        result_df.sort_index(inplace=True)
        return result_df
