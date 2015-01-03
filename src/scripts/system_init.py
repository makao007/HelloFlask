#encoding:utf8

#这个是系统初始化时（第一次安装）执行的脚本,
#用于创建系统所需要的数据库的表


import os
import sys
sys.path.append (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import etc as config

from model.model_cms import *
db.create_all()   #create the tables in the database


for i in config.settings:
    record = Setting (i.get('field'), i.get('value'), i.get('remark'))
    db.session.add (record)

db.session.commit()

print 'init db done'

