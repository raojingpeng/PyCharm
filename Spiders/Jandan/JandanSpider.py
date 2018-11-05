#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 21:03
# @Author  : raojingpeng
# @File    : JandanSpider.py

import os
import requests
import base64
from lxml import etree


def get_html(url):
    """请求页面，返回响应"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp
        return None
    except ConnectionError:
        print('Error.')


def get_img_hash(page_url):
    """请求页面，返回页面中所有图片hash值"""
    html = get_html(page_url).text
    doc = etree.HTML(html)
    img_hash = doc.xpath(r'//span[@class="img-hash"]/text()')

    return img_hash


def get_all_page():
    """得到所有需要爬取的页面"""
    url_list = []
    home_page = get_html(r'http://jandan.net/ooxx').text
    home_page_num = etree.HTML(home_page).xpath(r'//span[@class="current-comment-page"]/text()')[0][1:-1]
    for page in range(1, int(home_page_num)+1):
        url_list.append('http://jandan.net/ooxx/page-' + str(page) + '#comments')

    return url_list


def base64_decode(hash):
    """对图片hash值进行解密"""
    pic_url = 'http:' + base64.b64decode(hash).decode('utf-8')

    return pic_url


def download_pic(pic_url_list):
    """根据地址下载图片"""
    for pic_url in pic_url_list:
        file_name = './Jandan/' + pic_url[-14:]
        img_content = get_html(pic_url).content

        with open(file_name, 'wb') as file_object:
            file_object.write(img_content)
            print('Finished' + file_name + '!')


def main():
    if not os.path.exists('./Jandan'):
        os.mkdir('./Jandan/')

    pic_url_list = []
    for url in get_all_page():
        hash_list = get_img_hash(url)
        for hash in hash_list:
            pic_url = base64_decode(hash)
            pic_url_list.append(pic_url)

    download_pic(pic_url_list)


if __name__ == '__main__':
    main()
