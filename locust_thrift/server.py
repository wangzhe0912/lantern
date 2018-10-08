# -*- coding: utf-8 -*-
"""
# 该文件仅仅是用于模拟待压测服务使用的。
# 正式压测过程中可以忽略该文件。
"""
import thriftpy
from thriftpy.rpc import make_server
import os
from locust_thrift.settings import ROOT_PATH


pingpong_thrift = thriftpy.load(os.path.join(ROOT_PATH, "thrift_file/pingpong.thrift"), module_name="pingpong_thrift")


class Dispatcher(object):
    def ping(self):
        return "pong"


server = make_server(pingpong_thrift.PingPong, Dispatcher(), '127.0.0.1', 6000)
server.serve()
