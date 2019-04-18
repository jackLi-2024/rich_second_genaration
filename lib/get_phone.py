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


def get_phone():
    url = "http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=01356636748d53f500c8ffa87bf165398c2f8e877201&itemid=723&excludeno=165"
    phone = requests.get(url).text.split('|')[1]
    return phone
