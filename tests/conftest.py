# -*- coding: utf-8 -*-
"""pytest 公共夹具（测试数据统一放 tests/data.py）。"""
import pytest

from pages import InventoryPage, LoginPage
from tests.data import STANDARD_PASSWORD, STANDARD_USER


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
