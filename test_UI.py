import time
import yaml
from testpage import OperationsHelper
import logging


with open("./testdata.yaml") as f:
    testdata = yaml.safe_load(f)

login = testdata["login"]
password = testdata["password"]


def test_step1(browser):
    logging.info("test1 running")
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    testpage.enter_login(login)
    testpage.enter_pass(password)
    testpage.click_login_button()
    assert testpage.auth() == f"Hello, {login}"


def test_step2(browser):
    logging.info("test2 running")
    testpage = OperationsHelper(browser)
    testpage.click_about_link()
    time.sleep(2)
    assert testpage.get_title_size() == "32px"


def test_step3(browser):
    logging.info("test3 running")
    testpage = OperationsHelper(browser)
    res = testpage.checkout("nikto -h http://test-stand.gb.ru/ -ssl -Tuning 4", "0 error(s)")
    assert res, "test2 FAIL"
