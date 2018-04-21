#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:02
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""

import os.path
import traceback

import sys
from tornado import ioloop, web, options, httpserver

from config import settings
from lib.utils.logger_utils import logger
from schedules.my_scheduler import my_scheduler
from schedules.sys_schedules import sys_schedules
from views.webhook import WebHookHandler

options.define('port', default=8080, type=int)

SETTINGS = dict(
    template_path=os.path.join(os.path.dirname(sys.argv[0]), "templates"),
    static_path=os.path.join(os.path.dirname(sys.argv[0]), "static"),
    login_url="/signin",
    cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    websocket_ping_interval=20
)

session_settings = dict(
    driver="redis",
    driver_settings=dict(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_password,
        max_connections=settings.redis_max_connections
    ),
    cookie_config=dict(
        expires_days=30,
    )
)
urls = [
    (r'/webhook', WebHookHandler),
]


def main():
    try:
        options.parse_command_line()
        port = options.options.port
        settings.configure('PORT', port)
        SETTINGS.update(session=session_settings)
        app = web.Application(handlers=urls, debug=True, **SETTINGS)
        server = httpserver.HTTPServer(app)
        server.listen(settings.port)
        print "the server is going to start..."
        print "http://localhost:%s/" % options.options.port
        my_scheduler.start()
        for sched in sys_schedules:
            my_scheduler.add_my_job(*sched)
        ioloop.IOLoop().instance().start()
    except Exception, e:
        print traceback.format_exc(e)
        logger.error(traceback.format_exc(e))


if __name__ == "__main__":
    main()
