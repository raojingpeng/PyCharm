#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 19:36
# @File    : xml_parser.py

import os
import time
from lxml import etree


def get_xml(dir_path, result_path):
    """遍历指定目录下的xml文件，进行解析"""
    xml_path = os.listdir(dir_path)
    xml_list = [os.path.join(dir_path, xml) for xml in xml_path if os.path.splitext(xml)[1] == '.xml']
    global call_swftno
    target_num = excute_time = error_num = 0
    for xml_file in xml_list:
        try:
            start = time.time()
            call_swftno = os.path.splitext(os.path.split(xml_file)[1])[0]  # 获取流水号
            result = xml_parser(xml_file)
            create_file(result_path, result)
            end = time.time()
            excute_time += end - start
            print("'%s'解析完毕，耗时%.3f秒" % (call_swftno, end-start))
        except Exception as e:
            error_num += 1
            print("'%s'格式异常，解析失败!!！(Error:%s)" % (call_swftno, e))
        finally:
            target_num += 1

    return [target_num, error_num, excute_time]


def xml_parser(xml_file):
    """解析xml文件"""
    with open(xml_file, 'r') as file_object:
        xml_content = file_object.read().encode('utf-8')
        doc = etree.XML(xml_content)
        # 整通通话
        global total_duration
        total_duration = doc.xpath(r'//instance/@duration')[0]
        total_call = doc.xpath(r'//channel[@no="mix"]//item')
        input_dict, output_dict = {}, {}
        for tc in total_call:
            if tc.xpath(r'@duration'):  # 有duration属性的标签为静音通话
                etree.strip_attributes(tc, 'duration')
                tc.set('energy', '')
                tc.set('speed', '')
            get_attr = tc.xpath('attribute::*')  # 获取标签中所有属性值
            template = ('start', 'end', 'energy', 'speed')
            tmp_dict = dict(zip(template, get_attr))
            input_dict[int(tmp_dict['start'])] = tmp_dict  # 按开始时间打标

        sorted_list = [tl[1] for tl in sorted(input_dict.items(), key=lambda item: item[0])]  # 根据开始时间对通话排序
        for call_num in range(len(sorted_list)):
            output_dict[call_num+1] = sorted_list[call_num]

        # 坐席通话
        agent_time = doc.xpath(r'//channel[@no="n0"]//time/text()')[0].split(' ') if doc.xpath(r'//channel[@no="n0"]//time/text()') else []
        agent_text = doc.xpath(r'//channel[@no="n0"]//text/text()')[0].split(' ') if doc.xpath(r'//channel[@no="n0"]//text/text()') else []
        agent_call = call_generator(agent_time, agent_text, '0')
        # 客户通话
        cust_time = doc.xpath(r'//channel[@no="n1"]//time/text()')[0].split(' ') if doc.xpath(r'//channel[@no="n1"]//time/text()') else []
        cust_text = doc.xpath(r'//channel[@no="n1"]//text/text()')[0].split(' ') if doc.xpath(r'//channel[@no="n1"]//text/text()') else []
        cust_call = call_generator(cust_time, cust_text, '1')
        # 合并坐席与客户通话
        agent_call.update(cust_call)
        call_content = {key: value for key, value in sorted(agent_call.items(), key=lambda item: item[0])}
        result = call_match(output_dict, call_content)

        return result


def call_generator(timeline, contents, role):
    """生成通话信息"""
    call_content = {}
    for timestamp, content in zip(timeline, contents):
        start = int(timestamp.split(',')[0])  # 以开始时间先后作为对话顺序
        call_content[start] = {'content': content, 'role': role}

    return call_content


def call_match(entire_call, call_content):
    """根据时间点匹配通话内容"""
    text_generate = ["%s|0|||%s||||" % (call_swftno, total_duration)]  # 录音总时长
    for key1, value1 in entire_call.items():
        seq_num, start_time, end_time, speed, energy, content = \
            key1, int(value1['start']), int(value1['end']), value1['speed'], value1['energy'], ''
        duration = end_time - start_time
        role = 2  # 默认角色为静音
        for key2, value2 in list(call_content.items()):
            if key2 < end_time:
                content += value2['content'] + ' '  # 空格分词
                role = value2['role']
                call_content.pop(key2)  # 删除解析过的通话
            else:
                break

        text_generate.append("%s|%s|%s|%s|%s|%s|%s|%s|%s" % (call_swftno, seq_num, start_time, end_time, duration, role, speed, energy, content))

    return text_generate


def create_file(result_path, result):
    """生成dat文件"""
    file_name = os.path.join(result_path, call_swftno + '.dat')
    with open(file_name, 'w') as file_object:
        for content in result:
            file_object.writelines(content + '\n')


if __name__ == '__main__':
    dir_path = r'/Users/raojingpeng/PycharmProjects/Spiders/xml_home/testData'  # xml文件存放目录
    result_path = r'/Users/raojingpeng/PycharmProjects/Spiders/xml_home/result'  # 解析后存放目录
    excute_log = get_xml(dir_path, result_path)
    print('本次解析共%s个文件，失败%s个，共耗时%.3f秒' % (excute_log[0], excute_log[1], excute_log[2]))
