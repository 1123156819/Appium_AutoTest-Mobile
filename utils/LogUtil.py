import logging
import os
from config import Conf
import datetime

# 定义日志级别的映射
log_l = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR
}


# 1创建类
class Logger:
    # 2定义参数：写入日志文件的名称 test.lo个，logger名称、日志级别总开关
    def __init__(self, log_file, log_name, log_level):
        # 设置logger名称
        self.logger = logging.getLogger(log_name)
        # 设置日志级别
        self.logger.setLevel(log_l[log_level])
        # 3编写输出控制台handler
        # 判断handlers是否存在
        if not self.logger.handlers:
            fh_stream = logging.StreamHandler()
            fh_stream.setLevel(log_l[log_level])
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh_stream.setFormatter(formatter)
            self.logger.addHandler(fh_stream)
            # 4编写输出日志文件handler
            fh_file = logging.FileHandler(log_file)
            fh_file.setLevel(log_l[log_level])
            fh_file.setFormatter(formatter)
            self.logger.addHandler(fh_file)


# 外部调用方法
# log_file, log_name, log_level
# 1初始化参数数据
# 日志文件的名称 = logs目录 +文件名 当前时间+扩展名
log_path = Conf.log_path
# 当前时间
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# 扩展名
log_extension = ".log"
logfile = os.path.join(log_path, current_date + log_extension)
print(logfile)
# log_level
loglevel = "debug"


# 2对外方法、出事log工具类、提供其他类使用
def my_log(log_name=__file__):
    return Logger(logfile, log_name, loglevel).logger


if __name__ == "__main__":
    log = my_log("测试一下")
    log.info("info信息")
    log.debug("来个信息debug")
    log.error("来个信息err")
