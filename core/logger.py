#!/usr/bin/env python
# _*_coding:utf-8_*_
''' 
    * @author: Xwl_Yu.
'''

import logging
from conf import settings

def logger(log_type):
    '''
    日志函数
    :param log_type: 日志类型
    :return:
    '''
    #create logger
    my_logger = logging.getLogger(log_type)
    my_logger.setLevel(settings.LOG_LEVEL)

    #create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)

    #create file handler and set lelvel to warring
    log_file = '%s/log/%s' %(settings.BASE_DIR,settings.LOG_TYPES[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)

    #create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    #add ch and fh to logger
    my_logger.addHandler(ch)
    my_logger.addHandler(fh)
    return my_logger

