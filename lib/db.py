#!/usr/bin/env python
# _*_coding:utf-8_*_
''' 
    * @author: Xwl_Yu.
'''

import abc
import pickle
import os

class AbstractDatabase(object,metaclass = abc.ABCMeta):
    '''
    Database抽象类，对所有以后扩展数据库类的子类进行归一化
    '''
    def __init__(self,conn_params,username,password):
        self.conn_params = conn_params
        self.username = username
        self.password = password
        self.db_path = '%s/%s' %(conn_params['path'],conn_params['name'])

    @abc.abstractmethod
    def connect(self):
        '''
        连接数据库方法
        :return:
        '''
        pass

    @abc.abstractmethod
    def quary(self,sql):
        '''
        查询类的操作
        :param sql:
        :return:
        '''
        pass

    @abc.abstractmethod
    def nonquary(self,sql):
        '''
        非查询类的操作
        :param sql:
        :return:
        '''
        pass

    @abc.abstractmethod
    def close(self):
        '''
        关闭数据方法
        :return:
        '''
        pass

class FileStorage(AbstractDatabase):
    '''
    文件存储类
    '''
    def __init__(self,conn_params,username,password):
        super(FileStorage,self).__init__(conn_params,username,password)

    def connect(self):
        '''
        数据库连接方法
        但由于FileStorage 类是使用文件进行存储，不需要先连接数据库
        所以connect在FileStorage类中，主要是检查self.db_path的路径是否存在
        :return:
        '''
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)

    def quary(self,file):
        '''
        读取数据到内存中
        :param file: 读取文件名
        :return: 返回信息
        '''
        with open('%s/%s' %(self.db_path,file),'rb') as f:
            data = pickle.load(f)
            return data

    def nonquary(self,file,data):
        '''
        从内存中把数据写入到数据库中
        :param file: 写入的文件名
        :param data: 保存的数据
        :return:
        '''
        with open('%s/%s' %(self.db_path,file),'wb') as f:
            pickle.dump(data,f)
        return True

    def close(self):
        pass

class MysqlStorage(AbstractDatabase):
    '''
    Mysql 存储类，扩展功能
    '''
    def __init__(self,conn_params,username,password):
        super(MysqlStorage,self).__init__(conn_params,username,password)

    def connect(self):
        pass

    def quary(self,sql):
        pass

    def nonquary(self,sql):
        pass

    def close(self):
        pass

def inter_db_handler(conn_params):
    '''
    db_handler接口
    为File_storage类，Mysql_storage类定义一个接口，创建对象时可以通过这个接口创建
    :param conn_params: 数据库连接参数
    :return:
    '''
    if conn_params['engine'] == 'file_storage':
        file_db = FileStorage(conn_params,conn_params['username'],conn_params['password'])
        return file_db

    #扩展功能，支持mysql存储
    elif conn_params['engine'] == 'mysql_storage':
        mysql_db = MysqlStorage(conn_params,conn_params['username'],conn_params['password'])
        return mysql_db

def inter_db_connect(obj):
    '''
    connect 接口，所有的数据库连接都使用该接口
    :param obj:
    :return:
    '''
    obj.connect()

def inter_file_load_data(obj,file):
    obj.load_data(file)

def inter_file_dump_data(obj,file,data):
    obj.dump_data(file,data)









