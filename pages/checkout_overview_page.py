# -*- coding: utf-8 -*-
"""结算第二步：订单总览页面。"""
from playwright.sync_api import expect

from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    """结算总览页（/checkout-step-two.html）。"""

    # ---------- 元素定位 ----------
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    SUMMARY_SUBTOTAL = '[data-test="subtotal-label"]'
    SUMMARY_TAX = '[data-test="tax-label"]'
    SUMMARY_TOTAL = '[data-test="total-label"]'
    FINISH_BUTTON = '[data-test="finish"]'

    # ---------- 元素操作 ----------
    def click_finish(self) -> "CheckoutCompletePage":
        """点击 Finish 提交订单，进入完成页。"""
        self.page.locator(self.FINISH_BUTTON).click()
        from pages.checkout_complete_page import CheckoutCompletePage

        return CheckoutCompletePage(self.page)

    # ---------- 数据读取 ----------
    def item_names(self) -> list[str]:
        self._wait_items_ready(self.CART_ITEM, self.ITEM_NAME)
        return [e.inner_text() for e in self.page.locator(f"{self.CART_ITEM} {self.ITEM_NAME}").all()]

    def item_prices(self) -> list[float]:
        self._wait_items_ready(self.CART_ITEM, self.ITEM_NAME)
        return [
            self._parse_price(e.inner_text())
            for e in self.page.locator(f"{self.CART_ITEM} {self.ITEM_PRICE}").all()
        ]

    # ---------- 页面断言 ----------
    def expect_page(self) -> None:
        expect(self.page).to_have_url(f"{self.BASE_URL}checkout-step-two.html")

    def expect_summary(self, expect_item_total: float, expect_tax: float, expect_total: float) -> None:
        """断言商品小计、税费、总价与期望值一致（比较格式化后的金额字符串）。"""
        expect(self.page.locator(self.SUMMARY_SUBTOTAL)).to_have_text(f"Item total: ${expect_item_total:.2f}")
        expect(self.page.locator(self.SUMMARY_TAX)).to_have_text(f"Tax: ${expect_tax:.2f}")
        expect(self.page.locator(self.SUMMARY_TOTAL)).to_have_text(f"Total: ${expect_total:.2f}")
