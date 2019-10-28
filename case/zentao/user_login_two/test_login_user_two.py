# -*- coding: utf-8 -*-

# @author:  Administrator
# @license: (C) Copyright 2016-2019, Ding dong online.
# @software: PyCharm 
# @file:  test_login_user_two.py
# @time: 2019-10-24 15:23:06
# @desc: 通过关联函数名来运行实例

import os
import inspect

import unittest
from case.zentao import user_login

from business.zentao.login import user_login_business
from business.zentao.login.user_login_business import UserLoginBusiness

base_path = os.path.split(os.path.dirname(__file__))[1]
base_name = base_path + "-" + os.path.splitext(os.path.basename(__file__))[0]
excel_data = user_login.excel_to_pandas(user_login.login_excel, user_login.login_sheet_two, '函数')


class TestLoginUserTwo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.business_login = UserLoginBusiness(base_name)

    def setUp(self) -> None:
        self.business_login.create_browser()
        pass

    def tearDown(self) -> None:
        self.business_login.login_page.browser_action.close_driver_browser()
        pass

    def user_login_format(self, method_name):
        # 设置日志需要输出的函数名
        self.business_login.log.fun_name = method_name
        self.business_login.log.info("%s序号的用例开始运行" % method_name)
        # 打印需要输出的内容
        # self.business_login.log.info("用例中所以的内容为:%s" % case)

        # 定义第三方存储对象,可以让其它对象进行调用使用。
        self.business_login.data_case_singe = excel_data.loc[method_name]

        # 运行执行用例需要执行的动作
        self.business_login.user_pass_error()

        self.business_login.log.info("%s序号的用例运行完毕" % method_name)
        pass

    def test_format_error(self):
        self.user_login_format(inspect.stack()[0][3])
        pass

    def test_not_input(self):
        self.user_login_format(inspect.stack()[0][3])
        pass

    def test_input_account(self):
        self.user_login_format(inspect.stack()[0][3])
        pass

    def test_input_password(self):
        self.user_login_format(inspect.stack()[0][3])
        pass

    def test_succeed_skip(self):
        self.user_login_format(inspect.stack()[0][3])
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
