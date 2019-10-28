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
@file:      browser_prepare.py
@time:      2018/12/17 16:45
@desc:      浏览器工作
"""
import os

from selenium import webdriver

from util_tools.storage.read_model_file import ReadModelIni

argument = ReadModelIni("system_settings.ini")
driver_path = argument.get_value("driver_browser", "driver_path")
chrome_driver = argument.get_value("driver_browser", "chrome_driver")
ie_driver = argument.get_value("driver_browser", "ie_driver")
firefox_driver = argument.get_value("driver_browser", "firefox_driver")
microsoft_driver = argument.get_value("driver_browser", "microsoft_driver")
del argument


# https://www.cnblogs.com/ppppying/p/6143658.html IE浏览器配置方法文章说明

class BrowserPrepare(object):
    """
    工作内容:
    1. 打开浏览器
    """

    def run_web_browser(self, url: str, driver_browser: str = 'chrome', wait_time: int = 5):
        """
        打开浏览器并进入相应的网址
        :param wait_time:
        :param url:
        :param driver_browser:
        :return:
        """
        self.open_driver_browser(driver_browser, wait_time)
        self.input_browser_url(url)

    def open_driver_browser(self, driver_browser: str = 'chrome', wait_time: int = 5):

        # 创建浏览器对象
        if driver_browser.capitalize() in 'Chrome':
            self.chrome_browser()
        elif driver_browser.capitalize() in 'Firefox':
            self.firefox_browser()
        elif driver_browser.capitalize() in 'Edge':
            self.edge_browser()
        else:
            self.ie_browser()
        # 浏览器窗口最大化,程序运行过程中有些问题就是因为窗口没有最大化导致的.
        self.driver.maximize_window()
        # 等待网页加载，加载时间为10s，加载完就跳过
        # 隐形等待时间和显性等待时间不同时，默认使用两者之间最大的那个
        self.driver.implicitly_wait(wait_time)
        pass

    def input_browser_url(self, url: str):
        # 输入网址
        self.driver.get(url)
        pass

    def close_driver_browser(self, _quit=None):
        # 关闭并退出浏览器
        self.driver.quit()
        pass

    def chrome_browser(self):
        """
        调用函数，实现打开谷歌浏览器的步骤
        :return:
        """
        self.driver = webdriver.Chrome(executable_path=os.path.join(driver_path, chrome_driver))

    def ie_browser(self):
        """
        调用函数，实现打开ie浏览器的步骤
        :return:
        """
        # 实现全局变量的引用
        self.driver = webdriver.Ie(executable_path=os.path.join(driver_path, ie_driver))

    def edge_browser(self):
        """
        调用函数，实现打开edge浏览器的步骤
        :return:
        """
        # 实现全局变量的引用
        self.driver = webdriver.Edge(executable_path=os.path.join(driver_path, microsoft_driver))

    def firefox_browser(self, options=None):
        """
        调用函数，实现打开火狐浏览器的步骤
        :return:
        """

        # 实现全局变量的引用,当火狐安装路径不为默认路径时（即C盘）才需要填写firefox_bin
        firefox_bin = os.path.abspath(r"E:\Program Files\Mozilla Firefox\firefox.exe")
        os.environ["webdriver.firefox.bin"] = firefox_bin

        # 代码加载火狐驱动
        firefox_driver_path = os.path.abspath(os.path.join(driver_path, firefox_driver))
        self.driver = webdriver.Firefox(options, executable_path=firefox_driver_path)

    def mobile_phone_mode(self):
        '''
        将谷歌浏览器设置为手机模式
        :return:
        '''
        from selenium.webdriver.chrome.options import Options
        # 有效的移动设备Galaxy S5.Nexus 5X.Nexus 6P
        # mobile_emulation = {"deviceName": "iPhone 7"}

        mobile_emulation = {
            "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"}

        # mobile_emulation = {"browserName": "IE"}
        options = Options()
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        return options

    def chrome_prefs_flash(self):
        '''
        当谷歌浏览器运行时，不会加载flash
        :return:
        '''
        from selenium.webdriver.chrome.options import Options

        prefs = {
            "profile.managed_default_content_settings.images": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1
        }

        options = Options()
        options.add_experimental_option("prefs", prefs)
        return options

    def firefox_prefs_flash(self):
        '''
        当firefox运行时，flash不会加载
        :return:
        '''
        options = webdriver.FirefoxProfile()
        # 其中plugin.state.flash后的数值可以为0,1,2； 0：禁止，1：询问，2：允许。
        options.set_preference("plugin.state.flash", 2)
        return options

