#!/usr/bin/env python
# _*_coding:utf-8_*_
''' 
    * @author: Xwl_Yu.
'''

class Courses(object):
    def __init__(self,name,price,period,classes_list=[],student_list=[]):
        self.name = name
        self.__price = price
        self.__period = period
        self.classes = classes_list
        self.students = student_list

    @property
    def price(self):
        return self.__price

    @property
    def period(self):
        return self.__period

    @price.setter
    def price(self,value):
        if isinstance(value,int):
            self.__price = value
        else:
            raise TypeError('Error: Course price [%s] must be int' %value)

    @period.setter
    def period(self,value):
        if isinstance(value,int):
            self.__period = value
        else:
            raise TypeError('Error: Course Period [%s] must be int' %value)
