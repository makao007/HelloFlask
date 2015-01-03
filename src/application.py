# encoding:utf8
import math
import hashlib

from flask import Flask
from flask import flash
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import make_response
from flask import render_template
from flask import get_flashed_messages

from werkzeug import secure_filename

from model.model_cms import db, Setting as db_Setting, Category as db_Category, Post as db_Post
import etc as config
import tools.common as common
import tools.common_flask as common_flask

app = Flask(__name__)

def admin_login_required(handler):
    def decorator(*args, **kwargs):
        if not session.get('admin_login', False):
            return redirect(url_for('login'))
        return handler(*args, **kwargs)
    return decorator


def get_site_info ():
    settings  = db_Setting.query.all()
    site_info = {}
    for line in settings:
        site_info[line.field] = line.value
    return site_info

settings = config.st  
site     = get_site_info()

def default_error (msg):
    return render_template ('admin/default_error.html', msg=msg)

@app.route('/')
def index():
    categories = db_Category.query.filter_by(flag=1).order_by('ord')
    return render_template('pc/index.html', site=get_site_info(), categories=categories)

@app.route('/about/')
def about():
    tmp = db_Setting.query.filter_by(field=settings.about).first()
    if tmp:
        text = tmp.value
    else:
        text = 'About This Site'
    return render_template('pc/about.html', content=text, site=get_site_info() )


@app.route('/c/<category>')
def category(category):
    tmp  = db_Category.query.filter_by(slot=category).first()
    tmp2 = []
    if tmp:
        tmp2 = db_Post.query.filter_by(category_id=tmp.id).limit(site.get(settings.page_records) or 10)
    return render_template('pc/category.html', category=tmp, posts=tmp2, site=site)


@app.route('/d/<post>')
def article(post):
    tmp  = db_Post.query.filter_by(id=post).first()
    if tmp:
        tmp2 = db_Category.query.filter_by(id=tmp.category_id).first()
    return render_template('pc/article.html', post=tmp, category=tmp2, site=site)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name='Unknown User'):
    if request.method == "GET":
        print "this is a GET method"
    elif request.method == "POST":
        print "this is a POST method" 
    return render_template('hello.html', name=name)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        f = request.files['upload_file']
        f.save('upload/' + secure_filename(f.filename))
        return "upload file successful"
    return render_template('upload_file.html') 

@app.route('/admin/login', methods=['POST', 'GET'])
def admin_login():
    if 'admin_login' in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','').strip()
        password = hashlib.md5(password).hexdigest()
        
        if db_Setting.query.filter_by(field=settings.site_username, value=username).first() and \
           db_Setting.query.filter_by(field=settings.site_password, value=password).first():
            app.logger.debug("User %s login successful" % request.form.get('username',''))
            session['admin_login'] = True
            session['username']    = username
            return redirect(url_for('admin'))
        else:
            app.logger.debug("User %s login fail " % request.form.get('username',''))
            flash(u"用户名或密码不正确")
    return render_template('admin/login.html', admin_name = site.get(settings.site_username))

@app.route('/admin/logout')
def admin_logout ():
    session.clear()
    return redirect(url_for ('admin_login'))

#-------------------------------admin------------------------
@app.route('/admin/')
def admin():
    if not 'admin_login' in session:
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin_category'))
    #return render_template('admin/dashboard.html')

@app.route('/admin/category')
def admin_category():
    categories = db_Category.query.order_by('ord').all()
    return render_template('admin/category.html', records = categories)


@app.route('/admin/category/edit/<int:xid>', methods=['POST', 'GET'])
def admin_category_edit(xid):
    if request.method == "GET":
        if xid >0:
            category = db_Category.query.filter_by(id=int(xid)).first()
        else:
            category = {}
        return render_template('admin/category_edit.html', record = category)
    elif request.method == "POST":
        name = request.form.get('cname','').strip()
        slot = request.form.get('cslot','').strip()
        cord = request.form.get('cord','').strip()
        flag = request.form.get('flag','1').strip()
        remark = request.form.get('cremark','').strip()
        
        if not name or not slot or not cord.isdigit() or not flag in '01':
            return default_error (u"参数出错")
        xid  = int(xid)
        flag = int(flag)
        if xid == 0:
            cate = db_Category(name, remark, slot, cord, int(flag))
            db.session.add (cate)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash (u"添加分类失败，由于链接%s已存在" % slot)
                return redirect(url_for ('admin_category_edit', xid=xid))
        else:
            category = db_Category.query.filter_by(id=int(xid)).first()
            if not category:
                return default_error (u"记录不存在")
            category.name = name
            category.slot = slot
            category.desc = remark
            category.ord  = cord
            category.flag = flag
            db.session.add(category)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash (u"添加分类失败，由于链接%s已存在" % slot)
                return redirect(url_for ('admin_category_edit', xid=xid))
        return redirect(url_for('admin_category'))

@app.route('/admin/article')
@app.route('/admin/article/<int:length>--<int:index>')
def admin_article(length=0, index=1):
    length, index, offset = common.pagination_data (length, index, int(site.get(settings.page_records)), int(site.get(settings.page_records_max)))
    posts = db.session.query(db_Post.id, db_Post.title,db_Post.category_id, 'pub_date').order_by('-pub_date').limit(length).offset(offset)
    amount= db_Post.query.count()
    categories = db_Category.query.filter_by(flag=1).order_by('ord')
    categories_dict = common.list_to_dict (categories, 'id', 'name')
    pagination = common.pagination(index, int(math.ceil(float(amount)/length)), length, common_flask.pagination_url, common_flask.pagination_jump)
    return render_template('admin/article.html', records = posts, categories=categories, categories_dict=categories_dict, pagination=pagination)

@app.route('/admin/article/edit/<int:xid>', methods=['POST', 'GET'])
def admin_article_edit(xid):
    if request.method == "GET":
        categories = db_Category.query.filter_by(flag=1).order_by('ord')
        if xid >0:
            post = db_Post.query.filter_by(id=int(xid)).first()
        else:
            post = {}
        return render_template('admin/article_edit.html', record = post, categories = categories)
    elif request.method == "POST":
        title = request.form.get('title','').strip()
        body  = request.form.get('content','').strip()
        cate  = request.form.get('category','').strip()
        
        if not title or not cate.isdigit():
            return default_error (u"参数出错")
        xid  = int(xid)
        cate = int(cate)
        if xid == 0:
            record = db_Post(title, body, cate)
            db.session.add (record)
            db.session.commit()
        else:
            record = db_Post.query.filter_by(id=int(xid)).first()
            if not record:
                return default_error (u"记录不存在")
            record.title = title
            record.body  = body
            record.category_id = cate
            db.session.add(record)
            db.session.commit()
        return redirect(url_for('admin_article'))

@app.route('/admin/article/delete/<int:xid>')
def admin_article_delete(xid):
    tmp = db_Post.query.filter_by(id=int(xid)).first()
    db.session.delete (tmp)
    db.session.commit()
    return redirect(url_for('admin_article'))

@app.route('/admin/setting', methods=['POST', 'GET'])
def admin_setting():
    if request.method == "GET":
        records = db_Setting.query.order_by('id')
        records = filter(lambda x:x.field not in [settings.site_username, settings.site_password], records)
        return render_template('admin/setting.html', records = records)
    elif request.method == "POST":
        for i in config.settings:
            tmp = db_Setting.query.filter_by(field=i['field']).first()
            if tmp:
                if tmp.field in [settings.site_username, settings.site_password]:
                    continue
                tmp.value = request.form.get(i['field'],'').strip()
                db.session.add (tmp)
        db.session.commit()
        return redirect(url_for('admin_setting'))

@app.route('/admin/adminpw', methods=['POST', 'GET'])
def admin_adminpw():
    #修改后台的登录密码
    if request.method == "GET":
        return render_template('admin/adminpw.html')

    elif request.method == "POST":
        old_password = request.form.get('old_password','').strip()
        new_password = request.form.get('new_password1','').strip()
        if not old_password or not new_password:
            return default_error (u"旧密码和新密码都不能为空")
        old_password = hashlib.md5(old_password).hexdigest()
        password = db_Setting.query.filter_by(field=settings.site_password, value=old_password).first()
        if not password:
            return default_error (u"旧密码不正确")
        password.value = hashlib.md5(new_password).hexdigest()
        db.session.add(password)
        db.session.commit()
        return redirect(url_for ("admin_adminpw"))
       
@app.route('/forgot_password')
def forgot_password ():
    #忘记后台的登录密码，发送EMail到管理员的邮箱    
    email = site.get(settings.site_author)
    if '@' not in email:
        return default_error (u"发送邮件失败，无效的管理员邮件地址:%s" % email)
    flag,msg = send_email ("reset amdin login password", "noreply@xx.yy.com", \
                [email,], \
                "reset admin login password, new password is xxy","" )
    if not flag:
        return default_error (msg)
    email_a, email_b = email.split('@',1)
    return u"已发送邮件到%s, 请注意查收!" % (email_a[:4] + '***@' + email_b)

def send_email(subject, sender, recipients, text_body, html_body):
    try:
        from flask.ext.mail import Message
        from flask.ext.mail import Mail
    except ImportError,e:
        return False, u"发送邮件失败，由于服务器没有安装相关邮件模块"
    
    print 'send mail to %s' % recipients
    mail = Mail()
    mail.init_app(app)
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    try:
        mail.send(msg) 
    except Exception,e:
        return False, u'发送邮件失败，网络错误, %s' % (e)
    return True, ''

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return render_template('hello.html', name=username)

@app.route('/staff/<username>')
def show_staff_profile(username):
    # show the user profile for that user
    return 'staff %s' % username

@app.route('/post/<int:post_id>')        #int, float, path (path include "/")
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about2')
def about2():
    return 'The about page'
    resp = make_response(render_template('about.html'))
    resp.set_cookie('username', 'michael')
    return resp

@app.route('/session')
def session_page ():
    session['username'] = "michael"
    session.pop ('username')
    return "session testing"

@app.route('/mylog')
def mylog ():
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    return "this  is a log file"

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.debug = config.debug_mode    
    app.secret_key = config.session_key       
    app.run()             #app.run(debug=True)