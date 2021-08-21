import os
import unittest
import time

from base import BaseAction
from base.ExcelData import Data

from data.ExcelConfig import TestSteps, Elements, CaseData, TestCases
from base.BaseAction import screenshot_allure, Action
from base.DesireCaps import appium_desired_caps
import ddt
from utils.LogUtil import my_log
from config import Conf
from utils.YamlUtil import YamlReader
import allure

from utils.dbUtil import MysqlConnect

"""
1 重构 代码整理
2 pytest测试用例编写 新建测试文件
3 pytest框架用例执行 run.py pytest.ini

"""

log = my_log("operate")

data = Data(Conf.testcase_file)
# 执行测试用例的列表
run_list = data.run_list()


class Operate():

    def __init__(self,driver):
        self.driver = driver

    def get_keyword(self, name):
        # 1读取配置文件， 文件路径：绝对路径
        keyword_file = Conf.keywords_path
        # 2 YamlReader, data()
        reader = YamlReader(keyword_file).data()
        # 3 key获取值 name
        value = reader[name]
        return value

    def str_to_dict(self, content):
        # 3、字符串转换成字典
        # 1 通过, 分隔得到username=13718418200 password= 123456
        res = {}
        # 2 通过 = 分割
        for i in str(content).split(","):
            # print(i)
            c = i.split("=")
            # print(c)
            res[c[0]] = c[1]
        return res


    def test_run(self, run_case):
        log.info("执行用例内容{}".format(run_case))
        self.step(run_case)

    @screenshot_allure #装饰器
    def step(self, data, run_case):
        tc_id = run_case[TestSteps.STEP_TC_ID]
        # 获取步骤
        steps = data.get_steps_by_tc_id(tc_id)
        # allure 报告
        # feature 一级标题
        allure.dynamic.feature(run_case[TestCases.CASES_NOTE])
        # story 二级标题
        allure.dynamic.story(run_case[TestCases.CASES_DESC])

        # title 标题
        allure.dynamic.title(run_case[CaseData.DATA_CASE_ID] + "-" + run_case[CaseData.DATA_NAME])

        for step in steps:
            log.debug("执行步骤{}".format(step))
            # 获取元素信息
            elements = step[TestSteps.STEP_ELEMENT_NAME]
            element = data.get_elements_by_element(step[TestSteps.STEP_TC_ID], elements)
            log.debug("元素信息{}".format(element))
            # 操作步骤 关键表映射 click_btn
            operate = self.get_keyword(step[TestSteps.STEP_OPERATE])

            # 操作判断，是否存在， 不存在不执行
            if operate:
                # 定义方法参数：字典
                param_value = dict()
                # 根据getattr判断执行那个方法
                action_method = getattr(Action(self.driver), operate)
                log.debug("该关键字是{}".format(operate))

                # 定义具体参数
                by = element[Elements.ELE_BY]
                value = element[Elements.ELE_VALUE]


                # 1、获取by,value,send_value内容
                send_value = step[TestSteps.STEP_DATA]
                send_slid = step[TestSteps.STEP_SLIDE]
                send_COORD = step[TestSteps.STEP_COORD]
                send_note = step[TestSteps.STEP_NOTE]
                send_Keyboard = step[TestSteps.STEP_KEYBOARD]

                # 2、send_value内容转换，通过case data数据内容

                expect = run_case[CaseData.DATA_EXPECT_RESULT]
                param_value["by"] = by
                param_value["value"] = value
                param_value["expect"] = expect
                #映射 自动滑动
                param_value["slid"] = send_slid
                if send_Keyboard:
                    keyboard = int(send_Keyboard)
                    # 模拟键盘按键操作
                    self.driver.keyevent(keyboard)
                    time.sleep(1)
                # 判断 加入有输入 内容 字符转换
                if send_value:
                    data_input = run_case[CaseData.DATA_INPUT]
                    send = self.str_to_dict(data_input)
                    param_value["send"] = send[send_value]
                if send_COORD:
                    slid = self.str_to_dict(send_COORD)
                    # 映射 定位点击
                    param_value["tap"] = slid

                # 数据库拉取验证码进行填写
                if send_note:
                    time.sleep(1)
                    tunnelDB = MysqlConnect('192.168.199.243', 3306, 'cloud', 'Cloud.123456', 'cloud')
                    data_mobile = run_case[CaseData.DATA_INPUT]
                    send1 = self.str_to_dict(data_mobile)
                    param_value["note"] = send_note
                    phone = send1.get("username")

                    if send_note == "注册":
                        # 注册验证码
                        sql = 'SELECT regist FROM t_user_phonecode WHERE phone =%s' % phone
                        results = tunnelDB.select(sql)
                    elif send_note == "登录":
                        # 登陆验证码
                        sql = 'SELECT login FROM t_user_phonecode WHERE phone =%s' % phone
                        results1 = tunnelDB.select(sql)
                        param_value["syk"] = results1[0][0]
                        # 采用按键输入模拟输入验证码
                        if results1[0][0]:
                            for i in results1[0][0]:
                                print(i)
                                i = int(i)
                                if i == 0:
                                    y = 7
                                elif i == 1:
                                    y = 8
                                elif i == 2:
                                    y = 9
                                elif i == 3:
                                    y = 10
                                elif i == 4:
                                    y = 11
                                elif i == 5:
                                    y = 12
                                elif i == 6:
                                    y = 13
                                elif i == 7:
                                    y = 14
                                elif i == 8:
                                    y = 15
                                elif i == 9:
                                    y = 16
                                self.driver.keyevent(y)
                    elif send_note == "找回":
                        # 密码找回验证码
                        sql = 'SELECT passwd_back FROM t_user_phonecode WHERE phone =%s' % phone
                        results = tunnelDB.select(sql)
                    elif send_note == "绑定新手机":
                        # 绑定新手机验证码
                        sql = 'SELECT modify FROM t_user_phonecode WHERE phone =%s' % phone
                        results = tunnelDB.select(sql)
                    if send_note !="登录":
                        note = results[0][0]
                        param_value["send"] = note



                with allure.step(step[TestSteps.STEP_NAME]):
                    action_method(**param_value)
                # 判断 有滑动的进行滑动操作


            else:
                log.error("没有operate信息: {}".format(operate))




# allure定制测试报告
# 1 testcases 备注 feature
# 2 testcases 描述 story
# 3 casedata case_id+用例名称 title
# 4 teststeps 步骤名称 step
