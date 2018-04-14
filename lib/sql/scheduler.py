#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/14 0014 下午 10:01
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import sqlalchemy as SA

from lib.sql.base import Base


class Scheduler(Base):
    __tablename__ = "scheduler"

    id = SA.Column(SA.INTEGER, autoincrement=True, primary_key=True)
    request_url = SA.Column(SA.String(256), nullable=False, default="")
    request_type = SA.Column(SA.String(8))  # cron 定时 interval 间隔 date 定时(一次)
    args = SA.Column(SA.String(1024), default="")
    mold = SA.Column(SA.String(32), nullable=False, default="")  #
    type = SA.Column(SA.String(16), nullable=False, default="")  # sys
    status = SA.Column(SA.String(8), nullable=False, default="")
    next_run_time = SA.Column(SA.String(32), nullable=False, default="")
    user_id = SA.Column(SA.INTEGER, default=0)
    scheduler_id = SA.Column(SA.INTEGER, default=0)
    err_mess = SA.Column(SA.String(1024), default="")
    remark = SA.Column(SA.String(1024), default="")

    def update(self, session, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        session.add(self)
        session.commit()





