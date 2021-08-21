import os

import pytest
import time
from base.Allure_Report import allure_generate
from base.SendEmail import send_mail
from config import Conf

# 自动生成allure测试报告
report_path = Conf.report_path + os.sep + "result"
report_html = Conf.report_path + os.sep + "html"
if __name__ == '__main__':
    # 自定义参数
    # host="127.0.0.1",port="4723",bpport="4724",udid=None
    # --cmdopt 字典
    cmdopt = {"host": "127.0.0.1",
              "port": "4723",
              "bpport": "4724",
              "udid": "MBJVB20628004068"
    }
    pytest.main(["--cmdopt={}".format(cmdopt)])
    # time.sleep(2)
    # # 生成测试报告路径
    allure_generate(report_path, report_html)
    # time.sleep(3)
    # 发送邮件
    # send_mail(content="发送了一份邮件请查收")

#  实现出错自动拍图、图片与allure合并显示
#  1 结果验证
# 2 断言失败拍图
# 3 图片与allure合并
