# coding:utf-8
import os
import sys
import time
import datetime
import unittest
import HTMLTestRunner

# git config --global user.name “用户名”

# git config --global user.email “邮箱”


# 获取项目路径下的目录
path_project = os.path.split(os.path.abspath(__file__))[0]
os.chdir(path_project)

# 将项目路径保存
sys.path.append(path_project)

# 获取当前文件所在目录
CUR_PATH = os.path.dirname(os.path.realpath(__file__))

# 设置时间格式
day_now = time.strftime("%Y-%m-%d")
time_now = time.strftime("%H-%M-%S")


def add_case(case_name='Case', rule='test*.py'):
    # 加载所有的用例
    case_path = case_name
    # case_path = os.path.join(CUR_PATH,case_name)
    # 定义方法的参数
    discover = unittest.defaultTestLoader.discover(case_path,
                                                   pattern=rule,
                                                   top_level_dir=CUR_PATH)
    print("用例所在位置 %s  执行的文件 %s " % (case_path, rule))
    return discover


def run_case(all_case, reportName='report', filename="filename"):
    # 1.1报告存放路径
    report_path = os.path.join(os.getcwd(), reportName)

    # 1.2报告根据时间来分类
    report_path = os.path.join(report_path, day_now)
    if not os.path.exists(report_path): os.mkdir(report_path)

    filename = "%s-%s.html" % (time_now, filename)
    report_abspath = os.path.join(report_path, filename)

    print("新创建报告文件所在位置 %s " % report_abspath)

    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title=u'自动化测试报告测试结果如下：',
                                           description=u'用例执行情况：')

    # 调用add_case函数返回值
    runner.run(all_case)
    fp.close()


def get_report_file(report_path):
    # 获取最新的测试报告
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    print("最新报告名 %s" % lists[-1])

    # 找到最新生成的报告文件
    report_file = os.path.join(report_path, lists[-1])
    return report_file


def run_main(file_name, rule='test*.py'):
    # 加载用例
    all_case = add_case(file_name, rule)

    # 运行文件所在目录为文件名
    file_name = str.split(file_name, '\\')[-1]

    # 生成测试报告的路径
    run_case(all_case, filename=file_name)

    # 获取最新测试报告所在的文件路径

    report_path = os.path.join("report", day_now)  # 最新报告文件夹在项目中的路径
    report_path = os.path.join(CUR_PATH, report_path)  # 拼接项目

    # 获取最新的测试报告
    report_file = get_report_file(report_path)
    print("最新报告路径为{0}".format(report_file))


def list_dir(file_dir):
    '''
        通过 listdir 得到的是仅当前路径下的文件名，不包括子目录中的文件，如果需要得到所有文件需要递归
    '''
    # print('\n\n<><><><><><> listdir <><><><><><>')
    # print("current dir : {0}".format(file_dir))
    file_dir = os.path.join(CUR_PATH, file_dir)
    dir_list = os.listdir(file_dir)
    file_name = []
    for cur_file in dir_list:
        # 获取文件的绝对路径
        path = os.path.join(file_dir, cur_file)
        if os.path.isfile(path):  # 判断是否是文件还是目录需要用绝对路径
            # print("{0} : is file!".format(cur_file))
            continue
        if os.path.isdir(path):
            # print("{0} : is dir!".format(cur_file))
            list_dir(path)  # 递归子目录
            file_name.append(cur_file)
    return file_name


def start_loading_case():
    file_name = r'case'
    all_dir = list_dir(file_name)

    for dir in range(len(all_dir)):
        if "__pycache__" in all_dir[dir]:
            continue
        else:
            dir = os.path.join(file_name, all_dir[dir])
            print("需要运行的文件: %s" % dir)
            run_main(dir)


def start_single_loading():
    run_main('demo', "test_*.py")


if __name__ == '__main__':
    # 记录运行时间
    startTime = datetime.datetime.now()
    print("\nStart Run Time: %s\n" % startTime)
    # 指定case所在位置并自动运行位置下需要运行的test文件夹,并且每个文件夹都自动生成一个相应的html报告
    start_loading_case()
    # 指定需要运行的test文件夹，运行完毕之后只生成一个相应的html报告
    # start_single_loading()
    # 记录结束时间
    stopTime = datetime.datetime.now()
    print("\nFinish Run Time: %s\n" % stopTime)
    # 打印一共运行的时间
    print('\nRunning time: %s\n' % (stopTime - startTime), file=sys.stderr)
