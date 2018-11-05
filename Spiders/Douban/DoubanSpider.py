#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 18:00
# @Author  : raojingpeng
# @File    : DoubanSpider.py

import requests
from bs4 import BeautifulSoup

def get_html(url):
    '''发出请求获得HTML源码'''
    # 伪装成浏览器访问
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
    resp = requests.get(url, headers=headers).text

    return resp

def get_page():
    '''获得所有需要访问的页面'''
    # 豆瓣Top250
    base_url = r'https://book.douban.com/top250?start='
    url_list = []
    # 共10页，每个页面25本书
    for page in range(0, 250, 25):
        complete_url = base_url + str(page)
        url_list.append(complete_url)

    return url_list

def html_parse(write_proc):
    '''对HTML进行解析'''
    for url in get_page():
        # BeautifulSoup的解析
        soup = BeautifulSoup(get_html(url), 'lxml')
        # 书名
        all_name = soup.find_all('div', class_='pl2')
        name_list = [a.find('a')['title'] for a in all_name]
        # 作者
        all_author = soup.find_all('p', class_='pl')
        author_list = [p.get_text() for p in all_author]
        # 评分
        all_score = soup.find_all('span', class_='rating_nums')
        score_list = [s.get_text() for s in all_score]
        # 简介(部分图书无简介，需特殊处理)
        # 也可以使用CSS选择器选择父级元素：soup.select('tr.item > td:nth-of-type(2)')
        all_tr = soup.find_all('tr', class_='item')
        syno_list = []
        for tr in all_tr:
            # 查找子元素
            syno = tr.find('span', class_='inq')
            real_syno = syno.get_text() if syno else '无'
            syno_list.append(real_syno)

        for name, author, score, syno in zip(name_list, author_list, score_list, syno_list):
            name = '书名：' + str(name) + '\n'
            author = '作者：' + str(author) + '\n'
            score = '评分：' + str(score) + '\n'
            syno = '简介：' + str(syno) + '\n'
            data = name + author + score + syno

            write_proc.writelines(data + '==========================================' + '\n')


if __name__ == '__main__':
    filename = '豆瓣图书Top250.txt'
    with open(filename, 'w', encoding='utf-8') as file_object:
        html_parse(file_object)

    print('Finshed!')