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

CANCELLED = "999"
ACTIVE = "100"
RUNNING = "150"
ERROR = "200"
END = "300"


class Scheduler(Base):

    __tablename__ = "scheduler"

    id = SA.Column(SA.INTEGER, autoincrement=True, primary_key=True)
    request_url = SA.Column(SA.String(256), nullable=False, default="")
    trigger = SA.Column(SA.String(8))  # cron 定时 interval 间隔 date 定时(一次)
    action = SA.Column(SA.String(32)) # job 名字
    args = SA.Column(SA.String(1024), default="")  # json 序列化后的参数
    mold = SA.Column(SA.String(32), nullable=False, default="myweb")  # 默认
    type = SA.Column(SA.String(16), nullable=False, default="")  # sys
    status = SA.Column(SA.String(8), nullable=False, default=ACTIVE)
    next_run_time = SA.Column(SA.DATETIME, nullable=False, default="")
    user_id = SA.Column(SA.INTEGER, default=0)
    scheduler_id = SA.Column(SA.String(124), default=0)
    extra = SA.Column(SA.String(512), nullable=False, default="")  # 不同的trigger的不同参数
    err_mess = SA.Column(SA.String(1024), default="")
    remark = SA.Column(SA.String(1024), default="")

    def update(self, session, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        session.add(self)
        session.commit()

    @classmethod
    def find_by_scheduler_id(cls, session, scheduler_id):
        return session.query(cls).filter(cls.scheduler_id == scheduler_id).first()


