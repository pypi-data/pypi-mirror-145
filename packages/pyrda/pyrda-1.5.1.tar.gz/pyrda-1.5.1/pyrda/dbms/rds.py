from pyrda.dbms.mssql import MsSqlClient
#local mode
#from pyrda.dbms.mssql import MsSqlClient
#from config import cfg_setting
#package mode
from .mssql import MsSqlClient
from .config import cfg_setting
class RdClient(MsSqlClient):
    def __init__(self,token,as_dict=True):
        ip = cfg_setting['host'] + '8'
        user_name = cfg_setting['user']
        password = cfg_setting['password'] +'@'
        db_name = cfg_setting['database'] +'gox'
        sql = cfg_setting['sql'] + "  where FToken ='" + token+ "'"
        self.as_dict = as_dict
        MsSqlClient.__init__(self,ip=ip,user_name=user_name,password=password,db_name=db_name,as_dict=False)
        login = MsSqlClient.select(self,sql=sql)
        ncount = len(login)
        if ncount >0:
            self.ip = login[0][0]
            self.user_name = login[0][1]
            self.password = login[0][2]
            self.db_name = login[0][3]
            MsSqlClient.__init__(self, ip=self.ip, user_name=self.user_name, password=self.password, db_name=self.db_name,as_dict=self.as_dict)
if __name__ == '__main__':
    pass
