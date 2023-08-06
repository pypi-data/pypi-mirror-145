"""

.. Hint::
    时间工具类 时间统计


.. literalinclude:: ../../../pyefun/timeUtil_test.py
    :language: python
    :caption: 代码示例
    :linenos:

"""

import datetime
import time


class 时间统计():
    """
    计时器，对于需要计时的代码进行with操作：
    with 计时器() as timer:
        ...
        ...
    print(timer.cost)
    ...
    """

    def __init__(self, 名称=""):
        self.开始()
        self.名称 = 名称
        self.zstart = self.start
        # if self.名称:
        #     print("时间统计: %s 开始 %s" % (self.名称, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def __enter__(self):
        return self

    def 开始(self):
        """
        重新计算开始时间
        """
        self.start = time.perf_counter()

    def 取耗时(self, 名称=""):
        """
        每次计时后重置 如果需要总耗时的话 取总耗时() 即可
        """
        self.end = time.perf_counter()
        self.ms = int((self.end - self.start) * 1000)
        self.开始()
        if 名称 != "":
            print("时间统计: %s %s %sms" % (self.名称, 名称, self.ms))
        elif self.名称 != "":
            print("时间统计: %s %sms" % (self.名称, self.ms))

        return self.ms

    def 取总耗时(self):
        """
        自对象创建以来的总耗时
        """
        self.end = time.perf_counter()
        self.ms = int((self.end - self.zstart) * 1000)
        return self.ms

    def 取毫秒(self):
        return self.取耗时()

    def 取秒(self):
        return self.取耗时() / 1000

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.名称 != "":
            print("时间统计: %s 结束 %sms %s" % (self.名称, self.取总耗时(), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return exc_type is None


def 计时器():
    return 时间统计()

def 现行时间戳(位数):
    '13或10'
    if 位数==13:
        return int(round(time.time() * 1000))
    elif 位数==10:
        return int(time.time())
    else:
        return '传入参数错误',位数
def sleep(秒):
    '延迟单位秒'
    time.sleep(秒)
def 取启动时间():
    '返回浮点数时间，计算指定程序,函数运行的时间'
    return time.perf_counter()
def 获取当前时间(格式):
    '格式1 = 2020-10-09 22:11:52   格式2 = 2020-10-09 格式3= 22:13:37 格式4= 2020年10月17日18时27分40秒'
    '''
    %a  # 本地(local) 简化星期名称
    %A  # 本地完整星期名称
    %b  # 本地简化月份名称
    %B  # 本地完整月份名称
    %c  # 本地相应的日期和时间表示
    %d  # 一个月中的第几天（01-31）
    %H  # 一天中的第几个小时（24小时制00-23）
    %I  # 第几个小时（12小时制01-12）
    %j  # 一年中的第几天（001-366）
    %m  # 月份（01-12）
    %M  # 分钟数（00-59）
    %p  # 本地am或pm的相应符
    %S  # 秒（01-60）
    %U  # 一年中的星期数。（00-53 星期天是一个星期的开始）第一个星期天之前的所有天数都放在第0周
    %w  # 一个星期中的第几天（0-6 0是星期天）
    %W  # 和%U基本相同，不同的是%W以星期一为一个星期的开始
    %x  # 本地相应日期
    %X  # 本地相应时间
    %y  # 去掉世纪的年份（00-99）
    %Y  # 完整的年份
    %z  # 时区的名字
    '''
    if 格式==1:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())#2020-10-09 22:11:52
    elif 格式==2:
        return time.strftime("%Y-%m-%d", time.localtime())#2020-10-09
    elif 格式==3:
        return time.strftime("%H:%M:%S", time.localtime())#22:13:37
    elif 格式==4:
        return time.strftime("%Y{}%m{}%d{}%H{}%M{}%S{}", time.localtime()).format('年','月','日','时','分','秒')#2020年10月17日18时27分40秒