#encoding:utf8

def list_to_dict (data, k, v):
    # convert a list to dict
    tmp = {}
    for item in data:
        kk = getattr(item, k)
        vv = getattr(item, v)
        tmp[kk] = vv
    return tmp

def pagination (cur_page, max_page, length, make_url, make_jump):
    # 分页, 前端CSS用Bootstrap
    temp = """<div><ul class="pagination">"""
    
    if cur_page == 1:
        temp += '<li><a href="#" class="disabled">首页</a></li>'
        temp += '<li><a href="#" class="disabled">&laquo;</a></li>'
    else:
        temp += '<li><a href="%s" >首页</a></li>' % (make_url(length,1))
        temp += '<li><a href="%s" >&laquo;</a></li>' % (make_url(length,cur_page-1))
        
    if cur_page == max_page:
        temp += '%s' + '<li><a href="#" class="disabled">&raquo;</a></li>'
        temp += '<li><a href="#" class="disabled">尾页</a></li>'
    else:
        temp += '%s' + '<li><a href="%s">&raquo;</a></li>' % (make_url(length, cur_page+1))
        temp += '<li><a href="%s">尾页</a></li>' % (make_url(length, max_page))
    temp += "</ul>%s</div>" % make_jump(length, cur_page, max_page* length)
    
    if max_page < 10:
        start = 1
        end = max_page + 1
    else:
        start = cur_page - 3
        end = cur_page + 3 + 1
    tmp = ""
    for i in range(start, end):
        active = ''
        if i==cur_page:
            active = " class='active' "
        tmp += "<li %s ><a href='%s'>%s</a></li>" % (active, make_url(length,i),i) 
    return temp % tmp

def pagination_data (length, index, default_amount=None, max_amount=None):
    # 分页，控制取记录的数目，设置默认的数目和最大数目
    if not str(default_amount).isdigit():
        default_amount = 10
    else:
        default_amount = int(default_amount)
        
    if not str(max_amount).isdigit():
        max_amount = 100
    else:
        max_amount = int(max_amount)
        
    if length ==0:
        length = default_amount
    elif length >= max_amount:
        length = max_amount
    offset = (index-1) * length
    
    return length, index, offset