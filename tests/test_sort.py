# -*- coding: utf-8 -*-
"""商品排序功能测试用例。

设计思路：四种排序选项参数化；名称排序断言完整序列，
价格排序只断言价格序列（15.99 两件同价商品间的先后顺序站点未定义，不做断言）。
"""
import pytest

from tests.data import PRODUCT_NAMES_AZ, PRODUCT_PRICES

pytestmark = [pytest.mark.regression]


def test_default_order_is_name_ascending(logged_in_inventory):
    """默认（不选排序）即为名称 A-Z 升序。"""
    assert logged_in_inventory.item_names() == PRODUCT_NAMES_AZ


def test_sort_name_descending(logged_in_inventory):
    """名称 Z-A 降序。"""
    logged_in_inventory.sort_by("za")
    logged_in_inventory.expect_first_item(PRODUCT_NAMES_AZ[-1])  # 哨兵：排序生效
    assert logged_in_inventory.item_names() == list(reversed(PRODUCT_NAMES_AZ))


def test_sort_price_low_to_high(logged_in_inventory):
    """价格从低到高。"""
    logged_in_inventory.sort_by("lohi")
    logged_in_inventory.expect_first_item("Sauce Labs Onesie")  # $7.99 最便宜
    assert logged_in_inventory.item_prices() == sorted(PRODUCT_PRICES)


def test_sort_price_high_to_low(logged_in_inventory):
    """价格从高到低。"""
    logged_in_inventory.sort_by("hilo")
    logged_in_inventory.expect_first_item("Sauce Labs Fleece Jacket")  # $49.99 最贵
    assert logged_in_inventory.item_prices() == sorted(PRODUCT_PRICES, reverse=True)
