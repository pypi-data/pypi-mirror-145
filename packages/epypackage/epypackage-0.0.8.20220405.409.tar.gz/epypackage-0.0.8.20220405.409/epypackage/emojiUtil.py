# -*- coding: utf-8 -*-
# @Time : 2022-01-08 20:53
# @Author : LiGuangLong
# @File : emojiUtil.py
# @Software: PyCharm

import emoji
def 表情_解码(string):
	"""解码到正常文本"""
	return emoji.demojize(string)

def 表情_编码(string):
	"""把特殊标记文本转表情显示"""
	return emoji.emojize(string)