from config import Conf
from utils.YamlUtil import YamlReader


def get_keyword(name):
    # 1读取配置文件， 文件路径：绝对路径
    keyword_file = Conf.keywords_path
    # 2 YamlReader, data()
    reader = YamlReader(keyword_file).data()
    # 3 key获取值 name
    value = reader[name]
    return value


class A:
    name = "test"

    def get_name(self):
        print(self.name)


if __name__ == '__main__':
    a = A()
    print(getattr(a, "name"))  # 输出name属性的值
    # print(getattr(a, "test"))
    fun = getattr(a, "get_name")
    print(fun)
    fun()
    # print(get_keyword("click"))
