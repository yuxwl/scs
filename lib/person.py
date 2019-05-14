#!/usr/bin/env python
# _*_coding:utf-8_*_
''' 
    * @author: Xwl_Yu.
'''
class Person(object):
    '''
    Person类
    '''
    def __init__(self):
        self.__name = None
        self.__sex = None
        self.__age = None

    @property
    def name(self):
        return self.__name

    @property
    def sex(self):
        return self.__sex

    @property
    def age(self):
        return self.__age

    @name.setter
    def name(self,value):
        self.__name = value

    @sex.setter
    def sex(self,value):
        self.__sex = value

    @age.setter
    def age(self,value):
        self.__age = value

class Teacher(Person):
    def __init__(self):
        super(Teacher,self).__init__()

class Student(Person):
    def __init__(self):
        super(Student,self).__init__()
        self.__student_data = None
        self.__study_record = None

    @property
    def student_data(self):
        return self.__student_data

    @property
    def study_record(self):
        return self.__study_record

    @student_data.setter
    def student_data(self,value):
        self.__student_data = value

    @study_record.setter
    def study_record(self,value):
        self.__study_record = value









