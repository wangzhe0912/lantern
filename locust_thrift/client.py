# -*- coding: utf-8 -*-

import time
from locust import events
from thriftpy.rpc import make_client


class RpcClient(object):
    """
    # 自定义的支持Thrift协议的Client
    """
    def __init__(self, service, host, port, proto_factory=None, trans_factory=None):
        if not proto_factory:
            from thriftpy.protocol import TBinaryProtocolFactory
            proto_factory_value = TBinaryProtocolFactory()
        else:
            proto_factory_value = proto_factory

        if not trans_factory:
            from thriftpy.transport import TBufferedTransportFactory
            trans_factory_value = TBufferedTransportFactory()
        else:
            trans_factory_value = trans_factory
        self.client = make_client(
            service, host, port,
            proto_factory=proto_factory_value,
            trans_factory=trans_factory_value
        )

    def __getattr__(self, rpc_method):
        func = self.client.__getattr__(rpc_method)

        def wrapper(*args, **kwargs):
            result = None
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
            except Exception, e:
                end_time = time.time()
                total_time = int((end_time - start_time) * 1000)
                events.request_failure.fire(request_type="RpcClient",
                                            name=rpc_method,
                                            response_time=total_time,
                                            exception=e)
            else:
                end_time = time.time()
                total_time = int((end_time - start_time) * 1000)
                events.request_success.fire(request_type="RpcClient",
                                            name=rpc_method,
                                            response_time=total_time,
                                            response_length=0)
            return result
        return wrapper
