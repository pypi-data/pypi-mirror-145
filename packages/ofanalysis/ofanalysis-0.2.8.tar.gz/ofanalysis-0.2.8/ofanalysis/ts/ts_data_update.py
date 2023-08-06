import datetime
from time import sleep

import pandas as pd
from loguru import logger

import ofanalysis.const as const
import ofanalysis.utility as ut
import tushare as ts


class TSDataUpdate:
    def __init__(self, ts_pro_token:str):
        self.__pro = ts.pro_api(ts_pro_token)
        self.__today = datetime.date.today()

    def retrieve_all(self):
        self.retrieve_stock_basic()
        self.retrieve_stock_daily_basic()
        self.retrieve_stock_daily()
        self.retrieve_fund_basic()
        self.retrieve_fund_nav()
        self.retrieve_fund_share()
        self.retrieve_fund_manager()
        self.retrieve_fund_portfolio()

    def retrieve_stock_basic(self):
        logger.info('全量更新股票基础信息stock_basic')
        # 分页读取数据
        df_stock_basic = pd.DataFrame()
        i = 0
        while True:  # 分页读取数据
            df_batch_result = self.__pro.stock_basic(**{
                "ts_code": "",
                "name": "",
                "exchange": "",
                "market": "",
                "is_hs": "",
                "list_status": "",
                "limit": const.EACH_TIME_ITEM,
                "offset": i
            }, fields=[
                "ts_code",
                "symbol",
                "name",
                "area",
                "industry",
                "market",
                "list_date",
                "is_hs",
                "delist_date",
                "list_status",
                "curr_type",
                "exchange",
                "cnspell",
                "enname",
                "fullname"
            ])
            if len(df_batch_result) == 0:
                break
            df_stock_basic = pd.concat([df_stock_basic, df_batch_result], ignore_index=True)
            i += const.EACH_TIME_ITEM
        ut.db_del_dict_from_mongodb(  # 非增量更新 先清空数据
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_STOCK_BASIC,
            query_dict={}
        )
        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_STOCK_BASIC,
            target_dict=df_stock_basic.to_dict(orient='records')
        )

    def retrieve_stock_daily_basic(self):
        check_field = 'trade_date'  # 设置增量更新依据字段
        logger.info('更新股票每日指标stock_daily_basic')
        existed_records = ut.db_get_distinct_from_mongodb(
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_STOCK_DAILY_BASIC,
            field=check_field
        )
        if len(existed_records) == 0:  # 空表
            trade_cal_start_date = '20000101'
        else:
            existed_records.sort(reverse=True)  # 倒排
            trade_cal_start_date = pd.to_datetime(existed_records[-1]) + datetime.timedelta(days=1)
            trade_cal_start_date = trade_cal_start_date.strftime('%Y%m%d')
        trade_cal_list = ut.get_trade_cal_from_ts(ts_pro_token=self.__pro, start_date=trade_cal_start_date)

        for date in [x for x in trade_cal_list if x not in existed_records]:
            logger.info('更新股票每日指标stock_daily_basic: %s的数据' % date)
            df_daily = pd.DataFrame()
            i = 0
            while True:  # 分页读取数据
                for _ in range(const.RETRY_TIMES):  # 重试机制
                    try:
                        df_batch_daily = self.__pro.daily_basic(**{
                            "ts_code": "",
                            "trade_date": date,
                            "start_date": "",
                            "end_date": "",
                            "limit": const.EACH_TIME_ITEM,
                            "offset": i
                        }, fields=[
                            "ts_code",
                            "trade_date",
                            "close",
                            "turnover_rate",
                            "turnover_rate_f",
                            "volume_ratio",
                            "pe",
                            "pe_ttm",
                            "pb",
                            "ps",
                            "ps_ttm",
                            "dv_ratio",
                            "dv_ttm",
                            "total_share",
                            "float_share",
                            "free_share",
                            "total_mv",
                            "circ_mv"
                        ])
                    except:
                        sleep(1)
                    else:
                        break
                if len(df_batch_daily) == 0:
                    break
                df_daily = pd.concat([df_daily, df_batch_daily], ignore_index=True)
                i += const.EACH_TIME_ITEM
            if len(df_daily) == 0:
                logger.info('日期：%s, 股票每日指标stock_daily_basic返回为空' % date)
                continue
            ut.db_save_dict_to_mongodb(
                mongo_db_name=const.MONGODB_DB_TUSHARE,
                col_name=const.MONGODB_COL_TS_STOCK_DAILY_BASIC,
                target_dict=df_daily.to_dict(orient='records')
            )

    def retrieve_stock_daily(self):
        check_field = 'trade_date'  # 设置增量更新依据字段
        logger.info('更新股票日线行情stock_daily')
        existed_records = ut.db_get_distinct_from_mongodb(
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_STOCK_DAILY,
            field=check_field
        )
        if len(existed_records) == 0:  # 空表
            trade_cal_start_date = '20000101'
        else:
            existed_records.sort(reverse=True)  # 倒排
            trade_cal_start_date = pd.to_datetime(existed_records[-1]) + datetime.timedelta(days=1)
            trade_cal_start_date = trade_cal_start_date.strftime('%Y%m%d')
        trade_cal_list = ut.get_trade_cal_from_ts(ts_pro_token=self.__pro, start_date=trade_cal_start_date)

        for date in [x for x in trade_cal_list if x not in existed_records]:
            logger.info('更新股票日线行情stock_daily: %s的数据' % date)
            df_daily = pd.DataFrame()
            i = 0
            while True:  # 分页读取数据
                for _ in range(const.RETRY_TIMES):  # 重试机制
                    try:
                        df_batch_daily = self.__pro.daily(**{
                            "ts_code": "",
                            "trade_date": date,
                            "start_date": "",
                            "end_date": "",
                            "offset": i,
                            "limit": const.EACH_TIME_ITEM
                        }, fields=[
                            "ts_code",
                            "trade_date",
                            "open",
                            "high",
                            "low",
                            "close",
                            "pre_close",
                            "change",
                            "pct_chg",
                            "vol",
                            "amount"
                        ])
                    except:
                        sleep(1)
                    else:
                        break
                if len(df_batch_daily) == 0:
                    break
                df_daily = pd.concat([df_daily, df_batch_daily], ignore_index=True)
                i += const.EACH_TIME_ITEM
            if len(df_daily) == 0:
                logger.info('日期：%s, 股票日线行情stock_daily返回为空' % date)
                continue
            ut.db_save_dict_to_mongodb(
                mongo_db_name=const.MONGODB_DB_TUSHARE,
                col_name=const.MONGODB_COL_TS_STOCK_DAILY,
                target_dict=df_daily.to_dict(orient='records')
            )

    def retrieve_fund_basic(self):
        logger.info('全量更新基金基础信息fund_basic')
        df_all_fund = pd.DataFrame()
        i = 0
        while True:  # 分页读取数据
            df_batch_result = self.__pro.fund_basic(**{
                "ts_code": "",
                "market": "",
                "update_flag": "",
                "offset": i,
                "limit": const.EACH_TIME_ITEM,
                "status": ""
            }, fields=[
                "ts_code",
                "name",
                "management",
                "custodian",
                "fund_type",
                "found_date",
                "due_date",
                "list_date",
                "issue_date",
                "delist_date",
                "issue_amount",
                "m_fee",
                "c_fee",
                "duration_year",
                "p_value",
                "min_amount",
                "exp_return",
                "benchmark",
                "status",
                "invest_type",
                "type",
                "trustee",
                "purc_startdate",
                "redm_startdate",
                "market"
            ])
            if len(df_batch_result) == 0:
                break
            df_all_fund = pd.concat([df_all_fund, df_batch_result], ignore_index=True)
            i += const.EACH_TIME_ITEM
            sleep(8)
        ut.db_del_dict_from_mongodb(  # 非增量更新 先清空数据
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_FUND_BASIC,
            query_dict={}
        )
        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_FUND_BASIC,
            target_dict=df_all_fund.to_dict(orient='records')
        )

    def retrieve_fund_nav(self):
        check_field = 'nav_date'  # 设置增量更新依据字段
        logger.info('更新基金净值行情fund_nav')
        existed_records = ut.db_get_distinct_from_mongodb(
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_FUND_NAV,
            field=check_field
        )
        if len(existed_records) == 0:  # 空表
            trade_cal_start_date = '20000101'
        else:
            existed_records.sort(reverse=True)  # 倒排
            trade_cal_start_date = pd.to_datetime(existed_records[-1]) + datetime.timedelta(days=1)
            trade_cal_start_date = trade_cal_start_date.strftime('%Y%m%d')
        trade_cal_list = ut.get_trade_cal_from_ts(ts_pro_token=self.__pro, start_date=trade_cal_start_date)

        for date in [x for x in trade_cal_list if x not in existed_records]:
            logger.info('更新基金净值行情fund_nav: %s的数据' % date)
            df_daily = pd.DataFrame()
            i = 0
            while True:  # 分页读取数据
                for _ in range(const.RETRY_TIMES):  # 重试机制
                    try:
                        df_batch_daily = self.__pro.fund_nav(**{
                            "ts_code": "",
                            "nav_date": date,
                            "offset": i,
                            "limit": const.EACH_TIME_ITEM,
                            "market": "",
                            "start_date": "",
                            "end_date": ""
                        }, fields=[
                            "ts_code",
                            "ann_date",
                            "nav_date",
                            "unit_nav",
                            "accum_nav",
                            "accum_div",
                            "net_asset",
                            "total_netasset",
                            "adj_nav",
                            "update_flag"
                        ])
                    except:
                        sleep(1)
                    else:
                        break
                if len(df_batch_daily) == 0:
                    break
                df_daily = pd.concat([df_daily, df_batch_daily], ignore_index=True)
                i += const.EACH_TIME_ITEM
            if len(df_daily) == 0:
                logger.info('日期：%s, 基金净值行情fund_nav返回为空' % date)
                continue
            ut.db_save_dict_to_mongodb(
                mongo_db_name=const.MONGODB_DB_TUSHARE,
                col_name=const.MONGODB_COL_TS_FUND_NAV,
                target_dict=df_daily.to_dict(orient='records')
            )

    def retrieve_fund_share(self):
        check_field = 'trade_date'  # 设置增量更新依据字段
        logger.info('更新基金净值规模fund_share')
        existed_records = ut.db_get_distinct_from_mongodb(
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_FUND_SHARE,
            field=check_field
        )
        if len(existed_records) == 0:  # 空表
            trade_cal_start_date = '20000101'
        else:
            existed_records.sort(reverse=True)  # 倒排
            trade_cal_start_date = pd.to_datetime(existed_records[-1]) + datetime.timedelta(days=1)
            trade_cal_start_date = trade_cal_start_date.strftime('%Y%m%d')
        trade_cal_list = ut.get_trade_cal_from_ts(ts_pro_token=self.__pro, start_date=trade_cal_start_date)

        for date in [x for x in trade_cal_list if x not in existed_records]:
            logger.info('更新基金净值规模fund_share: %s的数据' % date)
            df_daily = pd.DataFrame()
            i = 0
            while True:  # 分页读取数据
                for _ in range(const.RETRY_TIMES):  # 重试机制
                    try:
                        df_batch_daily = self.__pro.fund_share(**{
                            "ts_code": "",
                            "trade_date": date,
                            "start_date": "",
                            "end_date": "",
                            "market": "",
                            "fund_type": "",
                            "limit": const.EACH_TIME_ITEM,
                            "offset": i
                        }, fields=[
                            "ts_code",
                            "trade_date",
                            "fd_share",
                            "fund_type",
                            "market"
                        ])
                    except:
                        sleep(1)
                    else:
                        break
                if len(df_batch_daily) == 0:
                    break
                df_daily = pd.concat([df_daily, df_batch_daily], ignore_index=True)
                i += const.EACH_TIME_ITEM
            if len(df_daily) == 0:
                logger.info('日期：%s, 基金净值规模fund_share返回为空' % date)
                continue
            ut.db_save_dict_to_mongodb(
                mongo_db_name=const.MONGODB_DB_TUSHARE,
                col_name=const.MONGODB_COL_TS_FUND_SHARE,
                target_dict=df_daily.to_dict(orient='records')
            )

    def retrieve_fund_manager(self):
        logger.info('全量更新基金经理fund_manager')
        df_result = pd.DataFrame()
        i = 0
        each_time_item = const.EACH_TIME_ITEM
        while True:  # 分页读取数据
            for _ in range(const.RETRY_TIMES):  # 重试机制
                try:
                    df_batch = self.__pro.fund_manager(**{
                        "ts_code": "",
                        "ann_date": "",
                        "name": "",
                        "offset": i,
                        "limit": const.EACH_TIME_ITEM
                    }, fields=[
                        "ts_code",
                        "ann_date",
                        "name",
                        "gender",
                        "birth_year",
                        "edu",
                        "nationality",
                        "begin_date",
                        "end_date",
                        "resume"
                    ])
                except:
                    sleep(1)
                else:
                    break
            if len(df_batch) == 0:
                break
            df_result = pd.concat([df_result, df_batch], ignore_index=True)
            i += each_time_item
        ut.db_del_dict_from_mongodb(  # 非增量更新 先清空数据
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_FUND_MANAGER,
            query_dict={}
        )
        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_FUND_MANAGER,
            target_dict=df_result.to_dict(orient='records')
        )

    def retrieve_fund_portfolio(self):
        check_field = 'ann_date'  # 设置增量更新依据字段
        logger.info('更新基金持仓的数据fund_portfolio')
        existed_records = ut.db_get_distinct_from_mongodb(
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_FUND_PORTFOLIO,
            field=check_field
        )
        if len(existed_records) == 0:  # 空表
            start_date = self.__today - datetime.timedelta(days=(365 * 7))
        else:
            existed_records.sort(reverse=True)  # 倒排
            start_date = pd.to_datetime(existed_records[0]) + datetime.timedelta(days=1)
        start_date = start_date.strftime('%Y%m%d')
        df_result = pd.DataFrame()
        i = 0
        while True:  # 分页读取数据
            for _ in range(const.RETRY_TIMES):  # 重试机制
                try:
                    logger.info('开始取日期%s的数据，分批取第%s数据' % (start_date, str(i)))
                    df_batch = self.__pro.fund_portfolio(**{
                        "ts_code": "",
                        "ann_date": "",
                        "start_date": start_date,
                        "end_date": self.__today.strftime('%Y%m%d'),
                        "limit": const.EACH_TIME_ITEM,
                        "offset": i
                    }, fields=[
                        "ts_code",
                        "ann_date",
                        "end_date",
                        "symbol",
                        "mkv",
                        "amount",
                        "stk_mkv_ratio",
                        "stk_float_ratio"
                    ])
                except:
                    sleep(1)
                else:
                    break
            if len(df_batch) == 0:
                break
            df_result = pd.concat([df_result, df_batch], ignore_index=True)
            i += const.EACH_TIME_ITEM
        if len(df_result) == 0:
            logger.info('取得的基金持仓的数据fund_portfolio为空')
            return
        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_FUND_PORTFOLIO,
            target_dict=df_result.to_dict(orient='records')
        )
