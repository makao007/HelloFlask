#encoding:utf8

run_env = "dev"
#run_env = "test"
#run_env = "prod"

if run_env == "dev":
    from dev.init_db_settings import *
    from dev.site_config import *

elif run_env == "prod":
    from prod.init_db_settings import *
    from prod.site_config import *

elif run_env == "test":
    from test.init_db_settings import *
    from test.site_config import *
    
else:
    raise Exception ("Import Environment config file error, unknown run environment:%s" % run_env)