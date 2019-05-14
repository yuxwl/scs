#!/usr/bin/env python
# _*_coding:utf-8_*_
''' 
    * @author: Xwl_Yu.
'''

from lib.accounts import *
from lib.schools import *
from lib.courses import *
from lib.classes import *
from lib.db import *
from core.logger import logger

class View(object):
    '''
    视图父类
    '''
    account = Accounts()        #关联Accounts对象，后续的登录，注册都需要使用
    school = Schools()
    account_storage = inter_db_handler(settings.ACCOUNT_DATABASE)
    base_storage = inter_db_handler(settings.BASE_DATABASE)
    user_data = {
        'account_id':None,
        'is_authenticated':False,
        'account_data':None
    }
    base_data = {
        'school':None,
        'course':{},
        'class':{},
        'teacher':{},
        'student':{}
    }
    access_log = logger('access')

    def __init__(self):
        self.menu = None,
        self.menu_dict = None,
        self.result = None,
        self.account_obj = None

    def login(self,account_type):
        '''
        登录视图
        :param account_type:
        :return:
        '''
        """
        """
        exit_flag = True
        while exit_flag:
            if not self.user_data['is_authenticated']:
                username = input('Please input username: ').strip()
                password = input('Please input password: ').strip()
                account_obj = self.account.getter(username,password)
                if account_obj and account_obj['account_data'].account_type == account_type:
                    self.user_data = account_obj
                    self.user_data['is_authenticated'] = True
                    print ('\033[34;1m[%s] Login Success!\033[0m'%username)
                    self.access_log.info('[%s] Login Success!' %username)
                    return self.user_data
                else:
                    print ('\033[31;1mUsername or Password error!\033[0m')
                    return False
            else:
                return self.user_data

    def register(self,account_type,account_status):
        '''
        注册视图
        支持注册后立即登录系统
        :param account_type:
        :param account_status:
        :return:
        '''
        exit_flag = True
        while exit_flag:
            username = input('Please input username: ').strip()
            password = input('please input password ').strip()
            re_password = input('please input password confirmation: ').strip()
            account_obj = self.account.setter(username,password,account_type,account_status)
            """下面代码，判断用户名是否等于密码。如果等于的话会报错。坦诚说,
            是因为注册账号时的account_id是用用户名的MD5算出来的，如果密码和用户名一样，账号的ID就和密码的MD5一样.
            所以添加这行代码,不让用户名和密码一样。其实也是一种伪装自己bug的方法（笑哭脸）。后续会改进
            """
            if not username or not password:
                print ("\033[31;1mError:Username or Password cannot be null!\033[0m")
                continue
            elif username == password:
                print ("\033[31;1mError:Username Cannot be equal to Password!\033[0m")
                continue
            elif password != re_password:
                print ("\033[31;1mError:Password do  not match!\033[0m")
                continue
            elif not account_obj:
                print ("\033[31;1mThe user has already existed!\033[0m")
            else:
                #注册新账号
                print ('\033[34;1mRegistry Success!\033[0m')
                print ('\033[34;1m"%s" account login!\033[0m' %username)
                self.user_data['account_id'] = account_obj.id
                self.user_data['is_authenticated'] = True
                self.user_data['account_data'] = account_obj
                self.account_storage.nonquary(account_obj.id,self.user_data)
                exit_flag = False

    def tell_info(self):
        '''
        展示账号信息方法
        本方法是一个视图，用来展示用户的人个信息
        :return:
        '''
        user_data_obj = self.user_data['account_data']
        user_info_data = user_data_obj.user_info
        #通过反射，判断user_info_data 对象中是否有相对应的属性，如有就赋值，没有就设置为Null
        if hasattr(user_info_data,'name'):
            name = getattr(user_info_data,'name')
        else:
            name = 'Null'

        if hasattr(user_info_data,'age'):
            age = getattr(user_info_data,'age')
        else:
            age = 'Null'

        if hasattr(user_info_data,'sex'):
            sex = getattr(user_info_data,'sex')
        else:
            sex = 'Null'

        info = '''
==================账户信息==================
         ID：         \033[34;1m%s\033[0m
         Account：    \033[34;1m%s\033[0m
         Fullname：   \033[34;1m%s\033[0m
         Age：        \033[34;1m%s\033[0m
         Sex：        \033[34;1m%s\033[0m
         Type：       \033[34;1m%s\033[0m
         Status:      \033[34;1m%s\033[0m
============================================
        ''' %(user_data_obj.id,user_data_obj.username,name,age,
              sex,user_data_obj.account_type,user_data_obj.status)
        print (info)

    def set_info(self):
        '''
        设置个人信息
        :return:
        '''
        exit_flag = True
        while exit_flag:
            fullname = input('Please input your fullname:').strip()
            sex = input('Please input your sex:').strip()
            age = input('Please input your age:').strip()
            account_obj = self.account.set_info(self.user_data['account_data'],fullname,sex,age)
            if account_obj:
                self.user_data['account_data'] = account_obj
                self.account_storage.nonquary(self.user_data['account_id'],self.user_data)
                print ('\033[34;1mSet Success!\033[0m')
                exit_flag = False

    def change_password(self):
        '''
        修改账号密码视图方法
        :return:
        '''
        exit_flag = True
        while exit_flag:
            old_password = input('Please input your old password:').strip()
            new_password = input('Please input your new password:').strip()
            re_new_password = input('Please input your new password confirmation:').strip()
            account_obj = self.account.getter(self.user_data['account_data'].username,old_password)
            if account_obj:
                if not new_password or re_new_password:
                    print ("\033[31;1mPassword cannot be null!\033\[0m")
                elif new_password != re_new_password:
                    print ("\033[31;1mError: Password do not match!\033[0m")
                else:
                    result = self.account.change_password(account_obj,new_password)
                    if result:
                        self.account_storage.nonquary(self.user_data['account_id'],result)
                        exit_flag = False
            else:
                print ('\033[31;1mError: Old password error!\033[0m')
    def logout(self):
        '''
        退出视图方法
        :return:
        '''
        if self.user_data['account_data']:
            username = self.user_data['account_data'].username
            self.user_data = {
                'account_id':None,
                'is_authenticated':False,
                'account_data':None
            }
            print ('\033[34;1m[%s] Account logout!\033[0m' %username)
            self.access_log.info('[%s] Account logout!' %username)

    @staticmethod
    def back_off():
        '''
        返回视图方法
        :return:
        '''
        print ('\033[34;1mBack off!\033[0m')

class StudentView(View):
    '''
    学生视图
    '''
    account = StudentAccounts()
    user_data = {
        'account_id':None,
        'is_authenticated':False,
        'account_data':None,
        'student_data':{'school':None,'course':[],'class':[],'teacher':[]},
        'study_record':None
    }

    def __init__(self):
        super(StudentView,self).__init__()


    def register(self,account_type,account_status):
        '''
        注册视图方法
        :param account_type:
        :param account_status:
        :return:
        '''
        print ('创建学生'.center(50,'='))
        #重用父类的注册账号代码
        super(StudentView,self).register(account_type,account_status)

    def choice_courses(self):
        '''
        选课视图方法
        :return:
        '''
        print ('购买课程'.center(50,'='))
        exit_flag = True
        while exit_flag:
            school_name = input('Please choice school:').strip()
            course_name = input('Please choice course:').strip()
            school_result = self.school.getter(school_name)
            #调试代码
            print (school_result)
            print (self.user_data)
            #调试代码
            if not school_name or not course_name:
                print ('\033[31;1mError:Input cannot null!\033[0m')
                exit_flag = False
            elif not school_result:
                print ("\033[31;1mSchool does not exist\033[0m")
                exit_flag = False
            elif course_name not in school_result['course']:
                print ('\033[31;1mCourse does not exist\033[0m')
                exit_flag = False
            elif course_name in self.user_data['student_data']['course']:
                print ('\033[31;1mThe course has been purchased\033[0m')
                exit_flag = False
            else:
                course_price = school_result['course'][course_name].price
                if self.payment(course_price):
                    account_name = self.user_data['account_data'].username
                    school_result['course'][course_name].students.append(account_name)
                    school_result['student'][account_name] = self.user_data
                    self.user_data['student_data']['school'] =school_name
                    self.user_data['student_data']['course'].append(course_name)
                    self.base_storage.nonquary(school_name,school_result)
                    self.account_storage.nonquary(self.user_data['account_id'],self.user_data)
                    print ("\033[34;1mThe success of the course purchase!\033[0m")
                    exit_flag = False
                else:
                    print ('\033[31;1mError: Failure of course purchase!\033[0m')

    def payment(self,pay):
        '''
        付款视图方法
        该方法是一个假方法，并没有任何账号支持的动作。只是比较一下用户输入的价格是否和课程的价格一致
        :return:
        '''
        exit_flag = True
        while exit_flag:
            tuition = input('Please pay tuition [%s RMB]: '%pay).strip()
            if not tuition:
                print ("\033[031;1mError:Tuition cannot be null\033[0m")
            else:
                if int(tuition) == pay:
                    return True
                else:
                    return False

    def tell_record(self):
        if not self.user_data['account_data'].study_record:
            study_record = '成绩未公布'
        else:
            study_record = self.user_data['account_data'].study_record.score
        info = '''
================学习记录=================

            Score:  \033[034;1m%s\033[0m

=========================================
        '''%study_record
        print (info)


class TeacherView(View):
    '''
    老师视图
    '''
    user_data = {
        'account_id':None,
        'is_authenticated':False,
        'account_data':None,
        'teacher_data':{'school':None,'course':[],'class':[]}
    }

    def __init__(self):
        super(TeacherView,self).__init__()
        self.teach_class = None

    def choice_class(self):
        '''
        选择班级视图方法
        :return:
        '''
        exit_flag = True
        while exit_flag:
            class_name = input('Please input name of class:').strip()
            school_result = self.base_storage.quary(self.user_data['teacher_data']['school'])
            if class_name not in school_result['class']:
                print ('\033[34;1mError,You input class error!\033[0m')
            else:
                if school_result['class'][class_name].teacher != self.user_data['account_data'].username:
                    print ('\033[31;1mError: You do not teach the class!\033[0m')
                else:
                    self.teach_class = class_name
                    print ('\033[31;1mChoice class success!\033[0m')
                    exit_flag = False
                    break

    def tell_students(self):
        '''
        查看班级的学生视图方法
        :return:
        '''
        if not self.teach_class:
            print ('\033[31;1mError: Please choice first!\033[0m')
        else:
            print ('班级学生列表'.center(50,'='))
            print ('Class: \033[34;1m%s\033[0m' %self.teach_class)
            print ('Student: ')
            school_result = self.base_storage.quary(self.user_data['teacher_data']['school'])

            for student in school_result['student']:
                if self.teach_class in school_result['student'][student]['student_data']['class']:
                    print ('\033[34;1m%s\033[0m'%student)
            print ('='.center(50,'='))

    def homework_correcting(self):
        '''
        修改学生成绩的视图方法
        :return:
        '''
        if not self.teach_class:
            print ('\033[31;1mError: Please choice class first!\033[0m')
        else:
            school_result = self.base_storage.quary(self.user_data['teacher_data']['school'])
            print ('作业批改'.center(50,'='))
            exit_flag = True
            while exit_flag:
                student_name = input('Please input name of student:').strip()
                score = input('Please input score of student: ').strip()
                if not student_name or not score:
                    print ('\033[31;1mError,Student name or Student score cannot be null!\033[0m')
                elif student_name not in school_result['student']:
                    print ('\033[31;1m%s i not your student!\033[0m' %student_name)
                elif self.teach_class not in school_result['student'][student_name]['student_data']['class']:
                    print ('\033[31;1mError: %s is not your student!\033[0m' %student_name)
                else:
                    confirm = input('Confirm input "yes". Back off input "B": ').strip()
                    if confirm.upper() == 'YES':
                        username_hash = self.account.create_hash(student_name)
                        student_data = self.account_storage.quary(username_hash)
                        student_data['account_data'].set_score(score)
                        self.account_storage.nonquary(username_hash,student_data)
                        print ('\033[34;1m[%s]homework to be corrected\033[0m' %student_name)
                    elif confirm.upper() == 'B':
                        exit_flag = False

class AdminView(View):
    '''
    管理员视图
    '''
    account = Accounts()
    account.setter(username=settings.DEFAULT_ADMIN_PASSWORD,password=settings.DEFAULT_ADMIN_PASSWORD,
                   account_type=1,status=0)
    user_data = {
        'account_id':account.id,
        'is_authenticated':False,
        'account_data':account
    }
    account_storage = inter_db_handler(settings.ACCOUNT_DATABASE)
    account_storage.nonquary(account.id,user_data)

    def __init__(self):
        super(AdminView,self).__init__()

    def login(self,account_type):
        '''
        管理员登录视图
        :param account_type:
        :return:
        '''
        account_result = super(AdminView,self).login(account_type)
        if not account_result:
            return False
        else:
            return account_result

    def create_school(self):
        '''
        管理员创建学校视图方法
        :return:
        '''
        exit_flag = True
        while exit_flag:
            print ('创建学校'.center(50,'='))
            name = input('Please input name of school: ').strip()
            city = input('Please input city of school: ').strip()
            location = input('Please input address os school: ').strip()
            school_result = self.school.setter(name,city,location)
            if not name or not city or not location:
                print ('\033[31;1mError: Cannot be null!\033[0m')
                exit_flag = False
            elif not school_result:
                print ("\033[31;1mSchool has already existed!\033[0m")
                exit_flag = False
            else:
                self.base_data['school'] = school_result
                self.base_storage.nonquary(name,self.base_data)
                print ('\033[34;1mCreate school success !\033[0m')
                exit_flag = False

    def create_courses(self):
        """
        管理员创建课程视图方法
        :return:
        """
        print('创建课程'.center(50,'='))
        exit_flag = True
        while exit_flag:
            course_name = input('Please input course name: ')
            price = input('Please input price: ')
            period = input('Please input term: ')
            school_name = input('Please input associated school: ')
            school_result = self.school.getter(school_name)

            if not course_name or not price or not period or not school_name:
                print ('\033[31;1mCannot be null!\033[0m')
                exit_flag = False
            elif not price.isdigit() or not period.isdigit():
                print ('\033[31;1mPrice and Period must be integer!\033[0m')
                exit_flag = False
            elif not school_result:
                print ('\033[31;1mSchool does not exist\033[0m')
                exit_flag = False
            elif course_name in school_result['course']:
                print ('\033[31;1mCourse has already existed!\033[0m')
                exit_flag = False
            else:
                course_obj = Courses(course_name,int(price),int(period))
                if course_obj:
                    school_result['course'][course_name] = course_obj
                    self.base_storage.nonquary(school_name,school_result)
                    print ('\033[34;1mCreate course success!\033[0m')
                    exit_flag = False
                else:
                    print ('\033[31;1mCreate course failed!\033[0m')
                    exit_flag = False

    def create_classes(self):
        """
        创建班级视图方法
        :return:
        """
        print ("创建班级".center(50,'='))
        exit_flag = True
        while exit_flag:
            class_name = input('Please input class name: ').strip()
            school_name = input('Please input associated school: ').strip()
            course_name = input('Please input associated course: ').strip()
            teacher_name = input('Please input associated teacher: ').strip()
            school_result = self.school.getter(school_name)
            if not class_name or not course_name or not school_name:
                print ('\033[31;1mCannot be null!\033[0m')
                exit_flag = False
            elif not school_result:
                print ('\033[31;1mSchool does not exist\033[0m')
                exit_flag = False
            elif not course_name in school_result['course']:
                print ('\033[31;Course does not exist\033[0m')
                exit_flag = False
            elif not teacher_name in school_result['teacher']:
                print ('\033[31;1mTeacher does not exist\033[0m')
                exit_flag = False
            else:
                course_obj = school_result['course'][course_name]
                course_obj.classes.append(class_name)
                classes_obj = Classes(class_name,teacher=teacher_name)
                school_result['class'][class_name] = classes_obj
                self.base_storage.nonquary(school_name,school_result)
                print ('\033[034;1mCreate class success!\033[0m')
                exit_flag = False

    def create_teachers(self,account_type,account_status):
        """
        创建老师视图方法
        :param account_type:
        :param accout_status:
        :return:
        """
        print ('创建老师'.center(50,'='))
        exit_flag = True
        while exit_flag:
            username = input('Please input username: ').strip()
            password = input('Please input password: ').strip()
            re_password = input('Please input password confirmation: ').strip()
            school_name = input('Please input associated school: ').strip()
            school_result = self.school.getter(school_name)
            account_obj = self.account.setter(username,password,account_type,account_status)

            #判断用户名是否等于密码，如果等于的话会报错，因为注册账号的account_id 是用用户名的MD5计算出来，如果用户名和密码一样，
            #账号的ID和密码的MD5一样，所以添加这行代码
            if not username or not password:
                print ('\033[31;1mError: Username or Password cannot be null!\033[0m')
                exit_flag = False
            elif not school_result:
                print ('\033[31;1mError: School does not exist\033[0m')
                exit_flag = False
            elif username == password:
                print ('\033[31;1mError: Username Cannot be equal to Password！\033[0m')
                exit_flag = False
            elif password != re_password:
                print ('\033[31;1mError:Password do not match!\033[0m')
                exit_flag = False
            elif not account_obj:
                print ('\033[31;The user has already existed!\033[0m')
            else:
                #创建新老师账号
                TeacherView.user_data['account_id'] = account_obj.id
                TeacherView.user_data['account_data'] = account_obj
                TeacherView.user_data['teacher_data']['school']=school_name

                school_result['teacher'][username] = account_obj
                self.base_storage.nonquary(school_name,school_result)
                self.account_storage.nonquary(account_obj.id,TeacherView.user_data)
                print ('\033[34;1mRegistry Success!\033[0m')
                exit_flag = False

    def tell_student(self):
        """
        管理员查看学校中的学生视图方法
        :return:
        """
        exit_flag = True
        while exit_flag:
            school_name = input('Please input school: ').strip()
            school_result = self.school.getter(school_name)
            if not school_name:
                print ('\033[31;1mError: School cannot be null!\033[0m')
                exit_flag = False
            elif not school_result:
                print ("\033[31;1mError:School does not exist!\033[0m")
                exit_flag = False
            else:
                students = school_result['student']
                if not students:
                    print ('\033[31;1mStudents does not exist!\033[0m')
                    exit_flag = False
                else:
                    for student_name in students:
                        student_id = students[student_name]['account_id']
                        account_data = students[student_name]['account_data']
                        student_data = students[student_name]['student_data']
                        account_type = account_data.account_type
                        account_status = account_data.status
                        account_school = student_data['school']
                        account_course = ','.join(student_data['course'])
                        account_class = ','.join(student_data['class'])
                        if not account_class:
                            account_class = "未分配班级"
                        account_teacher = ','.join(student_data['teacher'])
                        if not account_teacher:
                            account_teacher = '未分配老师'
                        info = '''
==================学生信息==================

         ID：         \033[34;1m%s\033[0m
         Account：    \033[34;1m%s\033[0m
         Type：       \033[34;1m%s\033[0m
         Status:      \033[34;1m%s\033[0m
         School:      \033[34;1m%s\033[0m
         Course:      \033[34;1m%s\033[0m
         Class:       \033[34;1m%s\033[0m
         Teacher:     \033[34;1m%s\033[0m
         
============================================                       
                        '''%(student_id,student_name,account_type,account_status,account_school,
                             account_course,account_class,account_teacher)
                        print (info)
                    exit_flag = False

    def assign_class(self):
        """
        管理员分配班级视图方法
        :return:
        """
        print ("分配班级".center(50,'='))
        exit_flag = True
        while exit_flag:
            school_name = input('Please input name of school: ').strip()
            student_name = input('Please input account of student: ').strip()
            course_name = input('Please input name of course: ').strip()
            class_name = input('Please ipnut name of class: ').strip()
            school_result = self.school.getter(school_name)
            if not school_name or not student_name or not class_name or not course_name:
                print ('\033[31;1mError: School or Student or Class or Course cannot be null!\033[0m')
                exit_flag = False
            elif not school_result:
                print ('\033[31;1mError: School does not exist!\033[0m')
            else:
                school_student = school_result['student']
                school_course = school_result['course']
                school_class = school_result['class']
                if student_name not in school_student:
                    print ('\033[31;1mError:Student does not exist!\033[0m')
                    exit_flag = False
                else:
                    student_data = school_student[student_name]
                    if course_name not in school_course:
                        print ('\033[31;1mError: Course does not exits!\033[0m')
                        exit_flag = False
                    elif class_name not in school_class:
                        print ('\033[31;1mError: Class does not exist!\033[0m')
                        exit_flag = False
                    elif course_name not in student_data['student_data']['course']:
                        print ('\033[31;1mError: Student does not buy Course!\033[0m')
                        exit_flag = False
                    elif class_name not in school_course[course_name].classes:
                        print ('\033[31;1mError: Course!\033[0m')
                        exit_flag = False
                    else:
                        school_student[student_name]['student_data']['class'].append(class_name)
                        school_student[student_name]['student_data']['teacher'].append(school_class[class_name].teacher)
                        self.account_storage.nonquary(school_student[student_name]['account_id'],school_student[student_name])
                        self.base_storage.nonquary(school_name,school_result)
                        print ('\033[34;1mStudents have bound course!\033[0m')
                        exit_flag = False








































