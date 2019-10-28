# -*- coding: utf-8 -*-

# @author:  Administrator
# @license: (C) Copyright 2016-2019, Ding dong online.
# @software: PyCharm 
# @file:  user_login_page.py
# @time: 2019-10-24 16:44:05
# @desc:


from util_tools.operation.action_interface import ActionParsing


class UserLoginPage(object):
    def __init__(self):
        self.browser_action = ActionParsing()
        pass

    def input_user_name(self, parameter) -> None:
        """
         返回账号元素的类型及路径
        :return:
        """
        account = "id>>account"
        self.browser_action.is_input_execute(account, parameter)
        pass

    def input_pass_word(self, parameter) -> None:
        """
        返回密码元素的类型及路径
        :return:
        """
        pass_word = "css>>input[type=password]"
        self.browser_action.is_input_execute(pass_word, parameter)
        pass

    def click_login_button(self) -> None:
        """
        返回登录按钮元素的类型及路径
        :return:
        """
        button = "css>>.btn.btn-primary"
        self.browser_action.is_click_execute(button)
        pass

    def get_form_error(self) -> str:
        """
        返回登录错误时系统弹窗提示语的类型及路径
        :return:
        """
        # form_error = "id>>formError"
        # attr_text = self.browser_action.get_text_value(form_error)
        # 获取弹窗对象
        alert_pupop = self.browser_action.driver.switch_to.alert
        # 获取弹窗内容
        alert_text = alert_pupop.text
        # 点击弹窗中的确定按钮
        alert_pupop.accept()
        return alert_text

    pass
