# -*- coding: utf-8 -*-
"""购物与结算流程测试用例（对应手工验证过的主流程）。

流程：登录 -> 添加两款商品到购物车 -> 打开购物车 -> 填写收货信息
     -> 校验订单总览金额 -> 提交订单 -> 断言下单成功。
"""
from tests.conftest import (
    CHECKOUT_FIRST_NAME,
    CHECKOUT_LAST_NAME,
    CHECKOUT_POSTAL_CODE,
)

# 选择加购的两款商品（data-test 中的 slug）
BACKPACK_SLUG = "sauce-labs-backpack"
BIKE_LIGHT_SLUG = "sauce-labs-bike-light"
# 商品名与其单价（与站点一致，用于断言）
BACKPACK_NAME = "Sauce Labs Backpack"
BIKE_LIGHT_NAME = "Sauce Labs Bike Light"
BACKPACK_PRICE = 29.99
BIKE_LIGHT_PRICE = 9.99


def test_add_two_products_and_checkout(logged_in_inventory):
    """登录后添加两款商品到购物车并完成结算。"""
    # 1. 添加两款商品到购物车
    logged_in_inventory.add_to_cart(BACKPACK_SLUG).add_to_cart(BIKE_LIGHT_SLUG)

    # 2. 校验购物车角标数量为 2
    logged_in_inventory.expect_cart_badge(2)
    assert logged_in_inventory.cart_badge_count() == 2

    # 3. 进入购物车页，校验商品名与价格
    cart_page = logged_in_inventory.open_cart()
    cart_page.expect_page()
    assert cart_page.item_names() == [BACKPACK_NAME, BIKE_LIGHT_NAME]
    assert cart_page.item_prices() == [BACKPACK_PRICE, BIKE_LIGHT_PRICE]

    # 4. 点击 Checkout，填写收货信息并进入订单总览
    checkout_info = cart_page.click_checkout()
    checkout_info.expect_page()
    overview = checkout_info.fill_info_and_continue(
        CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME, CHECKOUT_POSTAL_CODE
    )
    overview.expect_page()

    # 5. 校验订单总览：商品、小计、税费、总价
    #    saucedemo 税率为 8%，总价 = 小计 + 税费
    assert overview.item_names() == [BACKPACK_NAME, BIKE_LIGHT_NAME]
    assert overview.item_prices() == [BACKPACK_PRICE, BIKE_LIGHT_PRICE]

    item_total = round(BACKPACK_PRICE + BIKE_LIGHT_PRICE, 2)   # 39.98
    tax = round(item_total * 0.08, 2)                          # 3.20
    total = round(item_total + tax, 2)                         # 43.18
    overview.expect_summary(item_total, tax, total)

    # 6. 提交订单，断言下单成功文案出现
    complete = overview.click_finish()
    complete.expect_order_complete()

    # 7. 返回首页，购物车角标应消失（下单后购物车被清空）
    inventory = complete.click_back_home()
    assert inventory.cart_badge_count() is None
