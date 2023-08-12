#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
import os

import mariadb

from .conf_test import conf


def is_skysql():
    return conf()["host"][-13:] == "db.skysql.net"


def is_maxscale():
    return os.environ.get('srv') in ["maxscale", 'skysql-ha']


def is_mysql():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("select version()")
    row = cursor.fetchone()
    mysql_server = 0 if "MARIADB" in row[0].upper() else 1
    del cursor, conn
    return mysql_server


def create_connection(additional_conf=None):
    default_conf = conf()
    if additional_conf is None:
        c = dict((default_conf.items()))
    else:
        c = dict(list(default_conf.items()) + list(additional_conf.items()))
    return mariadb.connect(**c)
