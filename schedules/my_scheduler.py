#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/21 0021 下午 7:37
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import traceback
import uuid

import pytz
import ujson as json

from apscheduler.jobstores.base import ConflictingIdError

from lib.sql.scheduler import Scheduler, CANCELLED, ACTIVE
from lib.sql.session import sessionCM
from lib.utils.error_utils import ErrorArgumentError
from lib.utils.logger_utils import logger
from schedules import scheduler
from schedules.callback import aps_callback

TIMEZONE = pytz.timezone('Asia/Shanghai')

CALLBACK_FUNC = aps_callback

TRIGGER_LIST = ["interval", "cron", "date"]


class MyScheduler(object):

    def __init__(self):
        self.scheduler = scheduler

    def add_my_job(self, trigger, res_type, res_url, job_id, job_name, schedule_args, schedule_type, func_args,
                   user_id=0, remark="", job_store="default"):
        if trigger not in TRIGGER_LIST:
            raise ErrorArgumentError
        job_id = job_id or str(uuid.uuid1())
        callback_args = [res_type, res_url, func_args, job_id]
        try:
            job = self.add_job_to_scheduler(trigger, job_id, job_name, schedule_args, callback_args, job_store)
            with sessionCM() as session:
                _scheduler = Scheduler.find_by_scheduler_id(session, job.id)
                info = {
                    "request_url": res_url,
                    "trigger": trigger,
                    "action": job_name,
                    "args": json.dumps(func_args),  # json 序列化后的参数
                    "mold": schedule_type,
                    "type": schedule_type,  # sys
                    "next_run_time": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "user_id": user_id,
                    "scheduler_id": job.id,
                    "extra": json.dumps(schedule_args),  # 不同的trigger的不同参数
                    "remark": remark,
                    "status": ACTIVE
                }
                if not _scheduler:
                    Scheduler.create(session, **info)
                else:
                    _scheduler.update(session, **info)
            mess = "job_id为%s的任务添加成功" % job_id
            logger.info(mess)
            return {"status": 1, "message": mess}
        except ConflictingIdError:
            mess = "job_id为%s的任务已经存在" % job_id
            logger.error(mess)
            return {"status": 0, "message": mess}
        except Exception, e:
            logger.error(traceback.format_exc(e))
            return {"status": 0, "message": "添加任务失败"}

    def add_job_to_scheduler(self, trigger, job_id, job_name, schedule_args, callback_args, job_store):
        job = self.scheduler.add_job(
            CALLBACK_FUNC, trigger, id=job_id,
            name=job_name, jobstore=job_store,
            args=callback_args,
            timezone=TIMEZONE,
            **schedule_args
        )
        return job

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)
        with sessionCM() as session:
            job_record = Scheduler.find_by_scheduler_id(session, job_id)
            if job_record:
                job_record.status = CANCELLED
                session.add(job_record)
                session.commit()

    def start(self):
        self.scheduler.start()


my_scheduler = MyScheduler()
