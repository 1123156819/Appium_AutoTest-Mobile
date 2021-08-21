import os
import unittest
from base.ExcelData import Data
from data.ExcelConfig import TestSteps, Elements, CaseData, TestCases
from base.BaseAction import Action
from base.DesireCaps import appium_desired_caps
import ddt
import allure
from utils.LogUtil import my_log
from config import Conf
from utils.YamlUtil import YamlReader
from utils.HTMLTestRunner3 import HTMLTestRunner

# 多个用例编写及运行
"""
多个用例参数化可以使用ddt方式，file_data，data
data支持元组、列表、字典，unpack
1、删除无用的代码
2、获取测试用例的列表，[ [H],[H]〕转换[{,{H]修改ExcelData run_list
3、增加新的用例进行参数化运行，调用单条步骤执行方法不修改
4、编写ddt相关代码，ddt.ddt ddt.data不使用unpack方式
5、输出测试报告
6、运行及调试

"""
log = my_log("operate")

data = Data(Conf.testcase_file)
# 执行测试用例的列表
run_list = data.run_list()


@ddt.ddt
class Operate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = appium_desired_caps()

    # 2.2测试用例，执行步骤，先不运行appium，打印excel流，流程确认
    def setUp(self):
        self.driver.launch_app()
        # pass

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

    @ddt.data(*run_list)
    def test_run(self, run_case):
        log.info("执行用例内容{}".format(run_case))
        self.step(run_case)

    def step(self, run_case):
        tc_id = run_case[TestSteps.STEP_TC_ID]
        # 获取步骤
        steps = data.get_steps_by_tc_id(tc_id)
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
                # 2、send_value内容转换，通过case data数据内容

                expect = run_case[CaseData.DATA_EXPECT_RESULT]
                param_value["by"] = by
                param_value["value"] = value

                param_value["expect"] = expect
                # 判断 加入有输入 内容 字符转换
                if send_value:
                    data_input = run_case[CaseData.DATA_INPUT]
                    send = self.str_to_dict(data_input)
                    param_value["send"] = send[send_value]
                action_method(**param_value)
            else:
                log.error("没有operate信息: {}".format(operate))

    def tearDown(self):
        self.driver.close_app()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    suite = unittest.makeSuite(Operate)
    report = Conf.report_path + os.sep + "测试报告.html"
    with open(report, "wb+") as report:
        runner = HTMLTestRunner(stream=report,
                                verbosity=2,
                                title="移动端自动化测试报告",
                                description="关键字驱动测试")
        runner.run(suite)
