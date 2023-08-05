#local mode
#from pyrda.pyrda.main import DBClient
#package mode
from ..main import DBClient
import pymssql
class MsSqlClient(DBClient):
    def __init__(self,ip, user_name, password, db_name):
        self.ip = ip
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.connect = pymssql.connect(self.ip, self.user_name, self.password, self.db_name)
        self.res = {}
        if self.connect:
            print("连接成功!")
            self.res["status"] = True
            self.res["result"] = self.connect
        else:
            print("连接失败!")
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
    app = MsSqlClient(ip='115.159.201.178',user_name='sa',password='Hoolilay889@',db_name='py_test')
    data = app.select('select * from some_table')
    print(data)
    app.delete('delete from some_table where x = 1')








