import unittest

from utils.dbUtil import MysqlConnect

#连接数据库获取数据
class testdb(unittest.TestCase):
    def test_query(self):
       tunnelDB=MysqlConnect('192.168.199.243',3306,'cloud','Cloud.123456','cloud')
       sql="SELECT regist FROM t_user_phonecode WHERE phone ='19900000009'"
       results=tunnelDB.select(sql)
       for result in results:
           print(result)

    def test_get_cursor(self):
       tunnelDB=MysqlConnect('192.168.199.243',3306,'cloud','Cloud.123456','cloud')
       sql="SELECT * FROM t_user_phonecode WHERE phone ='19900000009'"
       cursor=tunnelDB.get_cursor()
       cursor.execute(sql)
       results=cursor.fetchall()
       for result in results:
           print(result)
