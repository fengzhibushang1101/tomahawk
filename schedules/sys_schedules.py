#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/21 0021 下午 7:31
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""


sys_schedules = [
    ["cron", "get", "http://180.76.98.136/api/jx3/info", "get_jx3_info", "get_jx3_info", {"second": '*/5'}, 'sys', {}]
]