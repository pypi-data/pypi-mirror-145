#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-11-21 21:09
# @Author : Nuonuo
# @Site :
# @Software: PyCharm


import pymysql#mysql数据库
# ============================MySQL数据库类=============
class mysql:
    def __init__(self, host, user, pwd, db):
        self.host = host  # 主机名
        self.user = user  # 用户名
        self.pwd = pwd  # 密码
        self.database = db  # 数据库
        self.__Getconnect()
        # 初始化数据库 根据db自动选择数据库 并获取游标

    def __Getconnect(self):
        """得到连接信息返回: conn.cursor() """
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, database=self.database,
                                    charset="utf8")
        self.cur = self.conn.cursor()  # 获取游标
        print('-----初始化数据库成功-----')
        print('当前默认数据库:', self.database)

    def 新建_数据库(self, 数据库名):
        '''创建数据库 命令：create database <数据库名> '''
        return self.cur.execute('create database ' + 数据库名)

    def 新建_数据表(self, 数据表名):
        '''
        auto_increment   主键自动增加


        '''

        sql = '''
            create table ts1(
            id int auto_increment primary key not null,
            name varchar(100)
            键名 数据类型

            )

            '''
        print(sql, '自写sql语句')

    def 显示_所有数据库(self):
        self.cur.execute('show databases')
        print(self.cur.fetchall())

    def 显示_所有数据表(self):
        ''' 前提是必须 进入一个数据库 才可以调用此方法
        '''
        self.cur.execute("show tables")
        table_list = [tuple[0] for tuple in self.cur.fetchall()]
        return table_list

    def 删除_数据库(self, 数据库名):
        return self.cur.execute('drop database ' + 数据库名)

    def 查看_当前使用的数据库(self):
        return self.cur.execute('select database();')

    def 选择库(self, 数据库):
        """选择一个数据库为当前用户默认使用的数据库"""
        return self.cur.execute('use ' + 数据库)

    def 删除_数据表(self, text):
        '''传入要删除数据表name'''
        self.cur.execute('drop table ' + text)

    def 数据_是否存在(self, 表名, 字段, 内容):
        """SELECT * FROM ts流  WHERE `id` = '3000'
        'select * from test where value = 0 limit 10'
        limit关键词为条数或者页数
        """
        self.cur.execute("SELECT * FROM {} WHERE `{}` = '{}'".format(表名, 字段, 内容))

    def 插入_数据到数据表(self, table, val_obj):
        '''val_obj对象是字典类型 字段:内容  目前只能添加类型为文本类型
        插入数据
        "INSERT INTO [表名](Name) VALUES('Truman Capote')"#name可以写key也可以不写  不写则values按列排序写了则插入指定列
        #INSERT INTO `nuo_m3u8`.`测试`(`time`, `ts`) VALUES ('123', '李广龙')
        '''
        a = '''
        insert into [表名](time,name,[字段名]) values('{}')
        '''

        print(a.format(123), '自写sql语句')

    def 删除_数据表数据(self, table, 表达式):
        '''"DELETE FROM EMPLOYEE WHERE AGE > '%d'"
        表达式:   字段 =>< '123'
        where 后边的条件必须加 不加代表全部删除
        '''
        return self.cur.execute("DELETE FROM {} WHERE {}".format(table, 表达式))

    def 删除_全部数据_数据表(self, 表名):
        '''删除表中的记录：'''
        return self.cur.execute('delete from {};'.format(表名))

    def 查询_表中的记录(self, 表名):
        '''显示表中的记录：
        select 字段 from 表明;    #按字段查询 显示字段所有信息
        select 字段 from 表明 where 条件 ;
        where 条件后面跟的条件
        关系 >,<,>=,<=,!=
        逻辑 or and 与 和
        区间 id between 4 and 6;  闭区间

        范围查询 limit 0,10 参数 表示查询前10个 0代表开始位置 10代表向后查询10条
        'select * from ts limit 10;'
        '''
        return self.cur.execute('select * from {};'.format(表名))

    def 获取_表结构(self, 表名):
        '''desc 表名，或者show columns from 表名'''
        return self.cur.execute('DESCRIBE ' + 表名)
    def 获取_最大行数(self,表名):
        '获取数据表的最大行数返回元组'
        return self.cur.execute('select count(*) from {};'.format(表名))

    def 更改_表名(self, 原表名, 新表名):
        return self.cur.execute('rename table {} to {};'.format(原表名, 新表名))

    def 提交_更改(self):
        ''' #如果是写删操作需要提交才能生效'''
        return self.conn.commit()

    def 回滚_当前事务(self):
        self.conn.rollback()

    def 执行SQL(self, text):
        return self.cur.execute(text)

    def 取返回信息(self):
        '''获取执行命令结果'''
        linsi = self.cur.fetchall()
        return linsi

    def 关闭(self):
        '''关闭游标 关闭数据库'''
        self.cur.close()
        self.conn.close()

