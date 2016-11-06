#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 16-11-6 下午9:22
# @Author  : ubuntu
# @Link    : xycfree@163.com
# @Version : 

import os
import hashlib
from functools import partial
from config import UPLOAD_FOLDER

HERE = os.path.abspath(os.path.dirname(__file__))

def get_file_md5(f, chunk_size=8192):
    h = hashlib.md5()
    print 'h: ', h
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdigest()

def humanize_bytes(bytesize,precision=2):
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )

    if bytesize == 1:
        return '1 byte'
    for factor,suffix in abbrevs:
        if bytesize >= factor:
            break
    return '%.*f %s' % (precision, bytesize / factor, suffix)

get_file_path = partial(os.path.join,HERE,UPLOAD_FOLDER)
print 'get_file_path: ', get_file_path
'''
    函数的partial应用
    典型的，函数在执行时，要带上所有必要的参数进行调用。然后，有时参数可以在函数被调用之前提前获知。这种情况下，
    一个函数有一个或多个参数预先就能用上，以便函数能用更少的参数进行调用。
    def add(a,b):
        return a+b
    plus = partial(add,100)
    plus(9) #output 109
'''









