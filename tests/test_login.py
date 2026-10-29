# -*- coding: utf-8 -*-
"""登录功能测试用例。

设计思路（见 docs/test-design.md）：
- 等价类划分：6 个内置账号按"正常/性能异常/功能异常/视觉异常/锁定"分类，参数化覆盖；
- 边界值：用户名/密码为空；
- 错误推测：正确用户名 + 错误密码。
"""
import pytest

from tests.data import (
    LOGIN_MATRIX,
    STANDARD_PASSWORD,
    STANDARD_USER,
    WRONG_PASSWORD,
)

pytestmark = [pytest.mark.regression]


@pytest.mark.parametrize(
    "user, expected, error_fragment",
    LOGIN_MATRIX,
    ids=[u for u, _, _ in LOGIN_MATRIX],
)
def test_login_matrix(login_page, user, expected, error_fragment):
    """登录矩阵：各等价类账号的登录结果符合预期。"""
    login_page.login(user, STANDARD_PASSWORD)
    if expected == "success":
        login_page.expect_login_success()
    else:
        login_page.expect_error_visible(error_fragment)


def test_login_empty_username_and_password(login_page):
    """账号密码均为空时应提示 Username is required（判定优先级高于密码）。"""
    login_page.login("", "")
    login_page.expect_error_visible("Username is required")


def test_login_empty_password(login_page):
    """只填用户名、密码为空时应提示 Password is required。"""
    login_page.login(STANDARD_USER, "")
    login_page.expect_error_visible("Password is required")


def test_login_wrong_password(login_page):
    """正确用户名 + 错误密码应提示账号不匹配。"""
    login_page.login(STANDARD_USER, WRONG_PASSWORD)
    login_page.expect_error_visible("Username and password do not match")
