#!/usr/bin/env python
# _*_coding:utf-8_*_
''' 
    * @author: Xwl_Yu.
'''

import sys
from lib import views

user_data = {
    'account_id':None,
    'is_authenticated':False,
    'account_data':None
}

student_view = views.StudentView()
teacher_view = views.TeacherView()
admin_view = views.AdminView()

def login(func):
    """
    登录函数
    :param func:
    :return:
    """
    def inner(*args,**kwargs):
        """这段有重复的if语句需要解决"""
        if isinstance(args[0],views.StudentView):
            if args[0].login(3):
                func(*args,**kwargs)
        elif isinstance(args[0],views.TeacherView):
            if args[0].login(2):
                func(*args,**kwargs)
        elif isinstance(args[0],views.AdminView):
            if args[0].login(1):
                func(*args,**kwargs)
    return inner

def interactive(menu,menu_dict,obj,flag):
    """
    主菜单接口，用户首先登录主菜单，选择进入具体的通道
    :param menu:
    :param menu_dict:
    :param obj:
    :param flag:
    :return:
    """
    exit_flag = True
    while exit_flag:
        print (menu)
        cmd = input(">>: ").strip()
        if cmd in menu_dict:
            eval(menu_dict[cmd])
        else:
            print ('\033[31;1m选项不存在\033[0m')

def homepage(obj = None):
    while True:
        menu = """
===============欢迎进入老男孩学校===============

                1. 学生登录通道
                2. 教师登录通道
                3. 管理员登录通道
                4. 退出
                
================================================
                """
        menu_dict = {
            '1':'student_homepage()',
            '2':'teacher_homepage()',
            '3':'admin_homepage()',
            '4':'exit_system()'
                     }
        interactive(menu,menu_dict,obj,flag = True)

def student_homepage(obj=student_view):
    menu="""
===============欢迎进入学员视图===============

               1. 注册账号
               2. 填写账户信息
               3. 查看账户信息
               4. 选择课程并付费
               5. 查看学习记录
               6. 修改密码
               7. 注销
               
==============================================
    """
    menu_dict = {
        '1':'sign_up(obj)',
        '2':'set_information(obj)',
        '3':'tell_information(obj)',
        '4':'choice_course(obj)',
        '5':'tell_record(obj)',
        '6':'change_password(obj)',
        '7':'sign_out(obj)'
    }
    interactive(menu,menu_dict,obj,flag=True)

def teacher_homepage(obj=teacher_view):
    menu="""
===============欢迎进入教师视图===============

               1. 填写账户信息
               2. 查看账户信息
               3. 班级管理
               4. 修改密码
               5. 注销
               
==============================================    
    """
    menu_dict = {
        '1':'set_information(obj)',
        '2':'tell_information(obj)',
        '3':'class_manage(obj)',
        '4':'change_password(obj)',
        '5':'sign_out(obj)'
    }
    interactive(menu,menu_dict,obj,flag = True)

@login
def class_manage(obj = teacher_view):
    menu = """
===============欢迎进入管理视图===============

               1. 选择班级
               2. 学生列表
               3. 批改作业
               4. 返回

==============================================
    """
    menu_dict = {
        '1':'choice_class(obj)',
        '2':'tell_students(obj)',
        '3':'homework_correcting(obj)',
        '4':'back_off(obj,teacher_homepage)'
    }
    interactive(menu,menu_dict,obj,flag = True)

def admin_homepage(obj=admin_view):
    menu= '''
===============欢迎进入管理视图===============

               1. 学校管理
               2. 学员管理
               3. 修改密码
               4. 注销
               
==============================================
    '''
    menu_dict = {
        '1':'school_admin_page(obj)',
        '2':'account_admin_page(obj)',
        '3':'change_password(obj)',
        '4':'sign_out(obj)'
    }
    interactive(menu,menu_dict,obj,flag=True)

@login
def school_admin_page(obj=admin_view):
    menu = """
===============欢迎进入管理视图===============

               1. 创建学校
               2. 创建课程
               3. 创建讲师
               4. 创建班级
               5. 返回
               
==============================================
    """
    menu_dict = {
        '1':'create_school(obj)',
        '2':'create_courses(obj)',
        '3':'create_teachers(obj)',
        '4':'create_classes(obj)',
        '5':'back_off(obj,admin_homepage)'
    }
    interactive(menu,menu_dict,obj,flag=True)

@login
def account_admin_page(obj=admin_view):
    menu = """
===============欢迎进入管理视图===============

               1. 学员信息
               2. 分配班级
               3. 返回
               
==============================================
    """
    menu_dict = {
        '1':'tell_student(obj)',
        '2':'assign_class(obj)',
        '3':'back_off(obj,admin_homepage)'
    }
    interactive(menu,menu_dict,obj,flag=True)

def sign_up(obj):
    """
    注册函数
    :param obj:传入需要的视图对象
    :return:
    """
    obj.register(3,0)

@login
def change_password(obj):
    """
    修改账号的密码
    :param obj: 传入需要的视图对象
    :return:
    """
    obj.change_password()

@login
def set_information(obj):
    """
    设置账号信息函数
    :param obj: 传入需要的视图
    :return:
    """
    obj.set_info()

@login
def tell_information(obj):
    """
    查看账户信息函数
    :param obj: 传入需要的视图对象
    :return:
    """
    obj.tell_info()

@login
def choice_course(obj):
    """
    选择课程函数
    :param obj:传入需要的视图对象
    :return:
    """
    obj.choice_courses()

@login
def tell_record(obj):
    """
    查看学习记录函数
    :param obj:
    :return:
    """
    obj.tell_record()


def sign_out(obj,page=homepage):
    """
    注销函数
    :param obj:
    :param page:传入需要的视图对象
    :return:
    """
    obj.logout()
    page()

def back_off(obj,page):
    """
    返回函数
    :param obj:传入需要的视图对象
    :param page:返回的页面属性
    :return:
    """
    obj.back_off()
    page()

def exit_system():
    """
    退出系统函数
    :return:
    """
    print ('\033[34;1m欢迎使用本系统，下次再见！\033')
    sys.exit()

@login
def create_school(obj):
    """
    创建学校函数
    :param obj:传入需要的视图对象
    :return:
    """
    obj.create_school()

@login
def create_courses(obj):
    """
    创建课程函数
    :param obj:传入需要的视图对象
    :return:
    """
    obj.create_courses()

@login
def create_classes(obj):
    """
    创建班级函数
    :param obj:传入需要的视图函数
    :return:
    """
    obj.create_classes()

@login
def create_teachers(obj):
    obj.create_teachers(2,0)

@login
def tell_student(obj):
    obj.tell_student()

@login
def assign_class(obj):
    obj.assign_class()

@login
def start_teach(obj):
    obj.start_teach()

@login
def tell_students(obj):
    obj.tell_students()

@login
def homework_correcting(obj):
    obj.homework_correcting()

@login
def choice_class(obj):
    obj.choice_class()

def run():
    homepage()





























