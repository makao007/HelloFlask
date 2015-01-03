from flask import Flask, url_for


import main

app = main.app

with app.test_request_context():   
    print url_for('hello')