# -*- coding: utf-8 -*-

# @author:  Administrator
# @license: (C) Copyright 2016-2019, Ding dong online.
# @software: PyCharm 
# @file:  __init__.py.py
# @time: 2019-10-24 15:13:09
# @desc:
import os
from util_tools.storage.openpyxl_excel import OpenExcelPandas
from util_tools.storage.read_model_file import ReadModelIni

cd_excel = "cd_excel"
cd_login = "login"
login_excel = "login_excel"
login_sheet = "登录"
login_sheet_two = "登录2"
register_sheet = "注册"
ini_name = "system_excel.ini"
login_browser = "chrome"
login_wait_time = 5


def get_ini_file(excel: str) -> str:
    # 文件参数路径
    argument = ReadModelIni(ini_name)

    # yaml读取用例位置
    login_path = argument.get_value(cd_excel, cd_login)
    module_path = argument.get_value(cd_excel, excel)

    module_excel_path = os.path.join(login_path, module_path)
    return module_excel_path


def excel_to_list(excel: str, sheet: str, title_name: str) -> list:
    """
    读取用例
    :return: 将数据转换成list进行返回
    """
    excel_path = get_ini_file(excel)
    # 读取相应路径中的数据
    read = OpenExcelPandas(name=excel_path, sheet=sheet)
    ex_data = read.internal_read_excel(title_name)
    df_index = ex_data.index
    ex_data = [ex_data.loc[df_i] for df_i in df_index]
    return ex_data


def excel_to_pandas(excel: str, sheet: str, title_name: str) -> object:
    """
    读取用例
    :return: 将数据转换成Pandas进行返回
    """
    excel_path = get_ini_file(excel)
    # 读取相应路径中的数据
    read = OpenExcelPandas(name=excel_path, sheet=sheet)
    ex_data = read.internal_read_excel(title_name)
    # ex_data = [row for row in ex_data.itertuples(index=True)]
    return ex_data
