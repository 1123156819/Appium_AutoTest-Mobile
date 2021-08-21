import pytest

from base.DesireCaps import appium_desired_caps
from base.StartAppium import get_devices, appium_start, check_port
import time


# 1、定义命令选项
def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store", default="run", help=None)


# 2、接收命令
@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--cmdopt")


# 3、调用命令使用
@pytest.fixture(scope="session")
def start_appium_desired(cmdopt):

    opt = eval(cmdopt)
    # # {"host":"127.0.0.1",
    # #          "port":"4723",
    # #          "bpport":"4724",
    # #         "udid":None}
    host = opt["host"]
    # print(host)
    port = opt["port"]
    # print(port)
    bpport = opt["bpport"]
    # print(bpport)
    udid = opt["udid"]

    # system_port = opt["systemPort"]
    driver = None
    if udid in get_devices():
        #放入 端口连接参数
        appium_start(host, port, bpport, udid)
        time.sleep(5)
        if not check_port():
            # print(host)
            # print(port)
            driver = appium_desired_caps(host, port)
    # if not check_port(host, port):
        # driver = appium_desired_caps(host, port, system_port)
    return driver
    # yield driver
    # driver.quit()

