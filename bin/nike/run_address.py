#!/usr/bin/python
# coding:utf-8

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@Baidu.com.xxxxxx
===========================================
"""
import random
import time
import os
import sys
import json
import multiprocessing

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/../.." % cur_dir)
from lib.get_config import get_parames
from src.nike import Nike
from lib.util import read_file
from lib.util import write_file
from lib.util import mkdir_log
from lib.util import result_to_file


def target(username, password, parames):
    url = random.choice(json.loads(parames.get("url").get("product")))
    url_setting = parames.get("url").get("setting")
    lastname = unicode(parames.get("address").get("lastname"),encoding="utf8")
    firstname = unicode(parames.get("address").get("firstname"),encoding="utf8")
    province = unicode(parames.get("address").get("province"),encoding="utf8")
    city = unicode(parames.get("address").get("city"),encoding="utf8")
    district = unicode(parames.get("address").get("district"),encoding="utf8")
    addressinfo = unicode(parames.get("address").get("addressinfo"),encoding="utf8")
    phone = unicode(parames.get("address").get("phone"),encoding="utf8")
    browser_type = parames.get("browser").get("browser_type")
    headless = eval(parames.get("browser").get("headless"))
    timeout = parames.get("browser").get("timeout")
    log = parames.get("data").get("log")
    proxies = None
    nike = Nike(browser_type=browser_type, headless=headless, username=username, password=password,
                timeout=timeout, proxies=proxies)
    result = nike.login(url=url)
    if result.get("status", -1) == 1:
        result = nike.address(url=url_setting, lastname=lastname, firstname=firstname,
                              province=province,
                              city=city, district=district, phone=phone, addressinfo=addressinfo)
    result_to_file(result, log, data_type="address")
    nike.close()


def run(conf):
    parames = get_parames(conf)
    user_file = parames.get("user").get("address", "")
    work_num = parames.get("master").get("work_num", "2")
    if not user_file:
        raise Exception("Please give a user file")
    user_list = read_file(user_file)
    if not user_list:
        raise Exception("User file no data")
    pool = multiprocessing.Pool(int(work_num))
    for one in user_list:
        username = json.loads(one).get("response").get("username")
        password = json.loads(one).get("response").get("password")
        pool.apply_async(target, args=(username, password, parames))
    pool.close()
    pool.join()


if __name__ == '__main__':
    run("./conf/nike_conf.txt")
