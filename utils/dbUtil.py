import pymysql as pymysql

class MysqlConnect:
    def __init__(self,host,port, user, password, database):

        self.db=pymysql.connect(host=host,port=port, user=user, password=password, database=database, charset='utf8')
        self.cursor = self.db.cursor()

    def select (self,sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results
    def get_cursor(self):
        return self.cursor