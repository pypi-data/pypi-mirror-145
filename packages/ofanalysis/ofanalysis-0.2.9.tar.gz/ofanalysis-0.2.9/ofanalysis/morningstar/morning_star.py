import datetime
import math
from time import sleep
import re
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from urllib import parse
import ofanalysis.utility as ut
from ofanalysis import const
from ofanalysis.morningstar.mysnowflake import IdWorker
import numpy as np
import requests
from PIL import Image


class MorningStar:
    def __init__(self, web_driver_path: str, assets_path: str, cookie_str:str, temp_path:str = './temp_storage.csv'):
        self.web_driver_path = web_driver_path
        self.assets_path = assets_path
        self.cookie_str = cookie_str
        self.temp_path = temp_path

    def write_to_db(self):
        morningstar_df = pd.read_csv(self.temp_path)
        morningstar_df['update_date'] = datetime.date.today().strftime('%Y%m%d')
        morningstar_df.reset_index(drop=True, inplace=True)

        ut.db_del_dict_from_mongodb(
            mongo_db_name=const.MONGODB_DB_MORNINGSTAR,
            col_name=const.MONGODB_COL_MORNINGSTAR_RATING,
            query_dict={}
        )

        ut.db_save_dict_to_mongodb(
            mongo_db_name=const.MONGODB_DB_MORNINGSTAR,
            col_name=const.MONGODB_COL_MORNINGSTAR_RATING,
            target_dict=morningstar_df.to_dict(orient='records')
        )

    def get_fund_list(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('headless')
        s = Service(self.web_driver_path)
        chrome_driver = webdriver.Chrome(service=s, options=chrome_options)
        chrome_driver.set_page_load_timeout(12000)  # 防止页面加载个没完

        morning_fund_selector_url = "https://www.morningstar.cn/fundselect/default.aspx"
        for _ in range(const.RETRY_TIMES):  # 重试机制
            try:
                self.__set_cookies(chrome_driver, morning_fund_selector_url)
            except:
                logger.warning('set cookie error, retry...')
                sleep(2)
            else:
                break
        try:
            existed_df = pd.read_csv(self.temp_path, dtype={'代码': str})
        except:
            existed_df = pd.DataFrame()
        else:
            pass
        if existed_df.empty:
            page_num = 1
        else:
            page_num = existed_df.iloc[-1]['页码'] + 1
        page_count = 25
        page_num_total = math.ceil(
            int(chrome_driver.find_element(
                by=By.XPATH,
                value='/html/body/form/div[8]/div/div[4]/div[3]/div[2]/span'
            ).text) / page_count
        )

        output_head = '代码' + ',' + '晨星专属号' + ',' + '名称' + ',' + \
                      '类型' + ',' + '三年评级' + ',' + '五年评级' + ',' + '今年回报率' + ',' + '页码' + '\n'
        # 设置表头
        if page_num == 1:
            with open(self.temp_path, 'w+') as csv_file:
                csv_file.write(output_head)
        while page_num <= page_num_total:
            # 求余
            remainder = page_num_total % 10
            # 判断是否最后一页
            num = (remainder + 2) if page_num > (page_num_total - remainder) else 12
            next_page_xpath_str = '/html/body/form/div[8]/div/div[4]/div[3]/div[3]/div[1]/a[%s]' % (num)

            logger.info(f'processing page {page_num} of {page_num_total}')
            # 等待，直到当前页（样式判断）等于page_num
            WebDriverWait(chrome_driver, timeout=3600).until(self.__text_to_be_present_in_element(
                "/html/body/form/div[8]/div/div[4]/div[3]/div[3]/div[1]/span[@style='margin-right:5px;font-weight:Bold;color:red;']",
                str(page_num), next_page_xpath_str))
            sleep(1)

            # 列表用于存放爬取的数据
            id_list = []  # 雪花id
            code_list = []  # 基金代码
            morning_star_code_list = []  # 晨星专属代码
            name_list = []  # 基金名称
            fund_cat = []  # 基金分类
            fund_rating_3 = []  # 晨星评级（三年）
            fund_rating_5 = []  # 晨星评级（五年）
            rate_of_return = []  # 今年以来汇报（%）

            # 获取每页的源代码
            data = chrome_driver.page_source
            # 利用BeautifulSoup解析网页源代码
            bs = BeautifulSoup(data, 'lxml')
            class_list = ['gridItem', 'gridAlternateItem']  # 数据在这两个类下面

            # 取出所有类的信息，并保存到对应的列表里
            for i in range(len(class_list)):
                for tr in bs.find_all('tr', {'class': class_list[i]}):
                    # 雪花id
                    worker = IdWorker()
                    id_list.append(worker.get_id())
                    tds_text = tr.find_all('td', {'class': "msDataText"})
                    tds_nume = tr.find_all('td', {'class': "msDataNumeric"})
                    # 基金代码
                    code_a_element = tds_text[0].find_all('a')[0]
                    code_list.append(code_a_element.string)
                    # 从href中匹配出晨星专属代码
                    current_morning_code = re.findall(
                        r'(?<=/quicktake/)(\w+)$', code_a_element.get('href')).pop(0)
                    # 晨星基金专属晨星码
                    morning_star_code_list.append(current_morning_code)
                    name_list.append(tds_text[1].find_all('a')[0].string)
                    # 基金分类
                    fund_cat.append(tds_text[2].string)
                    # 三年评级
                    rating = self.__get_star_count(tds_text[3].find_all('img')[0]['src'])
                    fund_rating_3.append(rating)
                    # 5年评级
                    rating = self.__get_star_count(tds_text[4].find_all('img')[0]['src'])
                    fund_rating_5.append(rating)
                    # 今年以来回报(%)
                    return_value = tds_nume[3].string if tds_nume[3].string != '-' else None
                    rate_of_return.append(return_value)
            fund_df = pd.DataFrame(
                {
                    'id': id_list,
                    'fund_code': code_list,
                    'morning_star_code': morning_star_code_list,
                    'fund_name': name_list,
                    'fund_cat': fund_cat,
                    'fund_rating_3': fund_rating_3,
                    'fund_rating_5': fund_rating_5,
                    'rate_of_return': rate_of_return,
                    'page_number': page_num
                })
            fund_list = fund_df.values.tolist()
            # logger.info(f'fund_list{fund_list}')
            with open(self.temp_path, 'a') as csv_file:
                for fund_item in fund_list:
                    output_line = ','.join(str(x) for x in fund_item) + '\n'
                    csv_file.write(output_line)
            # 获取下一页元素
            next_page = chrome_driver.find_element(by=By.XPATH, value=next_page_xpath_str)
            # 点击下一页
            next_page.click()
            page_num += 1
        chrome_driver.close()
        logger.info('end')

    def __set_cookies(self, chrome_driver, url):
        for _ in range(const.RETRY_TIMES):  # 重试机制
            try:
                chrome_driver.get(url)  # 2.需要先获取一下url，不然使用add_cookie会报错，这里有点奇怪
            except:
                logger.warning('setting cookies error, retry...')
                sleep(2)
            else:
                break
        cookie_list = self.__parse_cookiestr()
        chrome_driver.delete_all_cookies()
        for i in cookie_list:
            cookie = {}
            # 3.对于使用add_cookie来说，参考其函数源码注释，需要有name,value字段来表示一条cookie，有点生硬
            cookie['name'] = i['name']
            cookie['value'] = i['value']
            # 4.这里需要先删掉之前那次访问时的同名cookie，不然自己设置的cookie会失效
            # chrome_driver.delete_cookie(i['name'])
            # 添加自己的cookie
            # print('cookie', cookie)
            chrome_driver.add_cookie(cookie)
        chrome_driver.refresh()

    def __parse_cookiestr(self, split_str="; "):
        cookielist = []
        for item in self.cookie_str.split(split_str):
            cookie = {}
            itemname = item.split('=')[0]
            iremvalue = item.split('=')[1]
            cookie['name'] = itemname
            cookie['value'] = parse.unquote(iremvalue)
            cookielist.append(cookie)
        return cookielist

    def __text_to_be_present_in_element(self, locator, text, next_page_locator):
        """ An expectation for checking if the given text is present in the
        specified element.
        locator, text
        """

        def _predicate(driver):
            try:
                element_text = driver.find_element(by=By.XPATH, value=locator).text
                if int(element_text) <= 10:  # 处理0-10页的情况，也就是翻页器在第一页，只出现一个'...'
                    next_10_page_locator = '/html/body/form/div[8]/div/div[4]/div[3]/div[3]/div[1]/span[2]/a'
                else:
                    next_10_page_locator = '/html/body/form/div[8]/div/div[4]/div[3]/div[3]/div[1]/span[3]/a'
                if (int(text) - int(element_text))>10:
                    logger.info(f'current page is {element_text} while finding {text}')
                    next_10_page = driver.find_element(by=By.XPATH, value=next_10_page_locator)
                    next_10_page.click()
                    sleep(5)
                elif int(element_text) < int(text):  # 比给定的页码小的话，触发下一页
                    logger.info(f'current page is {element_text} while finding {text}')
                    next_page = driver.find_element(by=By.XPATH, value=next_page_locator)
                    # driver.refresh()
                    next_page.click()
                    sleep(5)
                    # 比给定的页码大的话，触发上一页
                elif int(element_text) > int(text):
                    logger.info(f'current page is {element_text} while finding {text}')
                    prev_page =driver.find_element(
                        by=By.XPATH,
                        value='/html/body/form/div[8]/div/div[4]/div[3]/div[3]/div[1]/a[2]')
                    # driver.refresh()
                    prev_page.click()
                    sleep(5)
                return text == element_text
            except:
                return False

        return _predicate

    def __get_star_count(self, morning_star_url):
        temp_star_url = f'{self.assets_path}/star/tmp.gif'
        r = requests.get(morning_star_url)
        with open(temp_star_url, "wb") as f:
            f.write(r.content)
        f.close()
        path = f'{self.assets_path}/star/star'

        for i in range(6):
            p1 = np.array(Image.open(path + str(i) + '.gif'))
            p2 = np.array(Image.open(temp_star_url))
            if (p1 == p2).all():
                return i
