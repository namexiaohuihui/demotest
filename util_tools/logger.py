# -*- coding: utf-8 -*- 
"""
@__author__ :70486 
@file: logger.py
@time: 2017/12/21 22:02
@项目名称:operating
"""
import logging
import os
import pprint
import time

# log_path是存放日志的路径
cur_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(cur_path, 'logs')

# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path): os.mkdir(log_path)


class Logger(object):

    def __init__(self, executor: str = "Root", classification: str = 'Journal') -> None:
        """
        日志函数在实例化的声明内部参数
        :param executor:  日志使用者
        :param classification:  日志文件名字前缀
        """
        # 文件的命名
        self.logname = os.path.join(log_path, classification + '-%s.log' % time.strftime('%Y_%m_%d'))

        # 定义执行者的名字
        self.logger = logging.getLogger(executor)

        # 设置输入语句的等级
        self.logger.setLevel(logging.DEBUG)

        # 日志输出格式
        # self.formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(filename)s] - %(levelname)s: %(message)s')
        self.formatter = logging.Formatter('[%(asctime)s] - %(name)s] - %(levelname)s: %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')

        # 定义执行函数的名字供外部进行调用和修改
        self.fun_name = "Undefined_Function"

    def log_write_file(self) -> logging.FileHandler:
        """
        创建一个FileHandler，将日志写到本地文件中
        :return: logging.FileHandler
        """
        # fh = logging.FileHandler(self.logname, 'a')  # 追加模式  这个是python2的
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')  # 这个是python3的

        # 大于等于该错误等级的才被写入到日志文件
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        return fh

    def log_output_console(self) -> logging.StreamHandler:
        """
        创建一个StreamHandler,用于输出到控制台
        :return: logging.StreamHandler
        """
        ch = logging.StreamHandler()

        # 大于等于该错误等级的才被输出到控制台
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)
        return ch

    def __console(self, level, message):
        # 写入文件的定义
        fh = self.log_write_file()

        # 输出到控制的定义
        ch = self.log_output_console()

        level = getattr(self.logger, level)
        level(message)

        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)

        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', "%s---%s" % (self.function, message))

    def info(self, message):
        self.__console('info', "%s---%s" % (self.function, message))

    def warning(self, message):
        self.__console('warning', "%s---%s" % (self.function, message))

    def error(self, message):
        self.__console('error', "%s---%s" % (self.function, message))

    def critical(self, message):
        self.__console('critical', "%s---%s" % (self.function, message))

    def set_function_name(self, function_name):
        self.function = function_name

    def get_function_name(self):
        return self.function

    def log_ppriny(self, message):
        pprint.pprint(message)

    fun_name = property(get_function_name, set_function_name, doc="log获取的时候出错了")
