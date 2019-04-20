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
import logging
from SpiderTool import Browser
from loggingtool import loggingtool
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/.." % cur_dir)

from lib.util import error_result
from lib.util import normal_result
from lib.get_phone import get_phone
from lib.get_verification_code import get_code


class Nike(object):
    def __init__(self, proxies=None, headless=True,
                 timeout=20, executable_path=None,
                 browser_type=None, username=None, password=None):
        headless = bool(headless)
        timeout = int(timeout)
        self.username = username
        self.password = password
        if executable_path == "None":
            executable_path = None
        self.browser = Browser.Browser(proxies=proxies, headless=headless, timeout=timeout,
                                       executable_path=executable_path,
                                       browser_type=browser_type)
        self.browser.browser.set_window_size(1366, 768)

    def close(self):
        self.browser.close()

    def login(self, url=None):
        try:
            # https://www.nike.com/cn/launch/t/air-max-95-premium-throwback-future/

            self.browser.get(url=url)
            self.browser.wait_for_element_loaded(type_name="join-log-in", elem_type=By.CLASS_NAME)
            join_in_elem = self.browser.find_element("join-log-in", By.CLASS_NAME)
            self.browser.click_elem(join_in_elem)

            self.browser.wait_for_element_loaded(type_name="verifyMobileNumber",
                                                 elem_type=By.NAME)
            user = self.browser.find_element("verifyMobileNumber", By.NAME)
            pwd = self.browser.find_element("password", By.NAME)
            self.browser.send_keys(user, self.username)
            self.browser.send_keys(pwd, self.password)

            submit = self.browser.find_element("mobileLoginSubmit", By.CLASS_NAME)
            self.browser.click_elem(submit)
            try:
                self.browser.wait_for_element_loaded(type_name="test-profile-picture",
                                                     elem_type=By.CLASS_NAME)
            except:
                self.browser.wait_for_element_loaded(type_name="//input[@type='email']",
                                                     elem_type=By.XPATH)
                email_ = self.browser.find_element("//input[@type='email']", By.XPATH)
                save_ = self.browser.find_element("//input[@value='保存']", By.XPATH)
                self.browser.clear(email_)
                self.browser.send_keys(email_, "%s@qq.com" % self.username)
                self.browser.click_elem(save_)

            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "login successfully"}
            return normal_result(result)
        except Exception as e:
            logging.exception(str(e))
            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "login defeatly", "error": str(e)}
            return error_result(result)

    def buy(self, url=None, size=list(), wait_time=10):
        try:
            # self.browser.get(url)
            # time.sleep(5)
            self.browser.wait_for_element_loaded("cta-btn", By.CLASS_NAME, wait_time=wait_time)
            self.browser.wait_for_element_loaded("size-grid-button", By.CLASS_NAME,
                                                 wait_time=wait_time)
            sizeEU = self.browser.find_elements("size-grid-button", By.CLASS_NAME)
            # todo:这里需要修改，需要实时验证，把sleep去掉
            hassize = False
            sizenum = ""
            for one in sizeEU:
                try:
                    time.sleep(0.1)
                    ActionChains(self.browser.browser).move_to_element(one).perform()
                    if one.text in size:
                        sizenum = one.text
                        self.browser.click_elem(one)
                        hassize = True
                        break
                except:
                    logging.info("size error")
            if not hassize:
                result = {"username": self.username, "password": self.password, "url": url,
                          "msg": "No size for the shoe", "error": ""}
                return error_result(result)
            # save_button = browser.find_elements_by_class_name("save-button")[0]
            save_button = self.browser.find_elements("cta-btn", By.CLASS_NAME)[0]
            ActionChains(self.browser.browser).move_to_element(save_button).perform()
            # 得到鞋码数
            save_button.click()
            self.browser.wait_for_element_loaded("cta-btn", By.CLASS_NAME)
            # 获取配送地址
            addr = self.browser.find_elements("open-close", By.CLASS_NAME)[1]
            self.browser.wait_for_element_loaded("payment-provider-btn", By.CLASS_NAME,
                                                 wait_time=wait_time)
            alipay = self.browser.find_elements("payment-provider-btn", By.CLASS_NAME)[1]
            # 确定支付方式为支付宝
            alipay.click()
            self.browser.wait_for_element_loaded("save-button", By.CLASS_NAME, wait_time=wait_time)
            save_button = self.browser.find_elements("save-button", By.CLASS_NAME)[1]
            time.sleep(2)
            save_button.click()
            time.sleep(1)

            self.browser.wait_for_element_loaded("save-button", By.CLASS_NAME, wait_time=wait_time)
            save_button = self.browser.find_elements("save-button", By.CLASS_NAME)[2]
            print save_button.text
            # 提交订单并排队
            save_button.click()
            time.sleep(10)
            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "wait in line", "sizenum": sizenum}
            return normal_result(result)
        except Exception as e:
            logging.exception(str(e))
            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "buy defeatly", "error": str(e)}
            return error_result(result)

    def order(self, url, wait_time=10):
        try:
            self.browser.get(url=url)
            self.browser.wait_for_element_loaded("product-base", By.CLASS_NAME,
                                                 wait_time=int(wait_time) * 1.5)
            products = self.browser.find_elements("product-base", By.CLASS_NAME)
            order_info = ""
            for one in products:
                content = one.text
                if content:
                    order_info += "[%s] " % content
            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "order info", "order_info": order_info}
            return normal_result(result)
        except Exception as e:
            logging.exception(str(e))
            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "order info", "error": str(e)}
            return error_result(result)

    def address(self, url, lastname=None, firstname=None, province=None, city=None, district=None,
                phone=None, addressinfo=None, wait_time=10):
        wait_time = int(wait_time)
        isprovince = False
        iscity = False
        isdistrict = False
        try:
            self.browser.get(url=url)
            # 这里时间较长，特殊处理
            try:
                self.browser.wait_for_element_loaded("edit-button-container", By.CLASS_NAME,
                                                     wait_time=int(wait_time) * 1.5)
            except:
                self.browser.wait_for_element_loaded("add-button", By.CLASS_NAME,
                                                     wait_time=int(wait_time) * 1.5)
            self.browser.wait_for_element_loaded("addresses", By.CLASS_NAME, wait_time=wait_time)
            address = self.browser.find_element("addresses", By.CLASS_NAME)
            ActionChains(self.browser.browser).move_to_element(address).perform()
            self.browser.click_elem(address)
            time.sleep(1)

            try:
                self.browser.wait_for_element_loaded("edit-button-container", By.CLASS_NAME,
                                                     wait_time=wait_time)
                edit = self.browser.find_element("edit-button-container", By.CLASS_NAME)
                ActionChains(self.browser.browser).move_to_element(edit).perform()
                self.browser.click_elem(edit)
            except:
                self.browser.wait_for_element_loaded("add-button", By.CLASS_NAME,
                                                     wait_time=wait_time)
                add_address = self.browser.find_elements("add-button", By.CLASS_NAME)[2]
                ActionChains(self.browser.browser).move_to_element(add_address).perform()
                self.browser.click_elem(add_address)

            # todo:这里有可能需要加入等待元素加载
            time.sleep(0.5)
            self.browser.wait_for_element_loaded("address-lastname", By.ID)
            self.browser.wait_for_element_loaded("address-firstname", By.ID)
            lastname_elem = self.browser.find_element("address-lastname", By.ID)
            firstname_elem = self.browser.find_element("address-firstname", By.ID)
            self.browser.clear(lastname_elem)
            time.sleep(0.1)
            self.browser.clear(firstname_elem)
            time.sleep(0.1)
            self.browser.send_keys(lastname_elem, lastname)
            time.sleep(0.1)
            self.browser.send_keys(firstname_elem, firstname)
            time.sleep(0.5)
            self.browser.wait_for_element_loaded("state-container", By.CLASS_NAME,
                                                 wait_time=wait_time)
            self.browser.wait_for_element_loaded("city-container", By.CLASS_NAME,
                                                 wait_time=wait_time)
            self.browser.wait_for_element_loaded("district-container", By.CLASS_NAME,
                                                 wait_time=wait_time)

            time.sleep(0.5)
            state = self.browser.find_element("state-container", By.CLASS_NAME)
            ActionChains(self.browser.browser).move_to_element(state).perform()
            self.browser.click_elem(state)

            state_province = self.browser.find_elements(
                "//div[@class='input-wrapper state-container container2 js-addressState']/div/ul/li",
                By.XPATH)

            for one in state_province:
                if one.text == province:
                    ActionChains(self.browser.browser).move_to_element(one).perform()
                    self.browser.click_elem(one)
                    isprovince = True
                    break
            time.sleep(0.5)
            city_ = self.browser.find_element("city-container", By.CLASS_NAME)
            ActionChains(self.browser.browser).move_to_element(city_).perform()
            self.browser.click_elem(city_)
            state_city = self.browser.find_elements(
                "//div[@class='input-wrapper city-container container1 js-addressCity']/div/ul/li",
                By.XPATH)
            for one in state_city:
                if one.text == city:
                    ActionChains(self.browser.browser).move_to_element(one).perform()
                    self.browser.click_elem(one)
                    iscity = True
                    break
            time.sleep(0.5)
            district_ = self.browser.find_element("district-container", By.CLASS_NAME)
            ActionChains(self.browser.browser).move_to_element(district_).perform()
            self.browser.click_elem(district_)
            state_district = self.browser.find_elements(
                "//div[@class='input-wrapper district-container container2 js-addressDistrict']/div/ul/li",
                By.XPATH)
            for one in state_district:
                if one.text == district:
                    ActionChains(self.browser.browser).move_to_element(one).perform()
                    self.browser.click_elem(one)
                    isdistrict = True
                    break
            if not all([state_province, state_city, state_district]):
                result = {"username": self.username, "password": self.password, "url": url,
                          "msg": "address defeatly",
                          "error": "Cant load  province or city or county"}
                return error_result(result)
            elif not all([isprovince, iscity, isdistrict]):
                result = {"username": self.username, "password": self.password, "url": url,
                          "msg": "address defeatly",
                          "error": "Cant get province or city or county"}
                return error_result(result)
            else:
                pass

            addressinfo_ = self.browser.find_element("address-addressone", By.ID)
            self.browser.clear(addressinfo_)
            self.browser.send_keys(addressinfo_, addressinfo)

            phone_ = self.browser.find_element("address-phonenumber", By.ID)
            self.browser.clear(phone_)
            self.browser.send_keys(phone_, phone)

            save_button = self.browser.find_element(
                "//button[@data-qa='my_account.settings.addresses.shipping_address.save_button']",
                By.XPATH)
            ActionChains(self.browser.browser).move_to_element(save_button).perform()
            self.browser.click_elem(save_button)
            self.browser.wait_for_element_loaded("edit-button-container", By.CLASS_NAME,
                                                 wait_time=int(wait_time) * 1.5)
            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "address successfully"}
            return normal_result(result)
        except Exception as e:
            logging.exception(str(e))
            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "address defeatly", "error": str(e)}
            return error_result(result)

    def regist(self, url, firstname="Lee", lastname="Jack", wait_time=10):
        try:
            self.browser.get(url=url)
            self.browser.wait_for_element_loaded(type_name="join-log-in", elem_type=By.CLASS_NAME)
            join_in_elem = self.browser.find_element("join-log-in", By.CLASS_NAME)
            self.browser.click_elem(join_in_elem)

            self.browser.wait_for_element_loaded(type_name="mobileLoginJoinLink",
                                                 elem_type=By.CLASS_NAME)
            register_div_elem = self.browser.find_element("mobileLoginJoinLink", By.CLASS_NAME)
            register_a_elem = register_div_elem.find_element_by_xpath(".//a")
            self.browser.click_elem(register_a_elem)
            phone_number_elem = self.browser.find_element("phoneNumber", By.CLASS_NAME)
            send_code_elem = self.browser.find_element("sendCodeButton", By.CLASS_NAME)
            code_elem = self.browser.find_element("//input[@class='code']", By.XPATH)
            self.browser.send_keys(phone_number_elem, self.username)
            time.sleep(1)
            self.browser.click_elem(send_code_elem)
            # 等待验证码
            ticks = 0
            code = "1"
            while code == "1":
                code = get_code(self.username)
                if code == "1":
                    time.sleep(5)
                    ticks += 5
                elif code == "0":
                    result = {"username": self.username, "password": self.password, "url": url,
                              "msg": "regist defeatly", "error": "Verification-code Error"}
                    return error_result(result)

                if ticks >= 60:
                    result = {"username": self.username, "password": self.password, "url": url,
                              "msg": "regist defeatly", "error": "Verification-code Timeout"}
                    return error_result(result)
            self.browser.send_keys(code_elem, code)
            join_continue_elem = self.browser.find_element("mobileJoinContinue ", By.CLASS_NAME)
            time.sleep(2)
            self.browser.click_elem(join_continue_elem)
            time.sleep(2)
            # 填写信息
            self.browser.wait_for_element_loaded("mobileJoinSubmit", elem_type=By.CLASS_NAME,
                                                 wait_time=wait_time)
            lastName_elem = self.browser.find_element("lastName", By.NAME)
            firstName_elem = self.browser.find_element("firstName", By.NAME)
            password_elem = self.browser.find_element("password", By.NAME)
            gender_div_elem = self.browser.find_element("shoppingGender", By.CLASS_NAME)
            man_elem = gender_div_elem.find_element_by_xpath(".//input[@type='button']")
            # ?mobileJoinSubmit: firefox width out of range

            register_div_elem = self.browser.find_element("mobileJoinSubmit", By.CLASS_NAME)
            ActionChains(self.browser.browser).move_to_element(register_div_elem).perform()
            time.sleep(0.1)
            self.browser.send_keys(lastName_elem, lastname)
            time.sleep(0.1)
            self.browser.send_keys(firstName_elem, firstname)
            time.sleep(0.1)
            self.browser.send_keys(password_elem, self.password)
            time.sleep(0.1)
            self.browser.click_elem(man_elem)
            time.sleep(0.5)
            self.browser.click_elem(register_div_elem)

            time.sleep(5)
            # 填写邮件
            self.browser.wait_for_element_loaded("captureEmailSubmit", elem_type=By.CLASS_NAME)
            email_elem = self.browser.find_element("emailAddress", By.NAME)
            save_elem = self.browser.find_element("captureEmailSubmit", By.CLASS_NAME)
            self.browser.send_keys(email_elem, self.username + "@qq.com")
            self.browser.click_elem(save_elem)
            time.sleep(1)
            # 验证邮件
            self.browser.wait_for_element_loaded("mobileJoinDobEmailSkipButton",
                                                 elem_type=By.CLASS_NAME)
            skip_elem = self.browser.find_element("mobileJoinDobEmailSkipButton", By.CLASS_NAME)
            self.browser.click_elem(skip_elem)

            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "regist successfully"}
            return normal_result(result)
        except Exception as e:
            logging.exception(str(e))
            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "regist defeatly", "error": str(e)}
            return error_result(result)


def test_login():
    url = "https://www.nike.com/cn/launch/t/react-element-87-volt-racer-pink-aurora/"
    username = "17042071241"
    password = "Zx651324959"
    # executable_path = "http://167.179.97.68:4444/wd/hub"
    executable_path = "None"
    nike = Nike(browser_type="Chrome", headless=False, username=username, password=password,
                timeout=20, executable_path=executable_path)
    login_result = nike.login(url=url)
    print(login_result)
    nike.close()


def test_buy():
    url = "https://www.nike.com/cn/launch/t/react-element-87-volt-racer-pink-aurora/"
    username = "13691926738"
    password = "Ljc19941108"
    # executable_path = "http://167.179.97.68:4444/wd/hub"
    executable_path = "None"
    nike = Nike(browser_type="Chrome", headless=False, username=username, password=password,
                timeout=20, executable_path=executable_path)
    login_result = nike.login(url=url)
    if login_result.get("status", -1) == 1:
        print(nike.buy(url=url, size=["39"], wait_time=10))
    else:
        print(login_result)
    nike.close()


def test_address():
    url = "https://www.nike.com/cn/launch/t/react-element-87-volt-racer-pink-aurora/"
    username = "13691926738"
    password = "Ljc19941108"
    url_setting = "https://www.nike.com/cn/zh_cn/p/settings?tab=addresses"
    lastname = "jiacai"
    firstname = "li"
    province = u"黑龙江省"
    city = u"绥化市"
    district = u"安达市"
    # 注意这里要使用unicode
    addressinfo = u"详细地址"
    phone = username
    # executable_path = "http://167.179.97.68:4444/wd/hub"
    executable_path = "None"
    nike = Nike(browser_type="Chrome", headless=False, username=username, password=password,
                timeout=20, executable_path=executable_path)
    login_result = nike.login(url=url)
    if login_result.get("status", -1) == 1:

        print(nike.address(url=url_setting, lastname=lastname, firstname=firstname,
                           province=province,
                           city=city, district=district, phone=phone, addressinfo=addressinfo))
    else:
        print(login_result)
    nike.close()


def test_order():
    url = "https://www.nike.com/cn/launch/t/react-element-87-volt-racer-pink-aurora/"
    url_order = "https://www.nike.com/cn/member/inbox"
    username = "18404983790"
    password = "Ljc19941108"
    # executable_path = "http://167.179.97.68:4444/wd/hub"
    executable_path = "None"
    nike = Nike(browser_type="Chrome", headless=False, username=username, password=password,
                timeout=20, executable_path=executable_path)
    login_result = nike.login(url=url)
    if login_result.get("status", -1) == 1:
        print(json.dumps(nike.order(url=url_order), ensure_ascii=False).encode("utf8"))
    else:
        print(login_result)
    nike.close()


def test_regist():
    url = "https://www.nike.com/cn/launch/t/air-max-95-premium-throwback-future/"
    username = get_phone()
    password = "Snkrs" + username
    # executable_path = "http://167.179.97.68:4444/wd/hub"
    executable_path = "None"
    nike = Nike(browser_type="Chrome", headless=False, username=username, password=password,
                timeout=20, executable_path=executable_path)
    print(nike.regist(url=url))


if __name__ == '__main__':
    test_address()
