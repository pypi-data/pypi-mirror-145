import json
import re
from datetime import datetime, date
from time import sleep

import pandas as pd
import pymongo
import pytz
import requests
from loguru import logger
from pyecharts.charts import Line
import pyecharts.options as opts
from pyecharts.globals import ThemeType
import ofanalysis.const as const


def get_numeric_df_by_column(target_df: pd.DataFrame, target_column_list: list = None, ignore_column_list: list = None):
    '''
    将target_df中需要转换的列，从字符串转换成数字格式列
    如果cell有非数字内容就过滤掉；不能转换成数字格式的成为NaN
    :param target_df:
    :param target_column_list: [column1，column2，...]，需要转换的列
    :param ignore_column_list: [column1，column2，...]，不需要转换的列
    :return:
    '''
    df = target_df.copy()
    column_list = list(target_df.columns)
    if target_column_list is not None:
        column_list = target_column_list
    if ignore_column_list is not None:
        for item in ignore_column_list:
            if item not in column_list:
                continue
            column_list.remove(item)
    for column in column_list:
        # s = df[column].str.extract(r'(-?[0-9]*([\.][0-9]+)?)', expand=True)[0]
        s = df[column].str.extract(r'(-?\d+(\.\d+)?)', expand=True)[0]
        df[column] = pd.to_numeric(s, errors='coerce')
    return df


def extract_float_from_str(s: str):
    '''
    给定的字符串中提取其中所有的数字
    :param s:
    :return:
    '''
    result_list = re.findall(r'-?\d+\.?\d*', s)
    return list(map(float, result_list))


def convert_float_for_dataframe_columns(target_df, columns, number=2, thousands=True):
    """
    给定的dataframe中，指定[列]中的所有数字转换convert_float_format
    :param target_df:
    :param columns: list-> [column1, column2]
    :param number: 保留小数点后几位
    :param thousands:
    :return:
    """
    for column in columns:
        target_df[column] = target_df[column].apply(convert_float_format, args=(number, thousands,))
    return target_df


# 转换数字为：保留n位小数；是否使用千分位
def convert_float_format(target, number=2, thousands=True):
    if isinstance(target, str):
        target = float(target.replace(',', ''))
    first_step = round(target, number)
    second_step = format(first_step, ',') if thousands else first_step
    return second_step


def request_post_json(api_url: str, headers: dict, request_param: dict):
    '''
    发送post request，使用自动重试机制；得到json并转换成字典返回
    :param request_param: 字典格式
    :param headers: const里有或传入
    :param api_url:
    :return: 字典
    '''
    request_data = json.dumps(request_param)
    for _ in range(const.RETRY_TIMES):  # 重试机制
        try:
            response = requests.post(api_url,
                                     headers=headers,
                                     data=request_data)
            if response.status_code != 200:
                logger.info('返回code不是200！')
                raise Exception
        except:
            sleep(2)
        else:
            break
    try:
        dict_result = response.json()['data']
    except Exception:
        try:
            dict_result = response.json()['text']
        except Exception:
            return None
        else:
            return dict_result
    else:
        return dict_result


def db_save_dict_to_mongodb(mongo_db_name: str, col_name: str, target_dict):
    c = pymongo.MongoClient(const.MONGODB_LINK)
    db = c[mongo_db_name]
    db_col = db[col_name]
    if not isinstance(target_dict, list):
        target_dict = [target_dict]
    if len(target_dict) == 0:
        logger.warning('准备存入db的数据为空，不能保存！')
        return
    item = db_col.insert_many(target_dict)
    return item.inserted_ids


def db_get_dict_from_mongodb(mongo_db_name: str, col_name: str,
                             query_dict: dict = {}, field_dict: dict = {}):
    '''

    :param mongo_db_name:
    :param col_name:
    :param query_dict:
    :param field_dict: {'column1':1, 'column2':1}
    :return:
    '''
    c = pymongo.MongoClient(
        host=const.MONGODB_LINK,
        tz_aware=True,
        tzinfo=pytz.timezone('Asia/Shanghai')
    )
    db = c[mongo_db_name]
    db_col = db[col_name]
    field_dict['_id'] = 0
    result_dict_list = [x for x in db_col.find(query_dict, field_dict)]
    return result_dict_list


def db_get_distinct_from_mongodb(mongo_db_name: str, col_name: str, field: str, query_dict: dict = {}):
    c = pymongo.MongoClient(
        host=const.MONGODB_LINK,
        tz_aware=True,
        tzinfo=pytz.timezone('Asia/Shanghai')
    )
    db = c[mongo_db_name]
    db_col = db[col_name]
    result_list = db_col.distinct(field, query=query_dict)
    return result_list


def db_del_dict_from_mongodb(mongo_db_name: str, col_name: str, query_dict: dict):
    c = pymongo.MongoClient(const.MONGODB_LINK)
    db = c[mongo_db_name]
    db_col = db[col_name]
    x = db_col.delete_many(query_dict)
    return x.deleted_count


def get_trade_cal_from_ts(ts_pro_token, start_date: str = '20000101', end_date: str = None):
    if end_date is None:
        end_date = date.today().strftime('%Y%m%d')
    df_trade_cal = ts_pro_token.trade_cal(**{
        "exchange": "SSE",
        "cal_date": "",
        "start_date": start_date,
        "end_date": end_date,
        "is_open": 1,
        "limit": "",
        "offset": ""
    }, fields=[
        "cal_date",
        "pretrade_date"
    ])
    return df_trade_cal['cal_date']


def get_q_end(target_date):
    '''
    获取给定日期所在的季度最后一天
    :param target_date: 6位数日期，例如20211201
    :return:
    '''
    quarter = pd.Period(target_date, 'Q').quarter
    if quarter == 1:
        return datetime(pd.to_datetime(target_date).year, 3, 31).strftime('%Y%m%d')
    elif quarter == 2:
        return datetime(pd.to_datetime(target_date).year, 6, 30).strftime('%Y%m%d')
    elif quarter == 3:
        return datetime(pd.to_datetime(target_date).year, 9, 30).strftime('%Y%m%d')
    else:
        return datetime(pd.to_datetime(target_date).year, 12, 31).strftime('%Y%m%d')


def get_pyechart_line_obj(target_df: pd.DataFrame, line_title: str = ''):
    """
    通过给定的df，生成pyechart的line对象并返回
    :param target_df:
    :param line_title:
    :return:
    """
    line = (Line(
        # init_opts=opts.InitOpts(width='100%', height="700px", theme=ThemeType.DARK)
        init_opts=opts.InitOpts(width='100%', height="700px", bg_color='rgba(173, 235, 179, 1)')

    ).add_xaxis(
        [d for d in list(target_df.index)]
    ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        title_opts=opts.TitleOpts(title=line_title),
        datazoom_opts=[
            opts.DataZoomOpts(is_show=True,
                              type_="slider",
                              range_start=0,
                              range_end=100),
            opts.DataZoomOpts(is_show=True,
                              type_="slider",
                              orient="vertical",
                              range_start=0,
                              range_end=100)
        ]
    ))

    for column in target_df.columns:
        line.add_yaxis(
            series_name=column,
            y_axis=[
                convert_float_format(item, 2, False)
                for item in list(target_df[column])
            ],
            is_symbol_show=False)

    return line
