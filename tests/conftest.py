# -*- coding: utf-8 -*-
"""pytest 公共夹具与测试数据。"""
import pytest

from pages import InventoryPage, LoginPage

# ---------------- 测试数据 ----------------
STANDARD_USER = "standard_user"
STANDARD_PASSWORD = "secret_sauce"

CHECKOUT_FIRST_NAME = "John"
CHECKOUT_LAST_NAME = "Doe"
CHECKOUT_POSTAL_CODE = "100001"


@pytest.fixture
def login_page(page) -> LoginPage:
    """打开 saucedemo 登录页并返回页面对象。"""
    return LoginPage(page).open()


@pytest.fixture
def logged_in_inventory(login_page) -> InventoryPage:
    """使用 standard_user 登录后返回商品库存页对象。"""
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)
    login_page.expect_login_success()
    return InventoryPage(login_page.page)
