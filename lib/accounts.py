#!/usr/bin/env python
# _*_coding:utf-8_*_
''' 
    * @author: Xwl_Yu.
'''

from lib import db
from conf import settings
import hashlib
import os
from lib.person import *
from lib.study_record import *

class Accounts(object):
    '''
    账号父类
    '''
    storage = db.inter_db_handler(settings.ACCOUNT_DATABASE)
    human = Person()
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.new_password = None
        self.account_type = None
        self.status = None
        self.user_info = None

    def getter(self,username,password):
        '''
        获取账号
        :param username:
        :param password:
        :return:
        '''
        self.id = self.create_hash(username)
        self.username =  username
        self.password = self.create_hash(password)
        if self.__check_username():
            return False
        else:
            result = self.storage.quary(self.id)
            if self.password == result['account_data'].password:
                return result
            else:
                return False

    def setter(self,username,password,account_type,status):
        '''
        创建账号
        对应view类的register的方法，用以注册，创建账号时使用
        :param username:
        :param password:
        :param account_type:
        :param status:
        :return:
        '''
        self.id = self.create_hash(username)
        self.username = username
        self.password = self.create_hash(password)
        self.account_type = account_type
        self.status = status
        if self.__check_username():
            return self
        else:
            return False

    @staticmethod
    def create_hash(arg):
        '''
        hash创建方法
        使用用户名进行MD5检验计算出账号的ID和密码
        :param arg:
        :return:
        '''
        md5_id = hashlib.md5()
        md5_id.update(arg.encode('utf-8'))
        return md5_id.hexdigest()

    def __check_username(self):
        '''
        封装方法-检查账号的用户名是否存在数据库
        :return:
        '''
        if not os.path.exists('%s/%s' %(self.storage.db_path,self.id)):
            return True
        else:
            return False

    def set_info(self,account_data,name,sex,age):
        '''
        设置账号的基本信息
        :param account_data: 用户登录后的账号数据
        :param name: 用户的真实姓名
        :param sex: 用户的性别
        :param age: 用户的年龄
        :return:
        '''
        self.human.name = name
        self.human.sex = sex
        self.human.age = age
        account_data.user_info = self.human
        return account_data

    def change_password(self,account_data,new_password):
        self.new_password = self.create_hash(new_password)
        account_data['account_data'].pasword = self.new_password
        return account_data

class TeacherAccounts(Accounts):
    def __init__(self):
        super(TeacherAccounts,self).__init__()

    def getter(self,username,password):
        '''
        获取管理员账号
        :param username:
        :param password:
        :return:
        '''
        result = super(TeacherAccounts,self).getter(username,password)
        if result:
            return result
        else:
            return False

    def setter(self,username,password,account_type,status):
        '''
        创建管理员账号
        :param username:
        :param password:
        :param account_type:
        :param status:
        :return:
        '''
        super(TeacherAccounts,self).setter(username,password,account_type,status)

    def __check_username(self):
        '''
        检查账号的用户名是否存在数据库
        :return:
        '''
        if not os.path.exists('%s/%s' %(self.storage.db_path,self.id)):
            return True
        else:
            return False

class StudentAccounts(Accounts):
    def __init__(self):
        super(StudentAccounts,self).__init__()
        self.study_record = None

    def set_score(self,value):
        study_record = StudyRecord()
        study_record.score = value
        self.study_record = study_record

class AdminAccounts(Accounts):
    def __init__(self):
        super(AdminAccounts,self).__init__()

    def getter(self,username,password):
        '''
        获取管理员账号
        :param username:
        :param password:
        :return:
        '''
        result = super(AdminAccounts,self).getter(username,password)
        if result:
            return result
        else:
            return False

    def setter(self,username=settings.DEFAULT_ADMIN_ACCOUNT,password=settings.DEFAULT_ADMIN_PASSWORD,account_type=1,status=0):
        '''
        创建管理账号
        :param username:
        :param password:
        :param account_type:
        :param status:
        :return:
        '''
        super(AdminAccounts,self).setter(username,password,account_type,status)

    def __check_username(self):
        '''
        检查账号的用户名是否存在数据据
        :return:
        '''
        if not os.path.exists('%s/%s' %(self.storage.db_path,self.id)):
            return True
        else:
            return False




