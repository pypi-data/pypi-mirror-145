import time

import pandas as pd

import ofanalysis.const as const
import ofanalysis.utility as ut
from ofanalysis.jiuquan.fund_info import FundInfo


class FundCurve:
    def __init__(self, code: str):
        '''
        获取基金相关曲线
        :param code: 六位基金代码
        '''
        self.__dict_draw_back_curve_raw = None
        self.__dict_dabaozha_curve_raw = None
        self.__dict_fund_curve_raw = None
        self.code = code
        self.name = FundInfo(self.code)

        self.retrieve_fund_curve_and_populate()  # 首次执行默认查询并填充对象
        self.retrieve_dabaozha_curve_and_populate()  # 首次执行默认查询并填充对象
        self.retrieve_draw_back_curve_and_populate()  # 首次执行默认查询并填充对象

    def retrieve_fund_curve_and_populate(self, only_chao_e: int = 0, benchmark: str = '',
                                         search_fund_code: str = '', month_period: int = 1000,
                                         only_now_manager: int = 0, start_date: str = ''):
        '''
        从韭圈儿获取基金曲线数据，以方便图形展示
        :param start_date: 六位开始时间代码 YYYYMMDD
        :param only_chao_e: 0或者1，是否只看超额
        :param benchmark: 对标标的 - 在返回数据中字段'ben'里面获取全集，例如'000300.SH'
        :param search_fund_code: 对标标的 - 不在返回数据中字段'ben'里面，六位代码
        :param month_period: 获取近几月的数据，单位是月
        :param only_now_manager: 是否只返回当前基金经理任职时间段的数据
        :return:
        '''
        if start_date != '':
            start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d'),
        request_param = {
            "cl_flag": only_chao_e,  # 是否只看超额
            "ben": benchmark,  # 对标标的 - 在返回数据中字段'ben'里面
            "search_fund_code": search_fund_code,  # 对标标的 - 不在返回数据中字段'ben'里面
            "code": self.code,  # 基金代码
            # "fund_day": year_period * 12,  # 查看周期，单位是月
            "fund_day": month_period,
            "fund_person": only_now_manager,  # 是否只看当前基金经理
            "start_time": start_date,  # 自定义开始时间
            "update_time": "",
            "type": "pc",
            # "data_source": "xichou",
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000))
        }
        dict_fund_curve_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v2/fund-lists/fundcurve',
            headers=const.JIUQUAN_HEADER,
            request_param=request_param
        )
        self.__dict_fund_curve_raw = dict_fund_curve_raw
        self.__populate_fund_curve_raw_to_object(dict_fund_curve_raw)

    def __populate_fund_curve_raw_to_object(self, dict_fund_curve_raw):
        self.fund_total_income = dict_fund_curve_raw['fund_info']['fund_income']['number']
        self.fund_year_income = dict_fund_curve_raw['fund_info']['year_income']['number']
        self.fund_benchmark_df = pd.DataFrame(dict_fund_curve_raw['ben'])
        self.start_date = dict_fund_curve_raw['start_time']
        self.update_time = dict_fund_curve_raw['update_time']

        line_data_df = pd.DataFrame()
        temp_df = pd.DataFrame(
            dict_fund_curve_raw["line_list"]["series"][0]["data"], columns=["timestamp", "value"]
        )
        line_data_df["日期"] = (
            pd.to_datetime(temp_df["timestamp"], unit="s", utc=True)
                .dt.tz_convert("Asia/Shanghai")
                .dt.date
        )
        line_data_df["日期"] = line_data_df["日期"].apply(lambda x: x.strftime('%Y%m%d'))

        for item_data in dict_fund_curve_raw["line_list"]["series"]:
            line_data_df[item_data["name"]] = pd.to_numeric(
                [item[1] for item in item_data["data"]]
            )
        line_data_df.set_index(["日期"], inplace=True)
        line_data_df.sort_index(inplace=True)
        self.fund_income_data_df = line_data_df

    def retrieve_dabaozha_curve_and_populate(self, benchmark: str = '', only_now_manager: int = 0):
        '''
        从韭圈儿获取基金大爆炸曲线数据，以方便图形展示
        :param benchmark: 对标标的 - 在返回数据中字段'ben'里面获取全集，例如'000300.SH'
        :param only_now_manager: 是否只返回当前基金经理任职时间段的数据
        :return:
        '''
        request_param = {
            "ben": benchmark,  # 对标标的 - 在返回数据中字段'ben'里面
            "code": self.code,  # 基金代码
            "fund_person": only_now_manager,  # 是否只看当前基金经理
            "type": "pc",
            # "data_source": "xichou",
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000))
        }
        dict_dabaozha_curve_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v2/fund-lists/bigdata',
            headers=const.JIUQUAN_HEADER,
            request_param=request_param
        )
        self.__dict_dabaozha_curve_raw = dict_dabaozha_curve_raw
        self.__populate_dabaozha_curve_raw_to_object(dict_dabaozha_curve_raw)

    def __populate_dabaozha_curve_raw_to_object(self, dict_dabaozha_curve_raw):
        line_data_df = pd.DataFrame()
        for item_data in dict_dabaozha_curve_raw["series"]:
            temp_df = pd.DataFrame(
                item_data["data"], columns=["日期", item_data['name']]
            )
            temp_df["日期"] = pd.to_datetime(temp_df["日期"], unit="s", utc=True).dt.tz_convert("Asia/Shanghai").dt.date
            temp_df["日期"] = temp_df["日期"].apply(lambda x: x.strftime('%Y%m%d'))
            temp_df.set_index(["日期"], inplace=True)
            line_data_df = pd.concat([line_data_df, temp_df], axis=1)
        line_data_df.sort_index(inplace=True)
        self.fund_dabaozha_data_df = line_data_df

    def retrieve_draw_back_curve_and_populate(self, benchmark: str = '-99999', month_period: int = 1000,
                                              only_now_manager: int = 0, start_date: str = ''):
        '''
        从韭圈儿获取基金曲线数据，以方便图形展示
        :param start_date: 六位开始时间代码 YYYYMMDD
        :param benchmark: 对标标的 - 在返回数据中字段'ben'里面获取全集，例如'000300.SH'
        :param month_period: 获取近几月的数据，单位是月
        :param only_now_manager: 是否只返回当前基金经理任职时间段的数据
        :return:
        '''
        if start_date != '':
            start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d'),
        request_param = {
            "ben": benchmark,  # 对标标的 - 在返回数据中字段'ben'里面
            "code": self.code,  # 基金代码
            "fund_day": month_period,
            "fund_person": only_now_manager,  # 是否只看当前基金经理
            "start_time": start_date,  # 自定义开始时间
            "update_time": "",
            "type": "pc",
            # "data_source": "xichou",
            "version": "1.8.9",
            "authtoken": const.JIUQUAN_TOKEN,
            "act_time": int(round(time.time() * 1000))
        }
        dict_draw_back_curve_raw = ut.request_post_json(
            api_url='https://api.jiucaishuo.com/v2/fund-lists/showhc',
            headers=const.JIUQUAN_HEADER,
            request_param=request_param
        )
        self.__dict_draw_back_curve_raw = dict_draw_back_curve_raw
        self.__populate_draw_back_curve_raw_to_object(dict_draw_back_curve_raw)

    def __populate_draw_back_curve_raw_to_object(self, dict_fund_curve_raw):
        line_data_df = pd.DataFrame()
        for item_data in dict_fund_curve_raw["series"]:
            temp_df = pd.DataFrame(
                item_data["data"], columns=["日期", item_data['name']]
            )
            temp_df["日期"] = pd.to_datetime(temp_df["日期"], unit="s", utc=True).dt.tz_convert("Asia/Shanghai").dt.date
            temp_df["日期"] = temp_df["日期"].apply(lambda x: x.strftime('%Y%m%d'))
            temp_df.set_index(["日期"], inplace=True)
            line_data_df = pd.concat([line_data_df, temp_df], axis=1)
        line_data_df.sort_index(inplace=True)
        self.fund_draw_back_data_df = line_data_df
