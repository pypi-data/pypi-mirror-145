#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''                                                          
Copyright (C)2018 SenseDeal AI, Inc. All Rights Reserved                                                      
Author: xuwei                                        
Email: weix@sensedeal.ai                                 
Description:                                    
'''


import time
import grpc
import sense_core as sd
from sense_data import stock_pb2_grpc


def catch_except_log(func):
    def try_catch(*args, **kwargs):
        _num = 1
        while True:
            try:
                with grpc.insecure_channel(sd.config('data_rpc', 'host') + ":" + sd.config('data_rpc', 'port'),
                                           options=[('grpc.max_send_message_length', 30 * 1024 * 1024),
                                                    ('grpc.max_receive_message_length', 30 * 1024 * 1024)]) as channel:
                    _stub = stock_pb2_grpc.StockInfStub(channel)
                    r = func(*args, stub=_stub, **kwargs)
                    return r
            except Exception as e:
                #time.sleep(3)
                _num += 1
                if _num > 1:
                    sd.log_exception("%s: %s, args: %s, xargs: %s " %(func.__name__, e, str(args), str(kwargs)))
                    return None
    return try_catch
