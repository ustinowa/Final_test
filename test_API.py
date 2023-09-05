import logging

from conftest import browser
from testpage import OperationsHelper


def test_step1():
    logging.info("Test1 API run")
    testpage = OperationsHelper(browser)
    assert testpage.auth_site()[2] == testpage.check_auth(), "Test1 API failed"


def test_step2():
    logging.info("Test2 API run")
    testpage = OperationsHelper(browser)
    assert testpage.create_post() == "my_description", "Test2 API failed"
