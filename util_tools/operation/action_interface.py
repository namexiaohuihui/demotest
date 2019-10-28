# -*- coding: utf-8 -*-
"""
                       _oo0oo_
                      o8888888o
                      88" . "88
                      (| -_- |)
                      0\  =  /0
                    ___/`---'\___
                  .' \\|     |// '.
                 / \\|||  :  |||// \
                / _||||| -:- |||||- \
               |   | \\\  -  /// |   |
               | \_|  ''\---/''  |_/ |
               \  .-\__  '-'  ___/-. /
             ___'. .'  /--.--\  `. .'___
          ."" '<  `.___\_<|>_/___.' >' "".
         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
         \  \ `_.   \_ __\ /__ _/   .-` /  /
     =====`-.____`.___ \_____/___.-`___.-'=====
                        `=---='


     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

               佛祖保佑         永无BUG
@author:    hz_company
@license:   (C) Copyright 2016- 2018, Node Supply Chain Manager Corporation Limited.
@Software:  PyCharm
@file:      action_interface.py
@time:      2018/12/17 17:07
@desc:
"""
import inspect
from time import sleep

import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By

from util_tools.logger import Logger

from util_tools.operation.browser_prepare import BrowserPrepare


# readModel
class ActionVisible(BrowserPrepare):
    """
    工作内容:
    1.执行元素校验动作 = [click,input,visible]
    """

    def __init__(self):
        self.log = Logger('ActionVisible')
        pass

    def is_visible_driver(self, locator: str, way: str) -> ():
        """
        根据类型定义相应的by元素对象
        :param locator:     元素路径
        :param way:     元素类路径类型
        :return:
        """
        by_ele = {"Css": 'CSS_SELECTOR', "Id": 'ID', "Xpath": 'XPATH', "Name": 'NAME'}
        # capitalize不区分大小写
        if way.capitalize() in by_ele.keys():
            ele_by = by_ele.get(way.capitalize())
            ele_by = getattr(By, ele_by)
            ele_by = (ele_by, locator)
        else:
            ele_by = None
        del by_ele
        return ele_by

    def differentiate_all_exist(self, ele_by, timeout=10):
        """
        根据某个元素路径,返回符合该路径的全部元素
        :param ele_by: 在is_visible_driver中返回的元素by属性
        :param timeout: 元素查找时间,默认为5s
        :return:
        """
        try:
            ele = ui.WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(ele_by))
            return ele
        except Exception as e:
            fun_name = inspect.stack()[0][3]
            print("%s发生错误%s,元素对象为%s" % (fun_name, e, ele_by))
            return False

    def prompt_all_exist(self, prompt, ele_by, timeout=5):
        try:
            ele = ui.WebDriverWait(prompt, timeout).until(
                EC.visibility_of_all_elements_located(ele_by))
            return ele
        except Exception as e:
            fun_name = inspect.stack()[0][3]
            print("%s发生错误%s,元素对象为%s" % (fun_name, e, ele_by))
            return False

    def differentiate_single_exist(self, ele_by, timeout=5):
        """
        根据某个元素路径,第一个符合该路径的元素
        :param ele_by: 在is_visible_driver中返回的元素by属性
        :param timeout: 元素查找时间,默认为5s
        :return:
        """
        try:
            ele = ui.WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(ele_by))
            return ele
        except Exception as e:
            fun_name = inspect.stack()[0][3]
            print("%s发生错误%s,元素对象为%s" % (fun_name, e, ele_by))
            return False

    def differentiate_not_exist(self, ele_by, timeout=5):
        """
        识别某个元素是否从界面上消失
        :param ele_by:在is_visible_driver中返回的元素by属性
        :param timeout:
        :return:
        """
        try:
            ui.WebDriverWait(self.driver, timeout).until_not(EC.element_to_be_clickable(ele_by))
            return True
        except Exception as e:
            fun_name = inspect.stack()[0][3]
            print("%s发生错误%s,元素对象为%s" % (fun_name, e, ele_by))
            return False

    def is_visible_single_driver(self, ele_para, timeout=5):
        """
        识别某个元素是否加载完毕
        :param ele_para: 元素路径 和 元素类型 的组合
        :param timeout: 查找元素的超时时间
        :return:
        """
        way, locator = ele_para.split(">>")
        ele_by = self.is_visible_driver(locator, way)
        return self.differentiate_single_exist(ele_by, timeout)

    def is_visible_all_driver(self, ele_para, timeout=5):
        """
        识别元素路径相同的全部元素
        :param ele_para:
        :param timeout:
        :return:
        """
        way, locator = ele_para.split(">>")
        ele_by = self.is_visible_driver(locator, way)
        return self.differentiate_all_exist(ele_by, timeout)

    def is_visible_all_prompt(self, prompt, locator, way, timeout=5):
        """
        识别元素路径相同的全部元素
        :param prompt:
        :param locator:
        :param way:
        :param timeout:
        :return:
        """
        ele_by = self.is_visible_driver(locator, way)
        return self.prompt_all_exist(prompt, ele_by, timeout)

    def is_visible_not_driver(self, locator, way, timeout=5):
        """
        判断某个元素是否消失
        :param locator:
        :param way:
        :param timeout:
        :return:
        """

        ele_by = self.is_visible_driver(locator, way)
        return self.differentiate_not_exist(ele_by, timeout)

    def is_visible_click(self, prompt):
        """
        执行点击操作
        :param prompt:
        :return:
        """
        prompt.click()
        sleep(1)

    def is_visible_input(self, attribute, parameter):
        """
        统一封装元素输入操作
        :param attribute: 元素对象
        :param parameter: 输入内容
        :return:
        """
        self.set_action_funname(inspect.stack()[0][3])
        attribute.click()
        attribute.clear()
        attribute.send_keys(parameter)
        self.log.info("输入的信息(%s)" % parameter)
        sleep(1)

    def set_action_funname(self, fun_name):
        self.log.fun_name = fun_name


class ActionParsing(ActionVisible):
    """
    主要实现selenium一些内置的动作封装
    例如：
        元素输入
        元素点击
        返回元素值
    """

    def is_input_execute(self, ele_para, parameter, timeout=5):
        """
        通过元素类型来找到元素,并输入内容
        :param ele_para:  元素路径
        :param parameter:  需要输入的内容
        :param timeout: 元素查找时间
        :return:
        """
        attribute = self.is_visible_single_driver(ele_para, timeout)
        self.is_visible_input(attribute, parameter)
        self.log.info("%s元素输入内容为%s" % (ele_para, parameter))

    def is_click_execute(self, ele_para, timeout=5):
        """
        通过元素类型来找到元素并执行点击操作
        :param ele_para:  元素路径
        :param timeout: 元素查找时间
        :return:
        """
        attribute = self.is_visible_single_driver(ele_para, timeout)
        self.is_visible_click(attribute)
        self.log.info("%s元素进行点击操作" % ele_para)

    def get_text_value(self, ele_para: str, attr: str = None, timeout: int = 5) -> str:
        """
        获取元素的text或者attribute
        :param ele_para:  元素路径
        :param attr:  为none时获取元素text,不为空时获取元素的attribute属性值
        :param timeout: 元素可见超时时间
        :return:
        """
        attribute = self.is_visible_single_driver(ele_para, timeout)
        if type(attribute) is bool:
            return attribute
        else:
            if attr:
                attribute = attribute.get_attribute(attr)
            else:
                attribute = attribute.text
        self.log.info("%s元素获取(%s)属性值为%s" % (ele_para, attr, attribute))
        return attribute


class ActionBuiltWeb(ActionVisible):
    """
    通过web内置的js来做操作。
    例如：
        元素查找
        元素点击
        元素输入
        聚焦及移除焦点
    """

    def cursor_execute_id(self, locator, parameter):
        """
        利用js找到相关id的元素,直接对value进行数据修改
        :param locator: 元素对象
        :param parameter: 输入内容
        :return:
        """
        self.driver.execute_script("document.getElementById(\'" + locator + "\').value=\'" + parameter + "\';")
        sleep(1)

    def cursor_execute_ordinal(self, cursor, parameter):
        """
         根据元素对象本身,通过JS对value进行写入
        :param cursor:  元素对象本身
        :param parameter:   需要输入的信息
        :return:
        """
        self.driver.execute_script("\'" + cursor + "\'.value=\'" + parameter + "\';")
        sleep(1)

    def cursor_execute_selectop(self, locator, parameter):
        """
        利用js找到相关selctop的元素,直接对value进行数据修改
        :param locator: 元素对象
        :param parameter: 输入内容
        :return:
        """
        self.driver.execute_script("document.querySelector(\'" + locator + "\').value=\'" + parameter + "\';")
        sleep(1)

    def id_confirm_execute(self, locator):
        """
        利用js语法通过id执行点击操作
        :param locator:     元素属性中,ID的属性值
        :return:
        """
        self.driver.execute_script("document.getElementById(\'" + locator + "\').click();")
        pass

    def css_confirm_execute(self, locator):
        """
        利用js语法通过元素selector执行点击操作
        :param locator: 元素属性中,selector的属性值
        :return:
        """
        self.driver.execute_script("document.querySelector(\'" + locator + "\').click();")
        pass

    def attribute_focus_blur(self, ele_attr, cursor_type):
        """
        通过元素id,实现元素获取焦点及失去焦点的操作
        :param ele_attr:    元素的id
        :param cursor_type: 聚焦或失焦
        :return:
        """
        if 'blur' == cursor_type:
            self.driver.execute_script("document.getElementById(\'" + ele_attr + "\').blur();")
            pass
        elif 'focus' == cursor_type:
            self.driver.execute_script("document.getElementById(\'" + ele_attr + "\').focus();")

    def cursor_focus_blur(self, ele_attr, cursor_type: str):
        """
        根据元素对象本身来实现元素获取焦点及失去焦点的操作
        :param ele_attr:  元素对象
        :param cursor_type:  focus聚焦或blur失焦
        :return:
        """
        if 'blur' == cursor_type:
            self.driver.execute_script("arguments[0].blur();", ele_attr)
            pass
        elif 'focus' == cursor_type:
            self.driver.execute_script("arguments[0].focus();", ele_attr)
