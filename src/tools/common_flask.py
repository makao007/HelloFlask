#encoding:utf8
import re 
import math

from flask import request

def pagination_jump(length, index, amount):
    #分页，跳到第n页
    html = """<form action="" method="get">""" 
    for i,j in request.args.iteritems():
        html += """<input type="hidden" name="%s" value="%s" >""" % (i,j)
        
    html += """<input type="hidden" name="length" value="%s" >""" % (length)
    html += "<span>有%s条记录，分%s页</span>" % (amount,  int(math.ceil(float(amount)/length)))
    html += """, 跳到第 <input type="text" name="index" value="" > 页"""
    html += """<input type="submit" value="确定">"""
    return html
    

def pagination_url (length, index):
    #为分页生成url
    path = request.path
    args = request.args
    temp = "?"
    for i,j in args.iteritems():
        temp += "%s=%s&" % (i,j)
    else:
        temp = ""
    if path.endswith('/'):
        path = path[:-1]
    last = path.split('/')[-1]    
    
    tmp = '/%d--%d' % (length, index)
    if re.match('^\d+--\d+$', last):
        path = path[:path.rindex('/')] + tmp
    else:
        path = path + tmp 
    return path + temp
        
         
    
    