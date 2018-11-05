#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/3 22:13
# @Author  : raojingpeng
# @File    : mysql_conn.py

import pymysql
from contextlib import contextmanager


@contextmanager
def get_cursor(host="127.0.0.1", port=3306, user="raojingpeng", password="19941117", db="spider", charset='utf8'):
    """实现上下文管理，执行完毕后自动commit、close"""
    conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

if __name__ == '__main__':
    with get_cursor() as cursor:
        sql = "drop table if exists test"
        cursor.execute(sql)