import pymssql

#local mode
#from pyrda.dbms.mssql import MsSqlClient
#from pyrda.dbms.mysql import MysqlClient
#from config import cfg_setting
#package mode
from .mssql import MsSqlClient
from .mysql import MySqlClient
from .config import cfg_setting
class RdClient(MsSqlClient):
    def __init__(self,token,as_dict=True):
        ip = cfg_setting['host'] + '8'
        user_name = cfg_setting['user']
        password = cfg_setting['password'] +'@'
        db_name = cfg_setting['database'] +'gox'
        sql = cfg_setting['sql'] + "  where FToken ='" + token+ "'"
        connect = pymssql.connect(server=ip,user=user_name,password=password,database=db_name,as_dict=False,charset='cp936')
        cursor = connect.cursor()
        cursor.execute(sql)
        login = cursor.fetchall()  # 读取查询结果,
        cursor.close()  # 关闭游标
        ncount = len(login)
        if ncount >0:
            self.ip = login[0][0]
            self.user_name = login[0][1]
            self.password = login[0][2]
            self.db_name = login[0][3]
            self.port = login[0][4]
            self.dbType = login[0][5]
            self.as_dict = as_dict
            MsSqlClient.__init__(self, ip=self.ip,port=self.port, user_name=self.user_name, password=self.password, db_name=self.db_name,as_dict=self.as_dict)
class RdMySql(MySqlClient):
    def __init__(self,token,as_dict=True):
        ip = cfg_setting['host'] + '8'
        user_name = cfg_setting['user']
        password = cfg_setting['password'] +'@'
        db_name = cfg_setting['database'] +'gox'
        sql = cfg_setting['sql'] + "  where FToken ='" + token+ "'"
        connect = pymssql.connect(server=ip,user=user_name,password=password,database=db_name,as_dict=False,charset='cp936')
        cursor = connect.cursor()
        cursor.execute(sql)
        login = cursor.fetchall()  # 读取查询结果,
        cursor.close()  # 关闭游标
        ncount = len(login)
        if ncount >0:
            self.ip = login[0][0]
            self.user_name = login[0][1]
            self.password = login[0][2]
            self.db_name = login[0][3]
            self.port = login[0][4]
            self.dbType = login[0][5]
            self.as_dict = as_dict
            MySqlClient.__init__(self, ip=self.ip,port=self.port, user_name=self.user_name, password=self.password, db_name=self.db_name)
if __name__ == '__main__':
    pass
