# -*- coding: utf-8 -*-
"""结算第一步：填写收货信息页面。"""
from playwright.sync_api import expect

from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    """结算信息页（/checkout-step-one.html）。"""

    # ---------- 元素定位 ----------
    FIRST_NAME_INPUT = '[data-test="firstName"]'
    LAST_NAME_INPUT = '[data-test="lastName"]'
    POSTAL_CODE_INPUT = '[data-test="postalCode"]'
    CONTINUE_BUTTON = '[data-test="continue"]'
    ERROR_MESSAGE = '[data-test="error"]'

    # ---------- 元素操作 ----------
    def fill_first_name(self, first_name: str) -> "CheckoutInfoPage":
        self.page.locator(self.FIRST_NAME_INPUT).fill(first_name)
        return self

    def fill_last_name(self, last_name: str) -> "CheckoutInfoPage":
        self.page.locator(self.LAST_NAME_INPUT).fill(last_name)
        return self

    def fill_postal_code(self, postal_code: str) -> "CheckoutInfoPage":
        self.page.locator(self.POSTAL_CODE_INPUT).fill(postal_code)
        return self

    # ---------- 组合操作 ----------
    def fill_info_and_continue(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutOverviewPage":
        """填写收货信息并点击 Continue，进入结算总览页。"""
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_postal_code(postal_code)
        self.page.locator(self.CONTINUE_BUTTON).click()
        from pages.checkout_overview_page import CheckoutOverviewPage

        return CheckoutOverviewPage(self.page)

    # ---------- 页面断言 ----------
    def expect_page(self) -> None:
        expect(self.page).to_have_url(f"{self.BASE_URL}checkout-step-one.html")

    def expect_error_visible(self, contains: str | None = None) -> None:
        """断言必填校验失败并出现错误提示。"""
        error = self.page.locator(self.ERROR_MESSAGE)
        expect(error).to_be_visible()
        if contains:
            expect(error).to_contain_text(contains)
