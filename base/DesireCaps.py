# encoding:utf8
import time
from config import Conf
from appium import webdriver
from utils.YamlUtil import YamlReader

# 1.通过yaml来读取 caps.yml
reader = YamlReader(Conf.conf_caps)
data = reader.data()


# 结果字典转换
# 2.desired创建字典

def appium_desired_caps(host, port):
    desired_caps = dict()
    # 3.platformName
    desired_caps['platformName'] = data['platformName']

    # 4.platformVesion
    desired_caps['platfromVersion'] = data['platfromVersion']


    # 5.deviceName
    desired_caps['deviceName'] = data['deviceName']

    # 6.启动程序的报名 appPackage    # 通过 adb shell dumpsys window|grep mCurrentFocus 获取
    desired_caps['appPackage'] = data['appPackage']

    # 7.启动界面名appActivity
    desired_caps['appActivity'] = data['appActivity']

    # 获取toast automationName = uiautomator2
    desired_caps["automationName"] = data['automationName']


    # 不清除app里的原有数据
    desired_caps["noReset"] = True


    # 8.使用http，链接appium服务器
    driver = webdriver.Remote('http://%s:%s/wd/hub' % (host, port), desired_caps)  # IP地址是Appium中的监听地址

    # WebDriverWait(driver, 5, 0.5).until(lambda x:x.find_element_by_id())
    driver.implicitly_wait(20)
    return driver
