import time

from selenium.webdriver.common.by import By

from data.ExcelConfig import TestSteps
from utils.LogUtil import my_log
from selenium.webdriver.support.wait import WebDriverWait
import allure
import datetime

# 1定义类
from utils.dbUtil import MysqlConnect


class Action:
    def __init__(self, driver):
        self.driver = driver
        self.log = my_log("Base_Page")


    def splitNum(self, n):
        #切割数字变成单个输出
        print(n)
        x = int(n)
        for a in n:
            a = int(a)
            print(a)

    # 2定义方法
    # 元素定位
    # byid,byxpath
    # 元素等待方法
    # 1、click
    # 2、send_keys
    # 3、toast
    # 4、坐标定位
    # click、 id 、 xpath
    def by_xpath(self, value):
        """
        xpath 元素定位
        :param value:
        :return:
        """
        return self.by_find_element(By.XPATH, value)

    def by_id(self, value):
        """
        id的元素定位
        :param value:
        :return:
        """
        return self.by_find_element(By.ID, value)

    # def by_xapth_class(self, value):
        # """
        # #
        # # :param value:
        # # :return:
        # # """
        # # if value:
        # #     y=0
        # #     for i in value:
        # #         print(i)
        # #         s = int(i)
        # #         if s == "0":
        # #             y = 7
        # #         elif s == "1":
        # #             y = 8
        # #         elif s == "2":
        # #             y = 9
        # #         elif s == "3":
        # #             y = 10
        # #         elif s == "4":
        # #             y = 11
        # #         elif s == "5":
        # #             y = 12
        # #         elif s == "6":
        # #             y = 13
        # #         elif s == "7":
        # #             y = 14
        # #         elif s == "8":
        # #             y = 15
        # #         elif s == "9":
        # #             y = 16
        # #         self.driver.keycode(y)
        # #         time.sleep(0.5)

    # send_keys
    def by_id_send_keys(self, **kwargs):
        """
        通过id定位元素发送内容
        :param by:
        :param value:
        :param send_value:
        :return:
        """
        # self.by_find_element(By.ID, value).send_keys(send_value)
        global loc
        by, value = kwargs["by"], kwargs["value"]
        if by == "id":
            loc = self.by_id(value)
        elif by == "xpath":
            loc = self.by_xpath(value)
        elif by == "xpath_dw":
            loc = self.by_xpath(value)
        elif by == "id_dw":
            loc = self.by_id(value)
        elif by == "class":
            time.sleep(2)
        if by != "class" and by != "id_dw" and by != "xpath_dw":
            loc.click()
            loc.send_keys(kwargs["send"])

    # WebDriverWait
    def by_find_element(self, by, value, timeout=30, poll=3, ):
        """
        隐式等待， 寻找元素
        :param by:
        :param value:
        :param timeout:
        :param poll:
        :return:
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until(lambda x: x.find_element(by, value))
            return self.driver.find_element(by, value)
        except Exception as e:
            self.log.error("没有找到该元素{}".format(e))

    # toast
    def is_toast_get_toast(self, **kwargs):
        # 1使用by_find_element寻找元素，类型xpath,value自定义
        # 2webdriverwait获取信息，text
        # toast_loc = "//*[contains(@text, '输入错误')]

        try:
            text = kwargs["expect"]
            toast_loc = "//*[contains(@text,'" + text + "')]"
            ele = WebDriverWait(self.driver, timeout=3, poll_frequency=1).until(
                lambda x: x.find_element(By.XPATH, toast_loc))
            self.log.info("获取toast内容为：{}".format(ele.text))
            return True
        except Exception as e:

            self.log.error("toast获取信息失败， 错误信息{}".format(e))

            return False


    def click_btn(self, **kwargs):
        global loc
        by, value = kwargs["by"], kwargs["value"]
        # 根据by类型，进行by_id, by_xpath方法调用
        if by == "id":
            loc = self.by_id(value)
        elif by == "xpath":
            loc = self.by_xpath(value)
            time.sleep(1)
        loc.click()

    # 1.定义一个swipeUp函数，n代表滑动的次数，t代表触摸时间，t可以填写，也可以不填写. dr代表driver
    # 2.get_window_size()是获取屏幕的尺寸大小，它返回的是一个字典例如{‘width’：720，’height’：1280}
    #
    # 3.将x1，y1，x2, y2的变量赋值，例如x1 = L[‘width’] *0.75 ，因为向上滑动，x轴无需变动，所以x1 = x2
    #
    # 4.这里使用一个for循环，目的是可以实现多次滑动，这样方便操作使用。n代表你要滑动的次数。

    # 屏幕向上滑动, x轴不变，y轴向上移动
    def swipeUp(self, n=1, t=500):
        L = self.driver.get_window_size()
        x1 = L['width'] * 0.5
        y1 = L['height'] * 0.75
        y2 = L['height'] * 0.25
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)

    # 屏幕向下滑动，x轴不变，y轴向下移动
    def swipeDown(self, n=1, t=500):
        L = self.driver.get_window_size()
        x1 = L['width'] * 0.5
        y1 = L['height'] * 0.25
        y2 = L['height'] * 0.75
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)

    # 屏幕向左滑动，y轴不变，x轴向左移动
    def swipeLeft(self, n=1, t=500):
        L = self.driver.get_window_size()
        x1 = L['width'] * 0.75
        x2 = L['width'] * 0.25
        y1 = L['height'] * 0.5
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)

    # 屏幕向右滑动，y轴不变，x轴向右移动
    def swipeRight(self, n=1, t=500):
        L = self.driver.get_window_size()
        x1 = L['width'] * 0.25
        x2 = L['width'] * 0.75
        y1 = L['height'] * 0.5
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)

    def taptest(self, **kwargs):
        # 设定系数,控件在当前手机的坐标位置除以当前手机的最大坐标就是相对的系数了
        by = kwargs["tap"]
        width = by.get('width')
        height = by.get('height')
        # 获取当前手机屏幕大小X,Y
        X = self.driver.get_window_size()['width']
        Y = self.driver.get_window_size()['height']
        a1 = int(width) / 720
        b1 = int(height) / 1280
        # 屏幕坐标乘以系数即为用户要点击位置的具体坐标
        time.sleep(1)
        self.driver.tap([(a1 * X, b1 * Y)], 500)

    # 自适应匹配方法、根据输入值选择上下左右滑动
    def by_slide(self, **kwargs):
        time.sleep(2)
        by = kwargs["slid"]
        # 根据by类型，进行by_id, by_xpath方法调用
        L = self.driver.get_window_size()
        if by == "swipeUp":
            loc = self.swipeUp()
        elif by == "swipeDown":
            loc = self.swipeDown()
        elif by == "swipeLeft":
            loc = self.swipeLeft()
        elif by == "swipeRight":
            loc = self.swipeRight()

    # 放入config配置文件中
    def assert_toast_result(self, **kwargs):
        toast_result = self.is_toast_get_toast(**kwargs)
        assert toast_result == False
        # try:
        #     # assert toast_result == False (测试截图能否正常使用）
        #     assert toast_result
        # except Exception as e:
        #     png = self.driver.get_screenshot_as_png()
        #     allure.attach(png, "toast错误", allure.attachment_type.PNG)
        #     raise e


# 定义装饰器
# 1 定义装饰2层函数
def screenshot_allure(func):
    def get_err_screenshot(self, *args, **kwargs):
        # 2 定义内部函数、拍图操作
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            png = self.driver.get_screenshot_as_png()
            # 当前时间
            name = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            allure.attach(png, name, allure.attachment_type.PNG)
            raise e

    # 3 返回内部函数名称
    return get_err_screenshot
# 4 重构toast断言
# 5 调用装饰器
