# -*- coding: utf-8 -*-
"""登录功能测试用例。"""
import pytest

from tests.data import STANDARD_PASSWORD, STANDARD_USER, WRONG_PASSWORD

pytestmark = [pytest.mark.regression]


@pytest.mark.smoke
def test_login_success(login_page):
    """standard_user + secret_sauce 可以成功登录并进入商品页。"""
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)
    login_page.expect_login_success()


def test_login_wrong_password(login_page):
    """密码错误时应提示账号不匹配的错误信息。"""
    login_page.login(STANDARD_USER, WRONG_PASSWORD)
    login_page.expect_error_visible("Username and password do not match")
