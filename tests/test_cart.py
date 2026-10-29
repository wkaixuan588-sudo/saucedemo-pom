# -*- coding: utf-8 -*-
"""购物车操作测试用例。

设计思路：
- 场景法：加购/移除后角标与购物车列表的状态联动；
- 错误推测：error_user 账号存在部分商品"点击加购但角标不变"的静默失败
  （站点故意埋的缺陷，对应 docs/bugs/ 缺陷报告，此处先固化为负向用例）。
"""
import pytest

from pages import InventoryPage, LoginPage
from tests.data import (
    ERROR_USER_BROKEN_SLUGS,
    ERROR_USER_WORKING_SLUG,
    PRODUCTS,
    STANDARD_PASSWORD,
)

pytestmark = [pytest.mark.regression]


def test_add_and_remove_updates_badge(logged_in_inventory):
    """库存页加购/移除后，角标数量正确联动，清空后角标消失。"""
    inv = logged_in_inventory
    inv.add_to_cart("sauce-labs-backpack")
    inv.expect_cart_badge(1)
    inv.add_to_cart("sauce-labs-bike-light")
    inv.expect_cart_badge(2)

    inv.remove_from_cart("sauce-labs-backpack")
    inv.expect_cart_badge(1)
    inv.remove_from_cart("sauce-labs-bike-light")
    assert inv.cart_badge_count() is None  # 清空后角标消失


def test_remove_item_from_cart_page(logged_in_inventory):
    """购物车页移除单件商品后，列表与角标同步更新。"""
    inv = logged_in_inventory
    inv.add_to_cart("sauce-labs-backpack").add_to_cart("sauce-labs-onesie")
    cart = inv.open_cart()
    cart.expect_page()

    cart.remove_item("sauce-labs-backpack")
    assert cart.item_names() == [PRODUCTS["sauce-labs-onesie"][0]]


def test_error_user_add_to_cart_silently_fails(login_page):
    """error_user：部分商品点击加购后角标不变（静默失败，无任何错误提示）。

    对比设计：先加购一件正常商品证明会话可用，再验证问题商品。
    """
    login_page.login("error_user", STANDARD_PASSWORD)
    login_page.expect_login_success()
    inv = InventoryPage(login_page.page)

    # 正常商品加购成功，排除"会话/账号整体不可用"的其他解释
    inv.add_to_cart(ERROR_USER_WORKING_SLUG)
    inv.expect_cart_badge(1)

    # 问题商品：按钮可点击、无报错，但角标不变
    for slug in ERROR_USER_BROKEN_SLUGS:
        inv.add_to_cart(slug)
        assert inv.cart_badge_count() == 1, f"{slug} 静默加购失败应保持角标不变"
        assert inv.page.locator('[data-test="error"]').count() == 0, "静默失败：不应出现错误横幅"
