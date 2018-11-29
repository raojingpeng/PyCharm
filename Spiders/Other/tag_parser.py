#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/27 11:23
# @Author  : raojingpeng
# @File    : tag_parser.py
# pip3 install pandas xlrd openpyxl

import sys
import time
import pandas as pd


def main(title_file, rule_file):
    """
    :rule.xlsx: type|project_name|project_code|project_word
    :title.xlxs: title
    """
    df, rule = pd.read_excel(rule_file), {}
    for i in df.itertuples(index=True, name='Pandas'):
        tp, pn, pc, pw = getattr(i, 'type'), getattr(i, 'project_name'), \
                         getattr(i, 'project_code'), getattr(i,'project_word')
        rule[pw.replace('(','').replace(')','')] = {'tp': tp, 'pn': pn, 'pc': pc, 'pw':pw}  # pw去括号

    df = pd.read_excel(title_file)
    # 生成结果列
    df['type'], df['project_name'], df['project_code'], df['project_word'] = [None for _ in range(4)]
    for i in df.itertuples():
        # print(i)
        index, title = getattr(i, 'Index'), getattr(i, 'title')
        tp, pn, pc, pw = [set() for _ in range(4)]
        for j in rule:
            flag = True
            if '-' not in j:
                for i in j.split('&'):
                    if i not in title:
                        flag = False
                    if flag == False:
                        break
            else:
                j_rule = j.split('-')
                for tmp in j_rule[1:]:
                    title_rule = title.replace(tmp, '')
                if j_rule[0] not in title_rule:
                    flag = False

            if flag:
                tp.add(rule[j]['tp'])
                pn.add(rule[j]['pn'])
                pc.add(rule[j]['pc'])
                pw.add(rule[j]['pw'])

        # df.loc[0]['type'] = '1' wrong method
        df.loc[index, 'type'] = ','.join(list(tp))
        df.loc[index, 'project_name'] = ','.join(list(pn))
        df.loc[index, 'project_code'] = ','.join(list(pc))
        df.loc[index, 'project_word'] = ','.join(list(pw))

    df.to_excel('./result_%s.xlsx' % time.strftime('%Y%m%d'), index=False)  # index=False 去掉多余序号


if __name__ == '__main__':
    title_file = sys.argv[1]  # title文件路径
    rule_file = sys.argv[2]  # rule文件路径
    start = time.time()
    main(title_file, rule_file)
    print('执行完毕!耗时%.2f秒' % (time.time()-start))