import pytest


from base.DesireCaps import appium_desired_caps
from base.ExcelData import Data
from config import Conf
from utils.LogUtil import my_log
from testcase.operate.KeywordOperatePytest import Operate

log = my_log("TestKeywords")

data = Data(Conf.testcase_file)
# 执行测试用例的列表
run_list = data.run_list()


# 1创建测试用例方法
class TestKeyword:
    # def test_run(self, test123):
    #     pass
    # def setup_class(self):
    #     self.driver = appium_desired_caps()
    #
    # #启动
    # def setup(self):
    #     self.driver.launch_app()

    @pytest.mark.parametrize("run_case", run_list)
    def test_run(self, start_appium_desired, run_case):
        self.driver = start_appium_desired
        self.driver.launch_app()

        log.info("执行用例内容{}".format(run_case))
        Operate(self.driver).step(data, run_case)

    # 2 重构代码
    # 3 增加setup teardown

    def teardown(self):

        self.driver.close_app()


    # def teardown_class(self):
    #     self.driver.quit()
    #
