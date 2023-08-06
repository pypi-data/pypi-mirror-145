#版权.py
class a():
    def __init__(self,x):
        self.b=x
    def 抄袭(self,x):
        return self.b>x.b
玩=lambda x:x.b
我的世界=a(0)
迷你世界=a(1)
奶块=a(0)
垃圾=a(1)

'''
#__init__
>>> from 版权 import *
>>> 玩(迷你世界)==玩(垃圾)
True
>>> 迷你世界.抄袭(我的世界)
True
>>> 迷你世界.抄袭(奶块)
True
>>> 奶块.抄袭(我的世界)
False
>>> 奶块!=垃圾
True
>>>

'''
