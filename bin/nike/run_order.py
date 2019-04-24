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
from lib.util import Email
from lib.proxy import get_proxy


def target(username, password, parames):
    email_smtpserver = parames.get("email").get("email_smtpserver")
    email_port = parames.get("email").get("email_port")
    email_sender = parames.get("email").get("email_sender")
    email_password = parames.get("email").get("email_password")
    email_receiver = json.loads(parames.get("email").get("email_receiver"))
    email_subject = parames.get("email").get("email_subject")

    url = random.choice(json.loads(parames.get("url").get("product")))
    url_order = parames.get("url").get("order")
    browser_type = parames.get("browser").get("browser_type")
    executable_path = parames.get("browser").get("executable_path")
    headless = eval(parames.get("browser").get("headless"))
    timeout = parames.get("browser").get("timeout")
    wait_time = int(parames.get("browser").get("wait_time","10"))
    log = parames.get("data").get("log")
    proxies = get_proxy()
    nike = Nike(browser_type=browser_type, headless=headless, username=username, password=password,
                timeout=timeout, proxies=proxies, executable_path=executable_path)
    result = nike.login(url=url)
    if result.get("status", -1) == 1:
        result = nike.order(url=url_order, wait_time=wait_time)
        if result.get("status", -1) == 1:
            email_ = Email(email_smtpserver, email_port, email_sender, email_password,
                           email_receiver,
                           email_subject)
            text = json.dumps(result, ensure_ascii=False).encode("utf8")
            email_.appendText(text)
            email_.sendEmail()

    result_to_file(result, log, data_type="order")
    nike.close()
    return result


def run(conf):
    parames = get_parames(conf)
    user_file = parames.get("user").get("order", "")
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
