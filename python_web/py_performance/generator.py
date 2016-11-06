#!/usr/bin/env python
#coding:utf-8
'''
	生成器
'''
def generator_function():
	for i in range(10):
		yield i

for item in generator_function():
	print(item)

#菲波纳契
def fibon(n):
	a = b = 1
	for i in range(n):
		yield a
		a, b = b, a + b

print 'fibon start ...'
for x in fibon(10):
	print(x)

#filter
num_list = range(-10,10)
less_than_zero = filter(lambda m: m < 0, num_list)
print(list(less_than_zero))
