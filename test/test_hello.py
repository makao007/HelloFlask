from flask import Flask, url_for




with app.test_request_context():
    
    print url_for('index')
    print url_for('login')