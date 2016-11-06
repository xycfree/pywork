#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 16-11-4 下午10:07
# @Author  : ubuntu
# @Link    : xycfree@163.com
# @Version : 

import os
import threading
import random
mydata = threading.local()
mydata.number = 42
print mydata.number
log = []

def f():
   for i in range(100):
      mydata.number = random.randint(1,100)
      log.append(mydata.number)

for i in range(10):
   thread = threading.Thread(target=f)
   thread.start()
   thread.join()

print 'log: ', log
print(mydata.number)


