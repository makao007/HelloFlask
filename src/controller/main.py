# encoding:utf8

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World2!"

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello2():
    return 'Hello World'

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

@app.route('/about')
def about():
    return 'The about page'

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.debug = True            
    app.run()             #app.run(debug=True)