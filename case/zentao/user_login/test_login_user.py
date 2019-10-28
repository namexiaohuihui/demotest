# -*- coding: utf-8 -*-

# @author:  Administrator
# @license: (C) Copyright 2016-2019, Ding dong online.
# @software: PyCharm 
# @file:  test_login_user.py
# @time: 2019-10-24 15:23:06
# @desc: 通过数据驱动的模式运行用例

import os
import inspect

import unittest
import ddt

from case.zentao import user_login
from business.zentao.login.user_login_business import UserLoginBusiness

base_path = os.path.split(os.path.dirname(__file__))[1]
base_name = base_path + "-" + os.path.splitext(os.path.basename(__file__))[0]

excel_data = user_login.excel_to_list(user_login.login_excel, user_login.login_sheet, '序号')


@ddt.ddt
class TestLoginUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.business_login = UserLoginBusiness(base_name)
        pass

    def setUp(self) -> None:
        self.business_login.create_browser()
        pass

    def tearDown(self) -> None:
        self.business_login.login_page.browser_action.close_driver_browser()
        pass


    @ddt.data(*excel_data)
    def test_run_login(self, case):
        self.business_login.log.info("%s序号的用例开始运行" % case["序号"])

        # 设置日志需要输出的函数名
        self.business_login.log.fun_name = "%s-%s" % (inspect.stack()[0][3], case["序号"])

        # 打印需要输出的内容
        # self.business_login.log.info("用例中所以的内容为:%s" % case)

        # 定义第三方存储对象,可以让其它对象进行调用使用。
        self.business_login.data_case_singe = case

        # 运行执行用例需要执行的动作
        self.business_login.user_pass_error()

        self.business_login.log.info("%s序号的用例运行完毕" % case["序号"])
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
    del excel_data
