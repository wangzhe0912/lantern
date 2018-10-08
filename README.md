## 项目说明
基于Locust和thriftpy扩展的用于thrift协议的压测工具。

Demo：启动server
    ``export PYTHONPATH=`pwd` ``
    ``python lantern/server.py``
    
Demo：启动压测脚本
    ``export PYTHONPATH=`pwd` ``
    ``locust -f lantern/tests/ping_pong.py``
