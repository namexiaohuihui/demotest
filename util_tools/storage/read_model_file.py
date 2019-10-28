# -*- coding: utf-8 -*-

# @author:  hz_company
# @license: (C) Copyright 2016-2019, Node Supply Chain Manager Corporation Limited.
# @software: PyCharm
# @file:  read_model.py
# @time: 2019/4/10 11:56
# @Software: PyCharm
# @Site    : 
# @desc:
import os

import yaml
import configparser


class ReadModelIni(object):
    """
    读取ini文件
    """

    def __init__(self, file_name: str, file_path: str = None) -> None:
        """
        实例化ini文件读取对象
        :param file_name:  需要读取的文件名字,需要传入文件后缀名
        :param file_path:  需要读取的文件所在路径
        """
        self.conf = None
        # 判断文件位置是否传入
        if file_path:
            self.file_path = file_path
        else:
            # 此处写死的原因:配置文件所在的目录跟项目代码目录不为同一个地址
            self.file_path = os.path.join("E:\\hezhan", 'configs')

        # 给内部参数file_name赋值
        self.file_name = file_name

        config_path = os.path.join(self.file_path, self.file_name)
        self.read_ini_file(config_path)
        pass

    def read_ini_file(self, config_path):
        """
        将ini文件内的数据转成dict
        :param config_path:  需要读取的ini文件
        :return:
        """

        self.conf = configparser.ConfigParser()
        self.conf.read(config_path)
        # s = self.conf.sections()
        # print('section:', s)
        # o = self.conf.options("driver_browser")
        # print('options:', o)

    pass

    def get_value(self, section, key):
        """
        通过key值获取相应的数据信息
        :param section:
        :param key:
        :return:
        """
        try:
            value = self.conf.get(section, key)
        except Exception as e:
            value = None
            print(e)
        return value


class ReadModelYaml(object):
    """
    读取yaml文件数据
    """

    def __init__(self, file_name, file_path=None):
        """
        实例化yaml文件读取对象
        :param file_name:  需要读取的文件名字,需要传入文件后缀名
        :param file_path:  需要读取的文件所在路径
        """

        # 判断文件位置是否传入
        self.pageElements = {}
        if file_path:
            self.file_path = file_path
        else:
            cur_path = os.path.abspath(os.path.dirname(os.getcwd()))
            self.file_path = os.path.join(cur_path, 'configs')

        self.file_name = file_name

        yaml_file_path = os.path.join(self.file_path, self.file_name)
        self.read_parse_yaml(yaml_file_path)

    def read_parse_yaml(self, yaml_file_path):
        """
        指定文件路径以及文件名来读取数据信息
        :param yaml_file_path:  文件路径
        :return:
        """
        # 排除一些非.yaml的文件
        if '.yaml' in str(yaml_file_path):
            with open(yaml_file_path, 'r', encoding='utf-8') as f:
                page = yaml.load(f)
                self.pageElements.update(page)

    def get_value(self, key):
        """
        根据key来获取数据信息
        :param key:
        :return:
        """
        try:
            value = self.pageElements[key]
        except Exception as e:
            value = None
            print("ReadModelYaml 读取时没有找到关键字%s----%s" % (key, e))
        return value

