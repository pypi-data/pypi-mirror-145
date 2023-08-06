#local mode
#from pyrda.main import DBClient
#package mode
from ..main import DBClient
import pymysql
class MySqlClient(DBClient):
    def __init__(self,ip, user_name, password, db_name,charset='utf8',port=3306,as_dict = True):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.charset = charset
        self.as_dict = as_dict
        self.connect = pymysql.connect(host=self.ip,port=self.port, user=self.user_name, password=self.password, database=self.db_name,charset= self.charset,cursorclass = pymysql.cursors.DictCursor)
        self.res = {}
        if self.connect:
            #print("连接成功!")
            self.res["status"] = True
            self.res["result"] = self.connect
        else:
            #print("连接失败!")
            self.res["status"] = False
            self.res["result"] = "error"
    def close(self):
        if self.res["status"]:
            self.connect.close()
            res = True
        else:
            res = False
        return(res)

    def exec(self, sql):
        if self.res["status"]:
            self.cursor = self.connect.cursor()
            self.cursor.execute(sql)  # 执行sql语句
            self.connect.commit()  # 提交
            res = True
        else:
            res = False
    def insert(self,sql):
        res = self.exec(sql)
        return(res)

    def update(self, sql):
        res = self.exec(sql)
        return (res)

    def delete(self, sql):
        res = self.exec(sql)
        return (res)

    def select(self, sql):
        if self.res["status"]:
            self.cursor = self.connect.cursor()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()  # 读取查询结果,
            self.cursor.close()  # 关闭游标
            return res


if __name__ == '__main__':
    pass


