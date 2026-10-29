# -*- coding: utf-8 -*-
"""商品库存页面对象（登录后的首页）。"""
from playwright.sync_api import expect

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """商品库存页（/inventory.html）。"""

    # ---------- 元素定位 ----------
    CART_LINK = '[data-test="shopping-cart-link"]'
    CART_BADGE = '[data-test="shopping-cart-badge"]'
    SORT_CONTAINER = '[data-test="product-sort-container"]'
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"

    def _add_button(self, slug: str) -> str:
        """根据商品 slug（如 sauce-labs-backpack）生成加购按钮选择器。"""
        return f'[data-test="add-to-cart-{slug}"]'

    def _remove_button(self, slug: str) -> str:
        return f'[data-test="remove-{slug}"]'

    # ---------- 元素操作 ----------
    def add_to_cart(self, slug: str) -> "InventoryPage":
        """把指定商品加入购物车，slug 为商品标识，如 sauce-labs-backpack。"""
        self.page.locator(self._add_button(slug)).click()
        return self

    def remove_from_cart(self, slug: str) -> "InventoryPage":
        self.page.locator(self._remove_button(slug)).click()
        return self

    def sort_by(self, option: str) -> "InventoryPage":
        """选择排序方式，option 取值：az / za / lohi / hilo。"""
        self.page.locator(self.SORT_CONTAINER).select_option(option)
        return self

    def open_cart(self) -> "CartPage":
        """点击右上角购物车图标，进入购物车页。"""
        self.page.locator(self.CART_LINK).click()
        from pages.cart_page import CartPage

        return CartPage(self.page)

    # ---------- 数据读取 ----------
    def cart_badge_count(self) -> int | None:
        """读取购物车角标数量；未添加商品时角标不存在，返回 None。"""
        badge = self.page.locator(self.CART_BADGE)
        return int(badge.inner_text()) if badge.count() else None

    def item_names(self) -> list[str]:
        self._wait_items_ready(self.INVENTORY_ITEM, self.ITEM_NAME)
        return [e.inner_text() for e in self.page.locator(self.ITEM_NAME).all()]

    def item_prices(self) -> list[float]:
        self._wait_items_ready(self.INVENTORY_ITEM, self.ITEM_NAME)
        return [self._parse_price(e.inner_text()) for e in self.page.locator(self.ITEM_PRICE).all()]

    # ---------- 页面断言 ----------
    def expect_cart_badge(self, count: int) -> None:
        expect(self.page.locator(self.CART_BADGE)).to_have_text(str(count))

    def expect_first_item(self, name: str) -> None:
        """断言列表第一件商品名（排序后用作生效哨兵，expect 自动重试）。"""
        expect(self.page.locator(self.ITEM_NAME).first).to_have_text(name)
