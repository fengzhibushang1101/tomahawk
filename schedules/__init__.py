#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/14 0014 上午 10:39
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.tornado import TornadoScheduler

from config import settings

import datetime

from lib.utils.logger_utils import logger


def print_datetime():
    print datetime.datetime.now()
    logger.info(datetime.datetime.now())


executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1,
    'misfire_grace_time': 60 * 60 * 20,
}

db_info = settings.db

jobstores = {
    "default": SQLAlchemyJobStore(url="mysql://%s:%s@%s/%s" % (
    db_info["user"], db_info["password"], db_info["host"], db_info["db_name"]))
}

scheduler = TornadoScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

