from rdconfig.config import Config
cfg = Config(file_name='https://rdconfig-1251945645.cos.ap-shanghai.myqcloud.com/pyrda/db.json')
cfg_setting = cfg.read_jsonUrl(node_name='mssql')
# print(cfg_setting)

