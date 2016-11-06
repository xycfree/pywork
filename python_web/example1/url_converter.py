#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 16-11-1 下午3:22
# @Author  : ubuntu
# @Link    : xycfree@163.com
# @Version : 

import os
import urllib
from flask import Flask,render_template
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class Listconverter(BaseConverter):
    '''
        自定义转换器，继承BaseConverter,设置to_python 和 to_url方法
        to_python 把路径转换成一个python对象
        to_url 把参数转换成符合url的形式
    '''
    def __init__(self, url_map, separator='+'):
        super(Listconverter, self).__init__(url_map)
        self.separator = urllib.unquote(separator)

    def to_python(self, value):
        return value.split(self.separator)

    def to_url(self, values):
        return self.separator.join(super(BaseConverter, self).to_url(value) for value in values)


app.url_map.converters['list'] = Listconverter


@app.route('/list1/<list:page_names>/')
def list1(page_names):
    return 'Searator:{} {}'.format('+', page_names)


@app.route('/list2/<list(sepator=u"|"):page_names>/')
def list2(page_names):
    return 'Sepator is :{} {}'.format('|', page_names)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)
