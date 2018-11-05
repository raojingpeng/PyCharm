#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 22:25
# @Author  : raojingpeng
# @File    : LagouSpider.py

import os
import time
import random
import requests
from Lagou import mysql_conn as mysql
from requests.exceptions import RequestException
from multiprocessing import Pool, Queue
from lxml import etree


def get_resp(url, proxies=None, name='Java', page=1):
    """发送url请求，返回网页内容"""
    user_agent_list = [
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    user_agent = random.choice(user_agent_list)
    referer = os.path.split(url[:-1])[1]  # 引用页变量
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": user_agent,
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "close",
        "Origin": "https://www.lagou.com",
        "Host": "www.lagou.com",
        "Referer": "https://www.lagou.com/zhaopin/%s/%s/?filterOption=%s" % (referer, str(page), str(page)),
        "X-Anit-Forge-Code": "0",
        "X-Anit-Forge-Token": "None",
        'Cookie': "JSESSIONID=ABAAABAAAGFABEFA9EAE9D97068B71292C0D79D0640E8E6;"
                + "_ga=GA1.2.243639404.1540776133;"
                + "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1540776133;"
                + "user_trace_token=20181029092212-1034a739-db19-11e8-af2d-525400f775ce;"
                + "LGUID=20181029092212-1034a99a-db19-11e8-af2d-525400f775ce;"
                + "index_location_city=%E5%85%A8%E5%9B%BD;"
                + "X_HTTP_TOKEN=3385ad6d5917ffd2b616415d0cca5c57;"
                + "sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22166bd6aa558ec6-051367878515ad-1e396652-1296000-166bd6aa55911e%22%2C%22%24device_id%22%3A%22166bd6aa558ec6-051367878515ad-1e396652-1296000-166bd6aa55911e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D;"
                + "showExpriedIndex=1;"
                + "showExpriedCompanyHome=1;"
                + "showExpriedMyPublish=1;"
                + "hasDeliver=0;"
                + "TG-TRACK-CODE=index_navigation;"
                + "login=false;"
                + "unick="";"
                + "_putrc="";"
                + "LG_LOGIN_USER_ID="";"  # 用户唯一标识值置空
                + "_gid=GA1.2.1500312194.1541218014;"
                + "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1541218422;"
                + "LGRID=20181103121342-d93f9c24-df1e-11e8-84f1-525400f775ce;"
                + "SEARCH_ID=a9ac5656b99e4b18aa4354b222ac0c0e"
    }
    post_param = {"first": "true", "pn": str(page), "kd": name}
    try:
        # 根据需要使用代理ip
        if proxies:
            resp = requests.post(url, headers=headers, data=post_param, proxies={'http:': proxies}, timeout=5)
        else:
            resp = requests.post(url, headers=headers, data=post_param, timeout=5)

        return resp.text
    except RequestException:
        return None


def parse_index():
    """获取首页的职位和职位对应的url"""
    url = 'http://www.lagou.com/'
    doc = etree.HTML(get_resp(url))
    job_name = doc.xpath(r'//div[@class="menu_box"]//dl//dd/a/text()')
    job_url = doc.xpath(r'//div[@class="menu_box"]//dl//dd/a/@href')
    for name, url in zip(job_name, job_url):
        job_info = {
            'name': name,
            'url': url
        }

        yield job_info


def parse_html(data):
    """解析岗位信息"""
    name, url = data['name'], data['url']
    result = []
    proxies = proxies_pool.get()  # 获得代理ip
    for page in range(1, 31):
        time.sleep(1)  # 防止请求频率过高被ban
        resp = get_resp(url, proxies, name, page)
        doc = etree.HTML(resp)
        # 岗位信息
        post = doc.xpath(r'//div[@class="p_top"]//h3/text()')
        # 工作地址
        addr = doc.xpath(r'//div[@class="p_top"]//span[@class="add"]/em/text()')
        # 发布时间
        release_time = doc.xpath(r'//div[@class="p_top"]//span[@class="format-time"]/text()')
        # 薪资待遇
        salary = doc.xpath(r'//div[@class="p_bot"]//span[@class="money"]/text()')
        # 面向人群
        fit_person = doc.xpath(r'//div[@class="p_bot"]/div/text()[3]')
        # 发布公司
        company = doc.xpath(r'//div[@class="company_name"]/a/text()')
        # 招聘标签
        label = doc.xpath(r'//div[@class="list_item_bot"]/div[@class="li_b_l"]')
        # 公司福利
        welfare = doc.xpath(r'//div[@class="li_b_r"]/text()')
        # 页面无法爬取到内容则退出
        if not post:
            break
        # 保存到列表
        for post, addr, release_time, salary, fit_person, company, label, welfare in \
                zip(post, addr, release_time, salary, fit_person, company, label, welfare):

            # 部分岗位招聘标签为空，需特殊处理
            label_content = ','.join(label.xpath(r'./span/text()')) if label.xpath(r'./span/text()') else ''
            result.append(
                (name, post, addr, release_time, salary, fit_person.strip(), company, label_content, welfare.strip('“”'))
            )
        print('代理ip：%s，爬取地址：%s，进程id：%s' % (proxies, url + str(page), os.getpid()))

    if not result:
        print('该进程被Ban！！')
    proxies_pool.put(proxies)  # ip放回代理池
    save_data(result)


def create_table():
    """清空结果表"""
    with mysql.get_cursor() as cursor:
        sql = "drop table if exists lagou"
        cursor.execute(sql)
        sql = '''
        create table lagou
        (
         job_name varchar(50)
        ,post varchar(50)
        ,addr varchar(50)
        ,release_time varchar(50)
        ,salary varchar(50)
        ,fit_person varchar(50)
        ,company varchar(50)
        ,label varchar(80)
        ,welfare varchar(100)
        ,index (job_name)
        )
        '''
        cursor.execute(sql)


def save_data(data):
    """存储至mysql"""
    with mysql.get_cursor() as cursor:
        insert_sql = '''
        insert into lagou(job_name,post,addr,release_time,salary,fit_person,company,label,welfare) 
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        cursor.executemany(insert_sql, data)
        print('%s保存%d条！' % (data[0][0], len(data)))


if __name__ == '__main__':
    start = time.time()
    # 代理ip列表
    proxies_list = [
        'http://59.32.37.109:8010',
        'http://27.211.137.2:8118',
        'http://39.89.103.181:8118',
        'http://125.125.215.174:53128',
        'http://221.232.234.192:8010',
        'http://115.46.97.64:8123',
        'http://221.232.234.192:8010',
        'http://182.88.165.117:8123',
        'http://218.76.253.201:61408',
        'http://59.32.37.109:8010',
        'http://121.31.173.24:8123',
        'http://42.51.216.15:808'
    ]
    proxies_pool = Queue()
    for proxies in proxies_list:
        proxies_pool.put(proxies)

    create_table()
    pool = Pool(8)

    jobs = (job_info for job_info in parse_index())  # 获取需要爬取的岗位
    for job in jobs:
        pool.apply_async(parse_html, args=(job,))  # 多进程爬取
    pool.close()
    pool.join()

    print('爬取完毕，共耗时%.3f秒' % (time.time() - start))
