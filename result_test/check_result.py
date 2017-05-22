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
import requests
from xml.etree import ElementTree as XmlTree
import sys
from constant_cofing.constant import *

sys.path.append(CONSTANT_DIR)


class ResultTest(object):
    def __init__(self):
        '''
                self.result = {'all': '',
                       'dir': {
                           'dir_name': {
                               'all': {'char_ratio': '',
                                       'col_ratio': ''},
                               'file1': {
                                   'char_ratio': '',
                                   'col_ratio': ''
                               }
                           },
                       }}
        '''
        self.result = {'dir': {}}

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

    @staticmethod
    def check_data(dir_name, file_name):
        constant_name = os.path.split(file_name)[-1].split('.')[0]
        constant_module = __import__(dir_name)
        CORRECT_RESULT = constant_module.GetConstant().get_constant(constant_name)
        # 总字符
        sum_str = ''
        # 匹配上的字符
        correct_str = ''
        # 匹配上的字段数
        correct_col = 0
        # 调用接口获取数据（测试张图片）
        file_path = os.path.join(IMAGE_DIR, file_name)
        result = ResultTest.get_result(file_path)

        # 读xml获取数据
        # file_path = os.path.join(XML_DIR, 'longwan.xml')
        # result = read_file(file_path)
        tree = XmlTree.fromstring(result.encode('utf-8'))
        content = tree.find('content')
        for k, v in CORRECT_RESULT.items():
            if not v:
                del CORRECT_RESULT[k]
                continue
            try:
                k_elem = content.find(k)
            except KeyError,e:
                print e
                print '{fileName} was lack columns: {colName}'.format(fileName=os.path.split(file_name)[-1], colName=k)
                print '---------------------------------------------------------------------'
                continue
            text = k_elem.text if k_elem is not None else ''
            if text == '':
                print '{fileName} '
            sum_str += v
            correct_str += ResultTest.find_correct_char(text, v) if text else ''
            if text == v:
                correct_col += 1
            else:

                print '{fileName} was lack columns: {colName}'.format(fileName=os.path.split(file_name)[-1], colName=k)
                print '---------------------------------------------------------------------'
            # print node.text
        char_ratio = len(correct_str) * 1.0 / len(sum_str)
        col_ratio = correct_col * 1.0 / len(CORRECT_RESULT)
        return char_ratio, col_ratio

    @staticmethod
    def get_abspath(file_name):
        abspath = os.path.abspath(file_name)
        return abspath

    @staticmethod
    def set_dir_file_dict(dir_file_dict, file_name):
        dirname = os.path.split(os.path.dirname(file_name))[-1]
        if dir_file_dict.has_key(dirname):
            dir_file_dict[dirname].append(file_name)
        else:
            dir_file_dict[dirname] = [file_name]

        return dir_file_dict

    @staticmethod
    def collect_files(files_dir):
        file_list = []
        for root, dirs, files in os.walk(files_dir):
            # file_list += map(ResultTest.get_abspath, files)
            for file in files:
                file_abs_path = os.path.join(root, file)
                file_list.append(file_abs_path)
                # char_ratio, col_ratio = ResultTest.check_data()
                # print PRINT_INFO_CHAR.format(ratio=char_ratio)
                # print PRINT_INFO_COL.format(ratio=col_ratio)
                # print(root)  # 当前目录路径
                # print(dirs)  # 当前路径下所有子目录
                # print(files)  # 当前路径下所有非目录子文件

        return file_list

    def get_ratio(self, image_dir):
        dir_file_dict = {}
        all_char_ratio = 0
        all_col_ratio = 0
        dir_count = 0
        files = self.collect_files(image_dir)
        for file in files:
            dir_file_dict = self.set_dir_file_dict(dir_file_dict, file)
        for dir_name, dir_file_list in dir_file_dict.items():
            dir_char_ratio = 0
            dir_col_ratio = 0
            dir_count += 1
            file_count = 0
            self.result['dir'][dir_name] = {}
            for file in dir_file_list:
                char_ratio, col_ratio = ResultTest.check_data(dir_name, file)
                print 'image %s : ' % file
                print PRINT_INFO_CHAR.format(ratio=char_ratio)
                print PRINT_INFO_COL.format(ratio=col_ratio)
                dir_char_ratio += char_ratio
                dir_col_ratio += col_ratio
                file_count += 1
                self.result['dir'][dir_name][file] = {'char_ratio': char_ratio, 'col_ratio': col_ratio}
            dir_char_ratio = dir_char_ratio / file_count if file_count else 0
            dir_col_ratio = dir_col_ratio / file_count if file_count else 0
            self.result['dir'][dir_name]['dir'] = {'char_ratio': dir_char_ratio, 'col_ratio': dir_col_ratio}
            all_char_ratio += dir_char_ratio
            all_col_ratio += dir_col_ratio

        self.result['all'] = {'char_ratio': all_char_ratio / dir_count if dir_count else 0,
                              'col_ratio': all_col_ratio / dir_count if dir_count else 0}
        return self.result


if __name__ == u'__main__':
    # test = ResultTest()
    # char_ratio, col_ratio = test.get_ratio()
    #
    # print u'总字符识别度：%s' % char_ratio
    # print u'总字段识别度：%s' % col_ratio

    data = ResultTest().get_ratio(IMAGE_DIR)
    print data
