# -*- coding: utf-8 -*-
"""结算完成页面。"""
from playwright.sync_api import expect

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    """订单完成页（/checkout-complete.html）。"""

    # ---------- 元素定位 ----------
    COMPLETE_HEADER = '[data-test="complete-header"]'
    COMPLETE_TEXT = '[data-test="complete-text"]'
    BACK_HOME_BUTTON = '[data-test="back-to-products"]'

    # ---------- 元素操作 ----------
    def click_back_home(self) -> "InventoryPage":
        """点击 Back Home 返回商品库存页。"""
        self.page.locator(self.BACK_HOME_BUTTON).click()
        from pages.inventory_page import InventoryPage

        return InventoryPage(self.page)

    # ---------- 页面断言 ----------
    def expect_order_complete(self) -> None:
        """断言下单成功，出现感谢文案。"""
        expect(self.page).to_have_url(f"{self.BASE_URL}checkout-complete.html")
        expect(self.page.locator(self.COMPLETE_HEADER)).to_have_text("Thank you for your order!")
        expect(self.page.locator(self.COMPLETE_TEXT)).to_contain_text("Your order has been dispatched")
