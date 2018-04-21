#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/15 0015 上午 11:00
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import requests

from lib.sql.scheduler import Scheduler, ACTIVE, ERROR, END
from lib.sql.session import sessionCM
from lib.utils.logger_utils import logger
from schedules import scheduler


def aps_callback(req_type, url, data, job_id, other_kwargs=None, retry=1):
    """
    scheduler回调函数
    TODO: 添加调用记录
    :param req_type: 请求方式 post|get
    :param url: 请求地址
    :param data: 请求数据
    :param job_id: 在任务队列中的id
    :param other_kwargs: 其他
    :param retry: 重试次数
    :return:
    """
    with sessionCM() as session:
        sched = Scheduler.find_by_scheduler_id(session, job_id)
        job = scheduler.get_job(job_id)
        next_run_time = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
        logger.info("正在执行scheduler回调, 第%s次s请求:" % retry)
        logger.info(url)
        logger.info(data)
        try:
            if req_type == "post":
                res = requests.post(url=url, data=data)
            else:
                res = requests.get(url=url, params=data)
            res = res.json()
            if res["status"]:
                sched.update(session,
                             **{"status": ACTIVE if sched.trigger != "date" else END, "next_run_time": next_run_time})
            else:
                sched.update(session,
                             **{"status": ERROR, "err_mess": res["message"], "next_run_time": next_run_time})
            return res
        except Exception, e:
            if retry < 3:
                return aps_callback(req_type, url, data, job_id, other_kwargs=other_kwargs, retry=retry + 1)
            else:
                logger.info("POST fail {0}".format(e.message))
                sched.update(session, **{"status": ERROR, "err_mess": "POST fail {0}".format(e.message),
                                         "next_run_time": next_run_time})
                return {"status": 0, "mess": e.message}
