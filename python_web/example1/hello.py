#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 16-11-1 下午2:16
# @Author  : ubuntu
# @Link    : xycfree@163.com
# @Version : 

import os
from flask import Flask,render_template
from local_settings import *

app = Flask(__name__, template_folder='../templates',
            static_folder='../static') #定义模板文件目录和静态文件目录

app.secret_key = 'secret key'
# app.config['DEBUG'] = True
# app.config.update(
#     DEBUG=True,
#     SECRET_KEY='secret key'
# )


@app.route('/')
def hello():
    return 'hello world wang 111'

@app.route('/about/<name>/')
def about(name):
    #return 'this is about page'
    return render_template('about.html',name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
