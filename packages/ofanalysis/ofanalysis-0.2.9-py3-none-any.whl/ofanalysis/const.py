'''
本模块存放常量
'''
import os

import tushare as ts

LIXINGREN_HEADER = {
    "Content-Type": "application/json",
    "Accept - Encoding": "gzip, deflate, br"
}

# MONGODB_LINK = "mongodb://localhost:27017/"
# MONGODB_LINK = "mongodb://192.168.2.188:27017/"  # 数据库连接指向gen8服务器
MONGODB_LINK = "mongodb://layewang:toorroot!@mongo:27017/"

MONGODB_DB_JIUQUAN = 'db_jiuquan'
MONGODB_COL_JQ_FUND_VEST_RAW = 'fund_vest_raw'
MONGODB_COL_JQ_FUND_INFO_RAW = 'fund_info_raw'
MONGODB_COL_JQ_FUND_DATA_RAW = 'fund_data_raw'
MONGODB_COL_JQ_FUND_RANK_LIST_RAW = 'fund_rank_list_raw'
MONGODB_COL_JQ_FUND_RANK_RAW = 'fund_rank_raw'
MONGODB_COL_JQ_FUND_MANAGER_RAW = 'fund_manager_raw'
MONGODB_COL_JQ_FUND_TYPE_CATE_MD = 'fund_type_cate_md'

MONGODB_DB_LXR = 'db_lixingren'
MONGODB_COL_LXR_SW_IND = 'sw_ind'
MONGODB_COL_LXR_INDEX = 'index'

MONGODB_DB_TUSHARE = 'db_tushare'
MONGODB_COL_TS_STOCK_BASIC = 'stock_basic'
MONGODB_COL_TS_STOCK_DAILY_BASIC = 'stock_daily_basic'
MONGODB_COL_TS_STOCK_DAILY = 'stock_daily'
MONGODB_COL_TS_FUND_BASIC = 'fund_basic'
MONGODB_COL_TS_FUND_NAV = 'fund_nav'
MONGODB_COL_TS_FUND_SHARE = 'fund_share'
MONGODB_COL_TS_FUND_MANAGER = 'fund_manager'
MONGODB_COL_TS_FUND_PORTFOLIO = 'fund_portfolio'

MONGODB_DB_TKSHARE = 'db_tkshare'
MONGODB_COL_TKS_INDEX_GUZHI = 'tks_index_guzhi'
MONGODB_COL_TKS_FUND_RATING = 'tks_fund_rating'

MONGODB_DB_MORNINGSTAR = 'db_morningstar'
MONGODB_COL_MORNINGSTAR_RATING = 'morningstar_fund_rating'

MONGODB_DB_ANALYSIS_HELP = 'db_analysis_help'
MONGODB_COL_ANALYSIS_HELP_MANAGER_ANALYSIS = 'analysis_help_manager_analysis'

# 韭圈儿相关常量
JIUQUAN_TOKEN = '3a4foJI0h844aoZGPLg18CU/gkpeEUed'
JIUQUAN_HEADER = {
    'Host': 'api.jiucaishuo.com',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json;charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://funddb.cn',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'zh-CN,zh;q=0.9',
}

# 从网上api拉数据相关参数
RETRY_TIMES = 5  # 重试次数
EACH_TIME_ITEM = 2000  # tushare分页获取数据，每页条目数

# 基金相关参数
PARAMS = {
    'lxr_index': {
        '000905': '中证500',
        '000300': '沪深300',
        '000922': '中证红利',
        '000903': '中证100',
        '399006': '创业板指',
        '000933': '中证医药',
        '000931': '中证可选',
        '000935': '中证信息',
        '399995': '基建工程',
        '399971': '中证传媒',
        '399967': '中证军工',
        '000807': '中证食品饮料',
        '000992': '全指金融',
        '399812': '养老产业',
        '000827': '中证环保',
        '000990': '全指消费',
        '399975': '证券公司',
        '000016': '上证50',
        '000852': '中证1000',
        '000906': '中证800',
        '000688': '科创50',
        '000998': '中证TMT',
        '1000002': '沪深A股',
        '1000004': '上海A股',
        '1000003': '深圳A股',
        '1000007': '创业板全指',
        '.INX': '标普500'
    },
    'lxr_sw_l1_ind': {
        '110000': '农林牧渔',
        '220000': '基础化工',
        '230000': '钢铁',
        '240000': '有色金属',
        '270000': '电子',
        '280000': '汽车',
        '330000': '家用电器',
        '340000': '食品饮料',
        '350000': '纺织服饰',
        '360000': '轻工制造',
        '370000': '医药生物',
        '410000': '公用事业',
        '420000': '交通运输',
        '430000': '房地产',
        '450000': '商贸零售',
        '460000': '社会服务',
        '480000': '银行',
        '490000': '非银金融',
        '510000': '综合',
        '610000': '建筑材料',
        '620000': '建筑装饰',
        '630000': '电力设备',
        '640000': '机械设备',
        '650000': '国防军工',
        '710000': '计算机',
        '720000': '传媒',
        '730000': '通信',
        '740000': '煤炭',
        '750000': '石油石化',
        '760000': '环保',
        '770000': '美容护理'
    }
}
