#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 16-11-5 下午11:20
# @Author  : ubuntu
# @Link    : xycfree@163.com
# @Version : 

import os

from flask_mako import MakoTemplates,render_template
from flask_sqlalchemy import SQLAlchemy

mako = MakoTemplates()
db = SQLAlchemy()