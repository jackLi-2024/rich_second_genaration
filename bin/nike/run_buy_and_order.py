#!/usr/bin/python
# coding:utf-8

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@Baidu.com.xxxxxx
===========================================
"""
import logging
import random
import time
import os
import sys
import json
import multiprocessing
from run_buy import target as buy_target
from run_order import target as order_target

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/../.." % cur_dir)
from lib.get_config import get_parames
from src.nike import Nike
from lib.util import read_file
from lib.util import write_file
from lib.util import mkdir_log
from lib.util import result_to_file
from lib.proxy import get_proxy
import multiprocessing


class QueueProcess(multiprocessing.Process):
    def __init__(self, record_queue=multiprocessing.Queue(), record_list=list(), parames=None,
                 group=None, name=None, args=None,
                 kwargs=None):
        self.args = args if args else ()
        kwargs = kwargs if kwargs else {}
        self.record_queue = record_queue
        self.record_list = record_list
        self.parames = parames
        super(QueueProcess, self).__init__(group=group, name=name, args=(), kwargs=kwargs)

    def run(self):
        self.run_()

    def run_(self):
        while True:
            new_record = None
            if self.record_list:
                one_record = self.record_list[0]
                if int(one_record.get("timestamp", "0")) < time.time():
                    new_record = self.record_list.pop(0)
                    username = new_record.get("response").get("username")
                    password = new_record.get("response").get("password")
                    order_target(username=username, password=password, parames=self.parames)
            if not new_record:
                try:
                    new_record = self.record_queue.get(timeout=2)
                    username = json.loads(new_record).get("response").get("username")
                    password = json.loads(new_record).get("response").get("password")
                    result = buy_target(username=username, password=password, parames=self.parames)
                    result["timestamp"] = time.time() + int(self.parames.get("interval").get(
                        "buy_and_order"))
                    if result.get("status", -1) == 1:
                        self.record_list.append(result)
                except Exception as e:
                    logging.exception(str(e))
                    new_record = None


def run(conf):
    parames = get_parames(conf)
    user_file = parames.get("user").get("buy", "")
    work_num = parames.get("master").get("work_num", "2")
    if not user_file:
        raise Exception("Please give a user file")
    user_list = read_file(user_file)
    if not user_list:
        raise Exception("User file no data")
    queue = multiprocessing.Queue()
    record_list = multiprocessing.Manager().list()
    process_pool = []
    for i in range(int(work_num)):
        p = QueueProcess(record_queue=queue, record_list=record_list, parames=parames)
        p.start()
        process_pool.append(p)
    for one in user_list:
        queue.put(one)
    for j in process_pool:
        j.join()


if __name__ == '__main__':
    run("./conf/nike_conf.txt")

