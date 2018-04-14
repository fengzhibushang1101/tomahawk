#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 0025 上午 9:45
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""

from lib.sql.base import metadata, db
from lib.sql.user import User


class CreateTables(object):

    @classmethod
    def create_tables(cls):
        metadata.create_all(db)


if __name__ == "__main__":
    CreateTables().create_tables()
