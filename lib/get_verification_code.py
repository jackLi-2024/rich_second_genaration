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
import requests


def get_code(phone):
    url = "http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=01356636748d53f500c8ffa87bf165398c2f8e877201&itemid=723&mobile=" + phone + "&release=1"
    response = requests.get(url).text
    if response == "3001":
        return "1"  # 继续等待
    elif '|' in response:
        return response[-6:]  # 返回验证码
    else:
        return "0"  # 错误代码
