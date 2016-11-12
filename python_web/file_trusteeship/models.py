#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 16-11-6 下午4:33
# @Author  : ubuntu
# @Link    : xycfree@163.com
# @Version : 

import os
from datetime import datetime
import uuid
import cropresize2
import magic
import short_url
from PIL import Image
from flask import abort, request
from werkzeug.utils import cached_property

try:
    from urllib import quote
    # 将url数据获取之后，并将其编码，从而适用与URL字符串中，使其能被打印和被web服务器接受
    # urllib.quote('http://www.baidu.com') 'http%3A//www.baidu.com'
except ImportError:
    from urllib.parse import quote

from mimes import IMAGE_MIMES, AUDIO_MIMES, VIDEO_MIMES
from utils import get_file_path, get_file_md5
from ext import db


class PasteFile(db.Model):
    __tablename__ = 'PasteFile'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(5000), nullable=False)
    filehash = db.Column(db.String(128), nullable=False, unique=True)
    filemd5 = db.Column(db.String(128), nullable=False, unique=True)
    uploadtime = db.Column(db.DateTime, nullable=False)
    mimetype = db.Column(db.String(256), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __init__(self, filename='', mimetype='application/octet-stream', size=0,
                 filehash=None, filemd5=None):
        self.uploadtime = datetime.now()
        self.mimetype = mimetype
        self.size = int(size)
        self.filehash = filehash if filehash else self._hash_filename(filename)
        self.filename = filename if filename else self.filehash
        self.filemd5 = filemd5

    @staticmethod
    def _hash_filename(filename):
        '''
        :param filename: 获取文件名称，str.rpartition('.')获取扩展名，通过uuid生成随机名
        :return:
        '''
        _, _, suffix = filename.rpartition('.')  # partition() 方法用来根据指定的分隔符将字符串进行分割。rpartition从右向左匹配

        # 如果字符串包含指定的分隔符，则返回一个3元的元组，第一个为分隔符左边的子串，第二个为分隔符本身，第三个为分隔符右边的子串。
        return '%s.%s' % (uuid.uuid4().hex, suffix)

    @cached_property  # property将类方法转换为只读属性  重新实现一个属性的setter和getter方法
    def symlink(self):
        return short_url.encode_url(self.id)

    @classmethod  # 类方法
    def get_by_symlink(cls, symlink, code=404):
        id = short_url.decode_url(symlink)
        return cls.query.filter_by(id=id).first() or abort(code)

    '''
        在Python中，静态方法和类方法都是可以通过类对象和类对象实例访问。但是区别是：
        @classmethod 是一个函数修饰符，它表示接下来的是一个类方法，而对于平常我们见到的则叫做实例方法。
        类方法的第一个参数cls，而实例方法的第一个参数是self，表示该类的一个实例。
        普通对象方法至少需要一个self参数，代表类对象实例
        类方法有类变量cls传入，从而可以用cls做一些相关的处理。并且有子类继承时，调用该类方法时，传入的类变量cls是子类，
        而非父类。 对于类方法，可以通过类来调用，就像C.f()，有点类似C＋＋中的静态方法, 也可以通过类的一个实例来调用，
        就像C().f()，这里C()，写成这样之后它就是类的一个实例了。
        静态方法则没有，它基本上跟一个全局函数相同，一般来说用的很少
    '''

    @classmethod
    def get_by_filehash(cls, filehash, code=404):
        return cls.query.filter_by(filehash=filehash) or abort(code)

    @classmethod
    def get_my_md5(cls, filemd5):
        return cls.query.filter_by(filemd5=filemd5).first()

    @classmethod
    def create_by_upload_file(cls, uploaded_file):
        rst = cls(uploaded_file.filename, uploaded_file.mimetype, 0)
        uploaded_file.save(rst.path)
        with open(rst.path, 'rb') as f:
            filemd5 = get_file_md5(f)
            uploaded_file = cls.get_my_md5(filemd5)
            if uploaded_file:
                os.remove(rst.path)
                return uploaded_file
        filestat = os.stat(rst.path) #文件目录状态
        rst.size = filestat.st_size #文件大小
        rst.filemd5 = filemd5
        return rst

    @classmethod
    def create_by_old_paste(cls,filehash):
        filepath = get_file_path(filehash)
        mimetype = magic.from_file(filepath, mime=True) #返回文件类型
        #python-magic是libmagic文件类型识别库的一个python接口。libmagic通过根据文件类型的预定义列表检查其标头识别文件类型。
        filestat = os.stat(filepath)
        size = filestat.st_size
        rst = cls(filehash, mimetype, size, filehash=filehash)
        return rst

    @property
    def path(self):
        return get_file_path(self.filehash)

    def get_url(self, subtype, is_symlink=False):
        hash_or_link = self.symlink if is_symlink else self.filehash
        return 'http://{host}/{subtype}/{hash_or_link}'.format(
            subtype = subtype, host=request.host, hash_or_link=hash_or_link )

    @property
    def url_i(self):
        return self.get_url('i')

    @property
    def url_p(self):
        return self.get_url('p') #文件预览地址

    @property
    def url_s(self):
        return self.get_url('s', is_symlink=True) #文件短链接地址

    def url_d(self):
        return self.get_url('d') #文件下载地址

    @property
    def image_size(self):
        if self.is_image:
            im = Image.open(self.path)
            return im.size
        return (0, 0)

    @property
    def quoteurl(self):
        return quote(self.url_i)

    @classmethod
    def rsize(cls,old_paste,weight,height):
        assert old_paste.is_image, TypeError('Unsupported Image Type')
        img = cropresize2.crop_resize(Image.open(old_paste),
            old_paste.mimetype, 0)
        rst = cls(old_paste.filename, old_paste.mimetype, 0)
        img.save(rst.path)
        filestat = os.stat(rst.path)
        rst.size = filestat.st_size
        return rst

    @property
    def is_image(self):
        return self.mimetype in IMAGE_MIMES

    @property
    def is_audio(self):
        return self.mimetype in AUDIO_MIMES

    @property
    def is_video(self):
        return self.mimetype in VIDEO_MIMES

    @property
    def is_pdf(self):
        return self.mimetype == 'application/pdf'

    @property
    def type(self):
        for t in ('image', 'pdf', 'video', 'audio'):
            if getattr(self, 'is_' + t):
                return t
        return 'binary'












