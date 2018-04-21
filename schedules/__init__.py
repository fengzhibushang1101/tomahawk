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
from apscheduler.schedulers.blocking import BlockingScheduler

from lib.sql.base import db
from schedules.print_datetime import print_datetime

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1,
    'misfire_grace_time': 60 * 60 * 20,
}


jobstores = {
    "default": SQLAlchemyJobStore(engine=db),
    "extra": SQLAlchemyJobStore(engine=db, tablename='extra_jobs'),
}

scheduler = TornadoScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

