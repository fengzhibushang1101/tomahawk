#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/21 0021 下午 9:49
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import traceback
import ujson as json
from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.concurrent import run_on_executor
from tornado.web import HTTPError

from lib.utils.logger_utils import logger
from schedules.my_scheduler import my_scheduler
from views.base import BaseHandler


class SchedulerHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)

    @gen.coroutine
    def get(self, *args, **kwargs):
        logger_dict = {"args": args, "kwargs": kwargs, "params": self.params, "method": "POST"}
        interface = args[0]
        method_settings = {
        }
        if interface not in method_settings:
            raise HTTPError(404)
        try:
            response = yield method_settings[interface]()
            self.write(response)
        except Exception, e:
            logger_dict["traceback"] = traceback.format_exc(e)
            logger.error(logger_dict)
            self.write({"status": 0, "message": "获取失败"})
        finally:
            self.finish()

    @gen.coroutine
    def post(self, *args, **kwargs):
        logger_dict = {"args": args, "kwargs": kwargs, "params": self.params, "method": "POST"}
        interface = args[0]
        method_settings = {
            "schedule": self.add_schedule
        }
        if interface not in method_settings:
            raise HTTPError(404)
        try:
            response = yield method_settings[interface]()
            self.write(response)
        except Exception, e:
            logger_dict["traceback"] = traceback.format_exc(e)
            logger.error(logger_dict)
            self.write({"status": 0, "message": "请求出错"})
        finally:
            self.finish()

    @gen.coroutine
    def delete(self, *args, **kwargs):
        logger_dict = {"args": args, "kwargs": kwargs, "params": self.params, "method": "POST"}
        interface = args[0]
        method_settings = {

        }
        if interface not in method_settings:
            raise HTTPError(404)
        try:
            response = yield method_settings[interface]()
            self.write(response)
        except Exception, e:
            logger_dict["traceback"] = traceback.format_exc(e)
            logger.error(logger_dict)
            self.write({"status": 0, "message": "获取失败"})
        finally:
            self.finish()

    @run_on_executor
    def add_schedule(self):
        data = self.params.get("data")
        data = json.loads(data)
        args = dict(
            trigger=data["trigger"],
            res_url=data["res_url"],
            res_type=data["res_type"],
            job_id=data.get("job_id"),
            job_name=data["job_name"],
            schedule_args=data["schedule_args"],
            schedule_type=data.get("schedule_type", "self"),
            func_args=data.get("func_args", {}),
            user_id=data.get("user_id", 0),
            remark=data.get("func_args", ""),
            job_store=data.get("job_store", "default")
        )
        return my_scheduler.add_my_job(**args)
