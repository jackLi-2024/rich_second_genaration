#!/usr/bin/python
# coding:utf-8

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@Baidu.com.xxxxxx
===========================================
"""

import os
import sys
import json
import time


def error_result(error_msg=None, error_code=-1):
    result = {
        "status": error_code,
        "response": error_msg
    }
    return result


def normal_result(data):
    result = {
        "status": 1,
        "response": data
    }
    return result


def write_file(filename="", data="", mode="a"):
    if type(data) != str:
        try:
            data = json.dumps(data, ensure_ascii=False).encode("utf8")
        except Exception as e:
            data = "No json data --> %s" % str(e)
    with open(filename, mode, 0) as f:
        f.write(data + "\n")
    return


def read_file(filename="", data="", mode="r"):
    with open(filename, mode) as f:
        lines = f.readlines()
    return lines


def mkdir_log(log):
    try:
        os.listdir(log)
    except:
        os.mkdir(log)


def result_to_file(result, log, data_type=""):
    today = time.strftime("%Y%m%d", time.gmtime(time.time()))
    mkdir_log("%s/%s" % (log, today))
    if result.get("status", "0") == 1:
        write_file("%s/%s/%s_success.txt" % (log, today, data_type), result)
        # with open("%s/%s/%s_success.txt" % (log, today, data_type),"a") as f:
        #     f.write(result + "\n")
    else:
        write_file("%s/%s/%s_defeat.txt" % (log, today, data_type), result)
        # with open("%s/%s/%s_defeat.txt" % (log, today, data_type),"a") as f:
        #     f.write(result + "\n")
