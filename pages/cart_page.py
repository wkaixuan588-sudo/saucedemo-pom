# -*- coding: utf-8 -*-
"""购物车页面对象。"""
from playwright.sync_api import expect

from pages.base_page import BasePage


class CartPage(BasePage):
    """购物车页（/cart.html）。"""

    # ---------- 元素定位 ----------
    CHECKOUT_BUTTON = '[data-test="checkout"]'
    CONTINUE_SHOPPING_BUTTON = '[data-test="continue-shopping"]'
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"

    # ---------- 元素操作 ----------
    def remove_item(self, slug: str) -> "CartPage":
        """在购物车页移除指定商品。"""
        self.page.locator(f'[data-test="remove-{slug}"]').click()
        return self

    def click_checkout(self) -> "CheckoutInfoPage":
        """点击 Checkout 按钮进入结算信息页。"""
        self.page.locator(self.CHECKOUT_BUTTON).click()
        from pages.checkout_info_page import CheckoutInfoPage

        return CheckoutInfoPage(self.page)

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
        expect(self.page).to_have_url(f"{self.BASE_URL}cart.html")
