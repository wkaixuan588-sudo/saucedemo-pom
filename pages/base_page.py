# -*- coding: utf-8 -*-
"""页面基类：所有页面对象的公共父类。"""


class BasePage:
    """封装公共 URL 与 Page 实例，提供跨页面的通用操作。"""

    BASE_URL = "https://www.saucedemo.com/"

    def __init__(self, page):
        self.page = page

    def open(self, path: str = "") -> "BasePage":
        """打开指定路径的页面（相对 BASE_URL）。"""
        self.page.goto(f"{self.BASE_URL}{path}")
        return self
