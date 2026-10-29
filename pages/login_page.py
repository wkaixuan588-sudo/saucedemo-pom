# -*- coding: utf-8 -*-
"""登录页面对象。"""
from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    """saucedemo 登录页（https://www.saucedemo.com/）。"""

    # ---------- 元素定位（页面层，全部使用已验证的 data-test 选择器） ----------
    USERNAME_INPUT = '[data-test="username"]'
    PASSWORD_INPUT = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'

    # ---------- 元素操作 ----------
    def fill_username(self, username: str) -> "LoginPage":
        self.page.locator(self.USERNAME_INPUT).fill(username)
        return self

    def fill_password(self, password: str) -> "LoginPage":
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        return self

    def click_login(self) -> None:
        self.page.locator(self.LOGIN_BUTTON).click()

    # ---------- 组合操作 ----------
    def login(self, username: str, password: str) -> None:
        """输入账号密码并点击登录。"""
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    # ---------- 页面断言 ----------
    def expect_login_success(self) -> None:
        """断言登录成功：跳转到商品库存页。"""
        expect(self.page).to_have_url(f"{self.BASE_URL}inventory.html")

    def expect_error_visible(self, contains: str | None = None) -> None:
        """断言登录失败并出现错误提示。"""
        error = self.page.locator(self.ERROR_MESSAGE)
        expect(error).to_be_visible()
        if contains:
            expect(error).to_contain_text(contains)
