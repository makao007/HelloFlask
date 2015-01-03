#encoding:utf8

settings = [
    {'id':  1,  'field':'          site_title',  'value':u'IT资讯站',  'remark':u'网页标题'},
    {'id':  2,  'field':'           site_name',  'value':u'IT资讯站',  'remark':u'导航栏'},
    {'id':  3,  'field':'           sub_title',  'value':u'全部最新资讯加油站',  'remark':u'主页标题'},
    {'id':  4,  'field':'         description',  'value':u'这里网罗全球新最新潮的IT资讯，为你的决策提供更有力的支持',  'remark':u'主页副标题'},
    {'id':  5,  'field':'               about',  'value':u'关于',  'remark':u'关于本站点'},
    {'id':  6,  'field':'          copy_right',  'value':u'Copyright 2015',  'remark':u'版权信息'},
    {'id':  7,  'field':'       site_keywords',  'value':u'IT,信息技术，百度，科技，Google,腾迅',  'remark':u'网站关键词'},
    {'id':  8,  'field':'    site_description',  'value':u'开发者头条,码农周刊,码农,码农IO,程序员,编程,程序设计,编程语言,程序员招聘,招聘,FIR.im,Coding',  'remark':u'网站介绍'},
    {'id':  9,  'field':'         site_author',  'value':u'test@126.com',  'remark':u'站长EMail'},
    {'id': 10,  'field':'        page_records',  'value':u'10',  'remark':u'每页显示记录'},
    {'id': 11,  'field':'  page_records_flash',  'value':u'10',  'remark':u'最多显示记录'},
    {'id': 12,  'field':'    page_records_max',  'value':u'5',   'remark':u'最多加载次数'},
    {'id': 13,  'field':'       site_username',  'value':u'admin',  'remark':u'管理员用户员'},
    {'id': 14,  'field':'       site_password',  'value':u'81dc9bdb52d04dc20036dbd8313ed055',  'remark':u'管理员密码(初始为1234)'},
]
for i in settings:
    i['field'] = i.get('field').strip()

class Settings :
    # 相当于枚举类型，防止用到没有定义的config field
    def __init__ (self, data):
        for i in data:
            tmp = i.get('field').strip()
            setattr(self, tmp, tmp)

st = Settings (settings)         

if __name__ == "__main__":
    st = Settings (settings)
    print dir(st)
    