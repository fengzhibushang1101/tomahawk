#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/21 0021 下午 7:31
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""

sys_schedules = [
    ["cron", "post", "http://www.kisu.top/api/jx3/info", "get_jx3_info", "get_jx3_info", {"hour": 3}, 'sys', {}],
    ["cron", "post", "http://monitor.kisu.top/api/all_monitor", "get_usage", "get_usage", {"minute": '*/1'}, 'sys', {}]
]
