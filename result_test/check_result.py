# -*- coding:utf-8 -*-
u'''
  文 件 名   : check_result.py
  依 赖 包   : pip install lxml
  版 本 号   :
  作    者   : 张茗 
  生成日期   : 2017年4月21日
  最近修改   :
  功能描述   : 测试龙湾OCR的接口返回数据的识别率
  函数列表   : 
  修改历史   :
    1、日    期   : 2017年4月21日
       作    者   : 张茗
       修改内容   : 创建文件

u'''
import json
from xml.etree import ElementTree as XmlTree
import requests
import os

from constant_cofing.ZGYHSKHD import CORRECT_RESULT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'static', 'image')
XML_DIR = os.path.join(BASE_DIR, 'static', 'xml')
LONG_WAN_URL = 'http://demo.longwend.com/ocr/api/v1.0/tickets'
TOCKEN = '24b1a094054940dca2e757c893fb7b6e'


class ResultTest(object):
    def __init__(self):
        # 总字符
        self.sum_str = ''
        # 匹配上的字符
        self.correct_str = ''
        # 总字段数
        self.sum_col = len(CORRECT_RESULT)
        # 匹配上的字段数
        self.correct_col = 0

    @staticmethod
    def get_result(file_path):
        files = {
            'image': open(file_path, 'rb'),
        }
        req = requests.post(url=LONG_WAN_URL, files=files, data={'token': TOCKEN})
        try:
            json_data = json.loads(req.text)
            result = json_data['datas'][0]['xml']
        except Exception, e:
            print e
            result == 'bad result'
        return result

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as f:
            data = f.read()
        return data

    @staticmethod
    def find_correct_char(src, dec):
        result_str = ''
        if src:
            for char in src:
                if char in dec:
                    result_str += char
        return result_str

    @staticmethod
    def file_name(files_dir):
        for root, dirs, files in os.walk(files_dir):
            print(root)  # 当前目录路径
            print(dirs)  # 当前路径下所有子目录
            print(files)  # 当前路径下所有非目录子文件

    def check_data(self):
        file_path = os.path.join(IMAGE_DIR, 'skhd.jpg')
        result = self.get_result(file_path)
        # file_path = os.path.join(XML_DIR, 'longwan.xml')
        # result = self.read_file(file_path)
        tree = XmlTree.fromstring(result.encode('utf-8'))
        content = tree.find('content')
        for k, v in CORRECT_RESULT.items():
            k_elem = content.find(k)
            text = k_elem.text if k_elem is not None else ''
            self.sum_str += v
            self.correct_str += self.find_correct_char(text, v) if text else ''
            self.correct_col += 1 if text == v else 0
            # print node.text

    def get_ratio(self):
        self.check_data()
        char_ratio = len(self.correct_str) * 1.0 / len(self.sum_str)
        col_ratio = self.correct_col * 1.0 / self.sum_col
        return char_ratio, col_ratio


if __name__ == u'__main__':
    # test = ResultTest()
    # char_ratio, col_ratio = test.get_ratio()
    #
    # print u'总字符识别度：%s' % char_ratio
    # print u'总字段识别度：%s' % col_ratio
    ResultTest.file_name(BASE_DIR)
