import json
import subprocess
import requests
from BaseApp import BasePage
from selenium.webdriver.common.by import By
import yaml


class TestSearchLocators:
    ids = dict()
    with open("./locators.yaml") as f:
        locators = yaml.safe_load(f)
    for locator in locators["xpath"].keys():
        ids[locator] = (By.XPATH, locators["xpath"][locator])
    for locator in locators["css"].keys():
        ids[locator] = (By.CSS_SELECTOR, locators["css"][locator])


class OperationsHelper(BasePage):
    with open("config.yaml", "r") as f:
        d = yaml.safe_load(f)

    #ENTER TEXT
    def enter_login(self, word):
        self.enter_text_into_field(TestSearchLocators.ids["LOCATOR_LOGIN_FIELD"], word, description="login form")

    def enter_pass(self, word):
        self.enter_text_into_field(TestSearchLocators.ids["LOCATOR_PASS_FIELD"], word, description="password form")

    def auth(self):
        return self.find_element(TestSearchLocators.ids["LOCATOR_AUTH"]).text

    #CLICK
    def click_login_button(self):
        self.click_button(TestSearchLocators.ids["LOCATOR_LOGIN_BTN"], description="login")

    def click_about_link(self):
        self.click_button(TestSearchLocators.ids["LOCATOR_ABOUT_BTN"], description="contact")

    #GET TEXT
    def get_user_text(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_HELLO"], description="username")

    def get_title_size(self):
        return self.get_element_property(TestSearchLocators.ids["LOCATOR_ABOUT_TITLE"], property="font-size")

    #API
    def auth_site(self):
        data = {
            "username": self.d["username"],
            "password": self.d["password"]
        }
        res = requests.post(url=self.d["url_auth"], data=json.dumps(data))
        return res.status_code, res.json()["token"], res.json()["username"]

    def create_post(self):
        headers = {
            "X-Auth-Token": self.auth_site()[1]
        }
        data = {
            "title": "my_title",
            "description": "my_description",
            "content": "my_content",
        }
        res = requests.post(url=self.d["url_create"], headers=headers, data=data)
        return res.json()["description"]

    def check_auth(self):
        headers = {
            "X-Auth-Token": self.auth_site()[1]
        }

        res = requests.get(url="https://test-stand.gb.ru/api/users/profile/7891", headers=headers)
        return res.json()["username"]

    def checkout(self, cmd, text):
        result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
        if text in result.stdout and result.returncode == 0 or text in result.stderr:
            return True
        else:
            return False


