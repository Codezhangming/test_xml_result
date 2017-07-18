# -*- coding:utf-8 -*-
'''
  文 件 名   : .py
  版 本 号   : 初稿
  作    者   : 张茗 
  生成日期   : 2017年3月31日
  最近修改   :
  功能描述   : 
  函数列表   : 
  修改历史   :
    1、日    期   : 2017年3月31日
       作    者   : 张茗
       修改内容   : 创建文件

'''
import os


# 获取常量的基类
class BaseConstant(object):

    def get_constant(self, constant_name):
        return getattr(self, constant_name, None)

# 文件路径统一在这里配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONSTANT_DIR = os.path.join(BASE_DIR, 'constant_cofing')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
IMAGE_DIR = os.path.join(STATIC_DIR, 'image')
XML_DIR = os.path.join(STATIC_DIR, 'xml')


# 龙湾相关的常量在这里配置
URL = ''
TOCKEN = ''

# 输出信息
PRINT_INFO_CHAR = u'总字符识别度：{ratio}'
PRINT_INFO_COL = u'总字段识别度：{ratio}'
