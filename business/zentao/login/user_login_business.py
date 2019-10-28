# -*- coding: utf-8 -*-

# @author:  Administrator
# @license: (C) Copyright 2016-2019, Ding dong online.
# @software: PyCharm 
# @file:  user_login_business.py
# @time: 2019-10-24 15:34:25
# @desc:

from selenium.webdriver.support import expected_conditions as EC

from util_tools.logger import Logger
from util_tools.storage.read_model_file import ReadModelIni
from pages.zentao.login.user_login_page import UserLoginPage
from case.zentao import user_login


class UserLoginBusiness(object):

    def __init__(self, base_name: str):
        """
        实例化对象,并且创建日志对象及元素操作对象
        :param base_name:  用例运行类类名
        """
        self.log = Logger(base_name)
        self.login_page = UserLoginPage()
        pass

    # ----------------- 将set跟get封装后由单个参数来实现 -----------------
    def set_case(self, case):
        self.case = case
        pass

    def get_case(self):
        return self.case

    data_case_singe = property(get_case, set_case, doc="找不到内容")

    # -----------------  -----------------
    def create_browser(self):
        # 获取需要打开的url
        argument = ReadModelIni("system_settings.ini")
        login_url = argument.get_value("wap_url", "zen_tao_url")
        self.log.info("浏览器url :" + login_url)

        # 创建浏览器对象，并打开
        self.login_page.browser_action.run_web_browser(login_url, user_login.login_browser, user_login.login_wait_time)
        self.log.info("%s浏览器已经打开,显示时间为%ss" % (user_login.login_browser, user_login.login_wait_time))

    def user_pass_error(self):
        # 执行账号输入操作
        self.login_page.input_user_name(self.data_case_singe["账号"])
        # 执行密码输入操作
        self.login_page.input_pass_word(self.data_case_singe["密码"])
        # 判断是否需要点击登录按钮
        login_button = self.data_case_singe["登录"]
        if login_button.capitalize() in 'Y':
            # 执行点击操作
            self.login_page.click_login_button()
            # 判断点击登录后的情况
            login_follow = self.data_case_singe["后续"]
            login_follow_label, login_follow_info = login_follow.split("-->")
            if 'error' in login_follow_label:
                # 账号密码错误时,提示语的判断。
                attr_text = self.login_page.get_form_error()
                assert attr_text in login_follow_info, "登录失败时,提示语判断错误。"
                self.log.info("登录失败的原因为:%s" % login_follow_info)
                pass
            elif 'go' in login_follow_label:
                # 点击登录后跳转的页面
                assert EC.title_contains(login_follow_info), "页面已经发生跳转并不在登录页面"
                pass
            else:
                self.log.info("点击登录后,excel中的后续编写有误:%s" % login_follow)
                pass
        else:
            self.log.info("不需要点击登录按钮")
        pass

    pass
